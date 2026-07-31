"""Central configuration for the multimodal generator, overridable via env vars."""
import os
from dataclasses import dataclass, field


def _env_int(name: str, default: int) -> int:
    return int(os.environ.get(name, default))


def _env_str(name: str, default: str) -> str:
    return os.environ.get(name, default)


@dataclass
class GenerationConfig:
    # Image generation
    image_model: str = field(default_factory=lambda: _env_str("MAG_IMAGE_MODEL", "stabilityai/sd-turbo"))
    image_width: int = field(default_factory=lambda: _env_int("MAG_IMAGE_WIDTH", 512))
    image_height: int = field(default_factory=lambda: _env_int("MAG_IMAGE_HEIGHT", 512))
    num_inference_steps: int = field(default_factory=lambda: _env_int("MAG_STEPS", 4))
    guidance_scale: float = 0.0  # sd-turbo is distilled for guidance-free sampling

    # Video generation
    video_num_frames: int = field(default_factory=lambda: _env_int("MAG_VIDEO_FRAMES", 16))
    video_fps: int = field(default_factory=lambda: _env_int("MAG_VIDEO_FPS", 8))
    video_zoom_factor: float = 1.15

    # Audio generation
    tts_rate: int = field(default_factory=lambda: _env_int("MAG_TTS_RATE", 165))

    # Output
    output_dir: str = field(default_factory=lambda: _env_str("MAG_OUTPUT_DIR", "outputs"))

    # Device — CPU only by design (no GPU required)
    device: str = "cpu"
    torch_dtype: str = "float32"


DEFAULT_CONFIG = GenerationConfig()
