"""Turns a still image into a short zoom/pan ("Ken Burns") MP4 clip using OpenCV."""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from src.utils.config import GenerationConfig, DEFAULT_CONFIG
from src.utils.helpers import get_logger

logger = get_logger(__name__)


def _ease_in_out(t: float) -> float:
    """Smootherstep easing so the zoom doesn't feel linear/robotic."""
    return t * t * (3 - 2 * t)


def _zoom_pan_frame(image: np.ndarray, progress: float, zoom_factor: float) -> np.ndarray:
    """Crop a shrinking window from the source image and resize back up (zoom-in effect)."""
    h, w = image.shape[:2]
    eased = _ease_in_out(progress)
    scale = 1.0 + (zoom_factor - 1.0) * eased

    crop_w, crop_h = int(w / scale), int(h / scale)
    # Gentle diagonal pan alongside the zoom.
    max_x_off, max_y_off = w - crop_w, h - crop_h
    x_off = int(max_x_off * eased * 0.5)
    y_off = int(max_y_off * eased * 0.5)

    cropped = image[y_off:y_off + crop_h, x_off:x_off + crop_w]
    return cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)


def generate_video(
    image_path: str | Path,
    output_path: str | Path,
    config: GenerationConfig = DEFAULT_CONFIG,
) -> Path:
    """Render a zoom/pan video from a single source image."""
    pil_image = Image.open(image_path).convert("RGB")
    frame_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    h, w = frame_bgr.shape[:2]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_path), fourcc, config.video_fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError(f"Could not open video writer for {output_path}")

    try:
        n = max(config.video_num_frames, 2)
        for i in range(n):
            progress = i / (n - 1)
            frame = _zoom_pan_frame(frame_bgr, progress, config.video_zoom_factor)
            writer.write(frame)
    finally:
        writer.release()

    logger.info("Saved %d-frame video to %s", config.video_num_frames, output_path)
    return output_path
