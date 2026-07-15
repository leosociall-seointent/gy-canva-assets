#!/usr/bin/env python3
"""Generate text-free FLUX photoreal backgrounds (ComfyUI :8188) for the 8 hero cards.
Indian context, cinematic, dark negative space for text, NO text/logos in the image.
Writes flux_<key>.png. ~2 min/image on MPS."""
import json, time, sys, urllib.request, urllib.parse
BASE_URL = "http://127.0.0.1:8188"

def flux_workflow(prompt, seed, w=1080, h=1080, steps=22):
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
        "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": "gy_hero/bg"}},
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
        time.sleep(3)
    raise TimeoutError(f"timeout on {pid}")

def fetch_bg(prompt, seed, dest):
    entry = wait(queue(flux_workflow(prompt, seed)))
    imgs = entry.get("outputs", {}).get("8", {}).get("images", [])
    if not imgs: raise RuntimeError("no image output")
    v = imgs[0]
    qs = urllib.parse.urlencode({"filename": v["filename"], "subfolder": v.get("subfolder", ""), "type": v.get("type", "output")})
    with urllib.request.urlopen(f"{BASE_URL}/view?{qs}") as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest

NEG_FREE = "cinematic photograph, shallow depth of field, natural light, no text, no words, no logos, no watermark, no signage"
HEROES = {
  "flux_12_weekend": f"candid documentary photo of a young Indian woman in her mid-20s sitting by a large sunlit window, smiling with quiet joy while looking at her phone, warm golden-hour light, soft warm bokeh, hopeful mood, dark negative space on the left third for text, {NEG_FREE}",
  "flux_15_sat":     f"a focused young Indian college graduate taking an online assessment on a laptop at a clean minimal desk, determined hopeful expression, soft daylight, modern room, dark negative space on the right side for text, {NEG_FREE}",
  "flux_29_route":   f"a confident Indian professional working intently at a modern office desk, glass-office bokeh behind, moody cool blue tones, not looking at camera, dark negative space on the left for text, {NEG_FREE}",
  "flux_32_team":    f"a modern Indian recruiting team of three people collaborating around a laptop in a bright office, professional and energetic, dark gradient area along the bottom for text, {NEG_FREE}",
  "flux_42_interview": f"a warm friendly job-interview scene, a young Indian fresher smiling across a table from an interviewer seen over the shoulder, bright modern office, encouraging mood, dark negative space along the top for text, {NEG_FREE}",
  "flux_46_post":    f"an Indian hiring manager quickly typing to post a job on a laptop in a bright modern office, sense of speed and ease, clean minimal desk, dark negative space on the left for text, {NEG_FREE}",
  "flux_47_matches": f"a warm group portrait of four diverse young Indian professionals in a bright modern workspace, genuine natural smiles, sense of community, soft light, dark gradient along the bottom for text, {NEG_FREE}",
  "flux_54_hire":    f"a poised Indian job candidate in smart-casual attire standing confidently in a modern office lobby, employer point of view, blue-hour tones, glass and greenery, dark negative space on the right for text, {NEG_FREE}",
}
if __name__ == "__main__":
    keys = sys.argv[1:] or list(HEROES)
    for i, k in enumerate(keys):
        seed = 700000 + i*13
        print(f"[{i+1}/{len(keys)}] {k} seed={seed}", flush=True)
        try:
            fetch_bg(HEROES[k], seed, f"{k}.png"); print(f"    saved {k}.png", flush=True)
        except Exception as e:
            print(f"    FAILED {k}: {e}", flush=True)
    print("DONE flux heroes", flush=True)
