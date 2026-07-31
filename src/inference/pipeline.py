"""Orchestrates image -> video -> audio generation from a single text prompt."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.evaluation.metrics import PipelineMetrics
from src.inference.audio_gen import generate_audio
from src.inference.image_gen import generate_image
from src.inference.video_gen import generate_video
from src.utils.config import GenerationConfig, DEFAULT_CONFIG
from src.utils.helpers import get_logger, make_run_dir

logger = get_logger(__name__)


@dataclass
class PipelineResult:
    prompt: str
    run_dir: Path
    image_path: Path
    video_path: Path
    audio_path: Path
    metrics: PipelineMetrics


def run_pipeline(
    prompt: str,
    config: GenerationConfig = DEFAULT_CONFIG,
    narration_text: str | None = None,
) -> PipelineResult:
    """Run the full text -> image -> video -> audio pipeline for ``prompt``.

    ``narration_text`` defaults to the prompt itself so the narration always matches
    what was actually generated.
    """
    run_dir = make_run_dir(config.output_dir, prompt)
    metrics = PipelineMetrics()

    with metrics.stage("image"):
        image_path = generate_image(prompt, run_dir / "image.png", config)

    with metrics.stage("video"):
        video_path = generate_video(image_path, run_dir / "video.mp4", config)

    with metrics.stage("audio"):
        audio_path = generate_audio(narration_text or prompt, run_dir / "narration.wav", config)

    metrics.save(run_dir / "metrics.json")
    logger.info("Pipeline finished in %.2fs -> %s", metrics.total_seconds, run_dir)

    return PipelineResult(
        prompt=prompt,
        run_dir=run_dir,
        image_path=image_path,
        video_path=video_path,
        audio_path=audio_path,
        metrics=metrics,
    )
