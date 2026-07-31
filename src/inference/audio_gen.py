"""Text-to-speech narration with a resilient fallback chain.

Tries, in order:
  1. pyttsx3   - fully offline, uses the OS speech engine (needs espeak-ng on Linux)
  2. gTTS      - online, works anywhere with internet access (e.g. HF Spaces)
  3. silence   - last resort so the pipeline never hard-fails on audio alone
"""
from __future__ import annotations

import wave
from pathlib import Path

from src.utils.config import GenerationConfig, DEFAULT_CONFIG
from src.utils.helpers import get_logger

logger = get_logger(__name__)


def _try_pyttsx3(text: str, wav_path: Path, rate: int) -> bool:
    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.setProperty("rate", rate)
        engine.save_to_file(text, str(wav_path))
        engine.runAndWait()
        engine.stop()
        return wav_path.exists() and wav_path.stat().st_size > 0
    except Exception as exc:  # pragma: no cover - depends on host TTS engine availability
        logger.warning("pyttsx3 TTS failed (%s); falling back to gTTS.", exc)
        return False


def _try_gtts(text: str, mp3_path: Path) -> bool:
    try:
        from gtts import gTTS

        gTTS(text=text).save(str(mp3_path))
        return mp3_path.exists() and mp3_path.stat().st_size > 0
    except Exception as exc:  # pragma: no cover - depends on network availability
        logger.warning("gTTS failed (%s); falling back to silent placeholder.", exc)
        return False


def _write_silence(wav_path: Path, duration_s: float = 2.0, sample_rate: int = 22050) -> None:
    n_frames = int(duration_s * sample_rate)
    with wave.open(str(wav_path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * n_frames)
    logger.warning("No TTS backend available; wrote %.1fs of silence to %s", duration_s, wav_path)


def generate_audio(
    text: str,
    output_path: str | Path,
    config: GenerationConfig = DEFAULT_CONFIG,
) -> Path:
    """Generate narration audio for ``text``. Returns the actual path written (extension may
    differ from what was requested, since backends produce different formats)."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    stem = output_path.with_suffix("")

    wav_path = stem.with_suffix(".wav")
    if _try_pyttsx3(text, wav_path, config.tts_rate):
        logger.info("Saved narration (pyttsx3) to %s", wav_path)
        return wav_path

    mp3_path = stem.with_suffix(".mp3")
    if _try_gtts(text, mp3_path):
        logger.info("Saved narration (gTTS) to %s", mp3_path)
        return mp3_path

    _write_silence(wav_path)
    return wav_path
