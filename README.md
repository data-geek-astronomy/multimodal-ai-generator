---
title: Multimodal AI Content Generator
emoji: 🎬
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🎬 Multimodal AI Content Generator

Turn a single text prompt into coordinated **image + video + audio narration** — entirely on CPU, no GPU required.

**Live demo:** https://huggingface.co/spaces/Darkweb007/multimodal-ai-generator

## What it does

**Input:** a text prompt (e.g. `"A beautiful sunset over mountains"`)

**Output:**
- 🖼️ a high-quality image (Stable Diffusion, via `diffusers`)
- 🎬 an MP4 video with a zoom/pan ("Ken Burns") effect (OpenCV, 16 frames by default)
- 🔊 spoken narration audio (offline TTS with an online fallback)

All three are generated from one pipeline call.

## Features

- ✅ **No GPU required** — runs on CPU (laptops, MacBooks, etc.)
- ✅ **Web interface** — Gradio UI for interactive use
- ✅ **CLI** — command-line entry point for scripting/automation
- ✅ **Python API** — import `src.inference.pipeline.run_pipeline` directly
- ✅ **Performance metrics** — per-stage timing and memory benchmarking
- ✅ **Auto-sync** — GitHub Actions workflow mirrors `main` to the Hugging Face Space

## Tech stack

| Component | Library |
|---|---|
| Image generation | [`diffusers`](https://github.com/huggingface/diffusers) (`stabilityai/sd-turbo` by default) |
| Video generation | OpenCV zoom/pan frame synthesis |
| Audio narration | `pyttsx3` (offline) with `gTTS` fallback |
| Web UI | Gradio |
| Infrastructure | GitHub + Hugging Face Spaces |

## Project structure

```
multimodal-ai-generator/
├── src/
│   ├── inference/          # image_gen, video_gen, audio_gen, pipeline
│   ├── evaluation/         # metrics.py — per-stage timing/memory
│   └── utils/              # config.py, helpers.py
├── app.py                  # Web UI (Gradio)
├── main.py                 # CLI
├── requirements.txt
├── packages.txt             # apt deps for HF Spaces (espeak-ng, ffmpeg)
└── tests/
```

## Quickstart

```bash
git clone https://github.com/data-geek-astronomy/multimodal-ai-generator.git
cd multimodal-ai-generator
pip install -r requirements.txt
```

### Web UI

```bash
python app.py
# → http://localhost:7860
```

### CLI

```bash
python main.py "A beautiful sunset over mountains" --steps 4 --output-dir outputs
```

### Python API

```python
from src.inference.pipeline import run_pipeline

result = run_pipeline("A cozy cabin in a snowy forest")
print(result.image_path, result.video_path, result.audio_path)
print(result.metrics.summary())
```

## Configuration

All defaults live in [`src/utils/config.py`](src/utils/config.py) and can be overridden via env vars
(`MAG_IMAGE_MODEL`, `MAG_IMAGE_WIDTH`, `MAG_STEPS`, `MAG_VIDEO_FRAMES`, `MAG_VIDEO_FPS`, `MAG_OUTPUT_DIR`, ...)
or CLI flags (`--steps`, `--width`, `--height`, `--frames`, `--fps`).

## Use cases

- 📚 **Content creators** — generate story illustrations/videos
- 🎓 **Educators** — create multimedia educational content
- 🎮 **Game devs** — generate game assets from descriptions
- 🎬 **Filmmakers** — quick storyboard visualization
- 📱 **Social media** — auto-generate posts with visuals

## Deployment

- **Local:** `python app.py` → http://localhost:7860
- **GitHub:** [data-geek-astronomy/multimodal-ai-generator](https://github.com/data-geek-astronomy/multimodal-ai-generator) — full source
- **Hugging Face Spaces:** [Darkweb007/multimodal-ai-generator](https://huggingface.co/spaces/Darkweb007/multimodal-ai-generator) — live demo, no setup needed

To enable the auto-sync GitHub Action, add a Hugging Face **write** access token as the `HF_TOKEN` secret
in the GitHub repo's Settings → Secrets → Actions. Every push to `main` will then mirror to the Space.

## License

[MIT](LICENSE)
