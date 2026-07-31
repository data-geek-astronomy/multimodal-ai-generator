"""Gradio web UI for the Multimodal AI Content Generator.

Run locally with `python app.py`, or deploy as-is to a Hugging Face Space
(the gradio SDK auto-detects this file as the entry point).
"""
from __future__ import annotations

import gradio as gr

from src.inference.pipeline import run_pipeline
from src.utils.config import GenerationConfig
from src.utils.helpers import get_logger

logger = get_logger(__name__)

EXAMPLE_PROMPTS = [
    "A beautiful sunset over snow-capped mountains, golden hour, cinematic",
    "A cozy cabin in a pine forest during a gentle snowfall",
    "A futuristic city skyline at night with neon reflections on wet streets",
    "An astronaut floating above Earth, stars in the background",
]


def generate(prompt: str, narration: str, steps: int, width: int, height: int, frames: int, fps: int):
    if not prompt or not prompt.strip():
        raise gr.Error("Please enter a prompt.")

    config = GenerationConfig(
        image_width=int(width),
        image_height=int(height),
        num_inference_steps=int(steps),
        video_num_frames=int(frames),
        video_fps=int(fps),
    )

    try:
        result = run_pipeline(prompt.strip(), config=config, narration_text=narration.strip() or None)
    except Exception as exc:  # surface generation failures (e.g. model download issues) in the UI
        logger.exception("Generation failed")
        raise gr.Error(f"Generation failed: {exc}") from exc

    return (
        str(result.image_path),
        str(result.video_path),
        str(result.audio_path),
        result.metrics.summary(),
    )


with gr.Blocks(title="Multimodal AI Content Generator") as demo:
    gr.Markdown(
        """
        # 🎬 Multimodal AI Content Generator
        Describe a scene once — get a matching **image**, a **zoom/pan video**, and **narration audio**.
        Runs entirely on CPU, no GPU required.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            prompt = gr.Textbox(label="Prompt", placeholder="A beautiful sunset over mountains", lines=3)
            narration = gr.Textbox(label="Narration text (optional, defaults to prompt)", lines=2)
            gr.Examples(examples=EXAMPLE_PROMPTS, inputs=prompt)

            with gr.Accordion("Advanced settings", open=False):
                steps = gr.Slider(1, 20, value=4, step=1, label="Diffusion steps")
                width = gr.Dropdown([384, 512, 640, 768], value=512, label="Image width")
                height = gr.Dropdown([384, 512, 640, 768], value=512, label="Image height")
                frames = gr.Slider(4, 32, value=16, step=1, label="Video frames")
                fps = gr.Slider(4, 24, value=8, step=1, label="Video FPS")

            generate_btn = gr.Button("Generate", variant="primary")

        with gr.Column(scale=1):
            image_out = gr.Image(label="Generated image")
            video_out = gr.Video(label="Generated video")
            audio_out = gr.Audio(label="Narration")
            metrics_out = gr.Textbox(label="Timing", lines=5)

    generate_btn.click(
        fn=generate,
        inputs=[prompt, narration, steps, width, height, frames, fps],
        outputs=[image_out, video_out, audio_out, metrics_out],
    )

if __name__ == "__main__":
    demo.queue().launch()
