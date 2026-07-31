#!/usr/bin/env python
"""CLI for the Multimodal AI Content Generator.

Example:
    python main.py "A beautiful sunset over mountains" --steps 4 --output-dir outputs
"""
from __future__ import annotations

import argparse
import sys

from src.inference.pipeline import run_pipeline
from src.utils.config import GenerationConfig
from src.utils.helpers import get_logger

logger = get_logger(__name__)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate an image, video, and narration from a text prompt.")
    parser.add_argument("prompt", type=str, help="Text prompt describing the scene to generate.")
    parser.add_argument("--narration", type=str, default=None, help="Narration text (defaults to the prompt).")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Directory where run outputs are saved.")
    parser.add_argument("--image-model", type=str, default="stabilityai/sd-turbo", help="Diffusers model id for image generation.")
    parser.add_argument("--width", type=int, default=512, help="Image width in pixels.")
    parser.add_argument("--height", type=int, default=512, help="Image height in pixels.")
    parser.add_argument("--steps", type=int, default=4, help="Number of diffusion inference steps.")
    parser.add_argument("--frames", type=int, default=16, help="Number of video frames.")
    parser.add_argument("--fps", type=int, default=8, help="Video frames per second.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    config = GenerationConfig(
        image_model=args.image_model,
        image_width=args.width,
        image_height=args.height,
        num_inference_steps=args.steps,
        video_num_frames=args.frames,
        video_fps=args.fps,
        output_dir=args.output_dir,
    )

    result = run_pipeline(args.prompt, config=config, narration_text=args.narration)

    print(f"\nDone. Outputs saved to: {result.run_dir}")
    print(f"  image:     {result.image_path}")
    print(f"  video:     {result.video_path}")
    print(f"  narration: {result.audio_path}")
    print("\nTiming:")
    print(result.metrics.summary())
    return 0


if __name__ == "__main__":
    sys.exit(main())
