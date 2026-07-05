#!/usr/bin/env python3
"""
Generate 5 TEXT-FREE photoreal backgrounds (Direction B) via local ComfyUI FLUX,
then bake a legibility scrim into each so the editable Canva template has ONE clean
background layer + separate movable text/logo/CTA layers (no baked-in text).

Output: bdark_<key>.png (1080x1080) in this dir, ready to push + reference in HTML.
    python3 gen_b_backgrounds.py
"""
import json, os, sys, time, urllib.request, urllib.parse
from PIL import Image

BASE_URL = os.environ.get("COMFY_BASE_URL", "http://127.0.0.1:8188")
HERE = os.path.dirname(os.path.abspath(__file__))
S = 1080

NEG = "no text, no words, no letters, no typography, no captions, no watermark, no signage, no posters, no writing"
POSTS = [
  ("get_found", 111, f"photorealistic candid lifestyle photo of a happy young Indian man in his early twenties looking at his smartphone with a hopeful smile, sitting in a bright modern cafe by a window, warm natural morning light, shallow depth of field, the person on the RIGHT third of the frame, clean uncluttered softly-blurred darker area on the LEFT, cinematic color grade, 35mm, high detail, {NEG}"),
  ("bad_hire", 222, f"photorealistic cinematic photo of a stressed corporate hiring manager at a desk beside a very tall stack of paper resumes in a modern glass office, moody dramatic blue lighting, the person and stack on the RIGHT, deep dark empty negative space on the LEFT half, 35mm, {NEG}"),
  ("marketplace", 333, f"abstract 3D render, a single glowing central node connecting two clusters of soft glowing dots on the left and right, deep navy background, blue and violet volumetric light, minimal futuristic clean, large empty dark areas, depth of field, {NEG}"),
  ("brand", 444, f"photorealistic photo of a confident diverse young Indian startup team of four standing together in a bright modern office, gentle smiles looking toward camera, soft natural window light, the group on the RIGHT and center, darker clean wall area on the LEFT for text, cinematic, 35mm, {NEG}"),
  ("campus", 555, f"photorealistic candid photo of diverse Indian university students walking and chatting together on a green leafy college campus pathway, warm sunny natural light, students grouped on the RIGHT, softer shaded darker area lower-LEFT, cinematic shallow depth of field, 35mm, {NEG}"),
]

def flux_workflow(prompt, seed, w=1024, h=1024, steps=22):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "flux1-dev-fp8.safetensors"}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": "", "clip": ["1", 1]}},
        "4": {"class_type": "FluxGuidance", "inputs": {"conditioning": ["2", 0], "guidance": 3.5}},
        "5": {"class_type": "EmptySD3LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "6": {"class_type": "KSampler", "inputs": {
            "model": ["1", 0], "positive": ["4", 0], "negative": ["3", 0], "latent_image": ["5", 0],
            "seed": seed, "steps": steps, "cfg": 1.0, "sampler_name": "euler", "scheduler": "beta", "denoise": 1.0}},
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},
        "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": "gy_bclean/post"}},
    }

def queue(wf):
    req = urllib.request.Request(f"{BASE_URL}/prompt", data=json.dumps({"prompt": wf}).encode(),
                                 headers={"Content-Type": "application/json"})
    body = json.loads(urllib.request.urlopen(req).read())
    if "error" in body: raise RuntimeError(json.dumps(body["error"], indent=2))
    return body["prompt_id"]

def wait(pid, timeout=900):
    t0 = time.time()
    while time.time() - t0 < timeout:
        hist = json.loads(urllib.request.urlopen(f"{BASE_URL}/history/{pid}").read())
        if pid in hist:
            st = hist[pid].get("status", {})
            if st.get("completed"): return hist[pid]
            if st.get("status_str") == "error": raise RuntimeError(json.dumps(st, indent=2))
        print(f"    ...generating ({int(time.time()-t0)}s)", file=sys.stderr); time.sleep(3)
    raise TimeoutError(f"timeout on {pid}")

def fetch(prompt, seed, dest):
    entry = wait(queue(flux_workflow(prompt, seed)))
    imgs = entry.get("outputs", {}).get("8", {}).get("images", [])
    if not imgs: raise RuntimeError("no image output")
    v = imgs[0]
    qs = urllib.parse.urlencode({"filename": v["filename"], "subfolder": v.get("subfolder", ""), "type": v.get("type", "output")})
    with urllib.request.urlopen(f"{BASE_URL}/view?{qs}") as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest

def cover(im, size=S):
    im = im.convert("RGB"); w, h = im.size; s = min(w, h)
    im = im.crop(((w-s)//2, (h-s)//2, (w-s)//2+s, (h-s)//2+s))
    return im.resize((size, size), Image.LANCZOS)

def hgrad(a_left, fade_end=0.78):
    """1080-wide horizontal alpha ramp (dark navy on left → clear), baked as RGBA."""
    row = Image.new("RGBA", (S, 1))
    px = row.load()
    for x in range(S):
        a = int(a_left * max(0.0, 1.0 - x/(S*fade_end)))
        px[x, 0] = (9, 12, 26, a)
    return row.resize((S, S), Image.NEAREST)

def vgrad(a_bot, start=0.42):
    col = Image.new("RGBA", (1, S)); px = col.load(); s0 = int(S*start)
    for y in range(S):
        t = 0.0 if y < s0 else (y-s0)/max(1, S-s0)
        px[0, y] = (9, 12, 26, int(a_bot*t))
    return col.resize((S, S), Image.NEAREST)

def darken(clean_path, out_path):
    base = cover(Image.open(clean_path)).convert("RGBA")
    base = Image.alpha_composite(base, Image.new("RGBA", base.size, (0, 0, 0, 45)))   # slight overall
    base = Image.alpha_composite(base, hgrad(238))                                    # strong left for headline
    base = Image.alpha_composite(base, vgrad(235))                                    # bottom for CTA
    base.convert("RGB").save(out_path, quality=92)

def main():
    for key, seed, prompt in POSTS:
        clean = os.path.join(HERE, f"bclean_{key}.png")
        dark  = os.path.join(HERE, f"bdark_{key}.png")
        print(f"[{key}] generating…", file=sys.stderr)
        fetch(prompt, seed, clean)
        darken(clean, dark)
        print(f"[{key}] -> {os.path.basename(dark)}")
    print("DONE 5 backgrounds")

if __name__ == "__main__":
    main()
