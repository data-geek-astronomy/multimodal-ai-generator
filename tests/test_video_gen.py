"""Video generation is pure OpenCV/PIL, so it's tested without any model downloads."""
from pathlib import Path

import numpy as np
from PIL import Image

from src.inference.video_gen import generate_video
from src.utils.config import GenerationConfig


def test_generate_video_from_image(tmp_path):
    image_path = tmp_path / "source.png"
    Image.fromarray(np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)).save(image_path)

    config = GenerationConfig(video_num_frames=6, video_fps=6)
    video_path = generate_video(image_path, tmp_path / "out.mp4", config)

    assert Path(video_path).exists()
    assert Path(video_path).stat().st_size > 0
