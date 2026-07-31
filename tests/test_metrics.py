import json
from pathlib import Path

from src.evaluation.metrics import PipelineMetrics


def test_stage_timing_and_save(tmp_path):
    metrics = PipelineMetrics()
    with metrics.stage("dummy"):
        pass

    assert len(metrics.stages) == 1
    assert metrics.stages[0].name == "dummy"
    assert metrics.total_seconds >= 0

    out = tmp_path / "metrics.json"
    metrics.save(out)
    data = json.loads(Path(out).read_text())
    assert data["stages"][0]["name"] == "dummy"
