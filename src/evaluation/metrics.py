"""Lightweight performance benchmarking for each pipeline stage (no external deps required)."""
from __future__ import annotations

import json
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

try:
    import psutil

    _PROCESS = psutil.Process()
except ImportError:  # pragma: no cover - psutil is a listed dependency but degrade gracefully
    psutil = None
    _PROCESS = None


def _rss_mb() -> float | None:
    if _PROCESS is None:
        return None
    return round(_PROCESS.memory_info().rss / (1024 * 1024), 2)


@dataclass
class StageTiming:
    name: str
    seconds: float
    memory_mb: float | None


@dataclass
class PipelineMetrics:
    stages: list[StageTiming] = field(default_factory=list)

    @contextmanager
    def stage(self, name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start
            self.stages.append(StageTiming(name=name, seconds=round(elapsed, 3), memory_mb=_rss_mb()))

    @property
    def total_seconds(self) -> float:
        return round(sum(s.seconds for s in self.stages), 3)

    def as_dict(self) -> dict:
        return {
            "stages": [s.__dict__ for s in self.stages],
            "total_seconds": self.total_seconds,
        }

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.as_dict(), indent=2))

    def summary(self) -> str:
        lines = [f"{s.name:>8}: {s.seconds:6.2f}s" + (f"  ({s.memory_mb} MB RSS)" if s.memory_mb else "") for s in self.stages]
        lines.append(f"{'total':>8}: {self.total_seconds:6.2f}s")
        return "\n".join(lines)
