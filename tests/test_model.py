import os
os.environ["TESTING"] = "true"

from src.fair_evaluator.models import Fair


def test_fair_model_fields():
    f = Fair(id="f1", name="Test Fair", url="https://example.com/fair", dates=["2026-06-01"])
    assert f.id == "f1"
    assert f.name == "Test Fair"
    assert f.url == "https://example.com/fair"
