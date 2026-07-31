"""CPU-friendly text-to-image generation using a distilled Stable Diffusion model."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PIL import Image

from src.utils.config import GenerationConfig, DEFAULT_CONFIG
from src.utils.helpers import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def _load_pipeline(model_id: str):
    """Load and cache the diffusion pipeline so repeated calls reuse the weights."""
    import torch
    from diffusers import AutoPipelineForText2Image

    logger.info("Loading image model '%s' on CPU (first run downloads the weights)...", model_id)
    pipe = AutoPipelineForText2Image.from_pretrained(
        model_id,
        torch_dtype=torch.float32,
        safety_checker=None,
    )
    pipe.to("cpu")
    return pipe


def generate_image(
    prompt: str,
    output_path: str | Path,
    config: GenerationConfig = DEFAULT_CONFIG,
) -> Path:
    """Generate a single image from a text prompt and save it to ``output_path``."""
    pipe = _load_pipeline(config.image_model)

    result = pipe(
        prompt=prompt,
        num_inference_steps=config.num_inference_steps,
        guidance_scale=config.guidance_scale,
        width=config.image_width,
        height=config.image_height,
    )
    image: Image.Image = result.images[0]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    logger.info("Saved image to %s", output_path)
    return output_path
