"""DIP-13 / NFR-11: the API contract and all its JSON examples must stay valid."""
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs" / "api" / "openapi.yaml"


def test_contract_validation_script_passes():
    result = subprocess.run(
        [sys.executable, "-W", "ignore", str(ROOT / "scripts" / "check_openapi.py"), str(SPEC)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_contract_covers_core_endpoints():
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    for path in ["/analyze", "/batches", "/batches/{batch_id}", "/batches/{batch_id}/items",
                 "/batches/{batch_id}/stats", "/batches/{batch_id}/export", "/health", "/model"]:
        assert path in spec["paths"], f"missing endpoint {path}"


def test_emotion_label_set_matches_requirements():
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    labels = spec["components"]["schemas"]["Emotion"]["enum"]
    assert labels == ["joy", "sadness", "anger", "fear", "surprise", "neutral"]  # DOC-06 §6.1.1
    assert spec["components"]["schemas"]["Language"]["enum"] == ["kk", "ru", "mixed"]  # FR-02
