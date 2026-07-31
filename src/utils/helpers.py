"""Shared helpers: logging setup and filesystem utilities."""
import logging
import re
import time
import uuid
from pathlib import Path


def get_logger(name: str = "multimodal_ai_generator") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def slugify(text: str, max_len: int = 40) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return slug[:max_len] or "untitled"


def make_run_dir(output_dir: str, prompt: str) -> Path:
    run_id = f"{int(time.time())}-{slugify(prompt)}-{uuid.uuid4().hex[:6]}"
    run_dir = Path(output_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir
