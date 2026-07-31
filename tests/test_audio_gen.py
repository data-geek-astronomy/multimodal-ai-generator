"""Audio generation always produces a file, even if every TTS backend is unavailable."""
from pathlib import Path

from src.inference.audio_gen import generate_audio
from src.utils.config import GenerationConfig


def test_generate_audio_produces_a_file(tmp_path):
    output = generate_audio("Hello world", tmp_path / "narration.wav", GenerationConfig())
    assert Path(output).exists()
    assert Path(output).stat().st_size > 0
