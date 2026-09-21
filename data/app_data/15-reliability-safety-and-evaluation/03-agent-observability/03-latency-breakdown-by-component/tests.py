"""pytest data/app_data/15-reliability-safety-and-evaluation/03-agent-observability/03-latency-breakdown-by-component/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

latency_breakdown = load_solution(
    f"15-reliability-safety-and-evaluation/03-agent-observability/{Path(__file__).resolve().parent.name}"
).latency_breakdown


def test_1_single_event_per_component():
    result = latency_breakdown([("llm", 1.2), ("tool", 0.5)])
    assert result == {"llm": 1.2, "tool": 0.5}


def test_2_repeated_component_sums():
    result = latency_breakdown([("llm", 1.0), ("tool", 0.3), ("llm", 0.5)])
    assert result == {"llm": 1.5, "tool": 0.3}


def test_3_single_component_many_events():
    result = latency_breakdown([("retrieval", 0.1), ("retrieval", 0.2), ("retrieval", 0.3)])
    assert abs(result["retrieval"] - 0.6) < 1e-9


def test_4_empty_events_returns_empty_dict():
    assert latency_breakdown([]) == {}


def test_5_order_of_components_does_not_affect_sums():
    result = latency_breakdown([("a", 1.0), ("b", 2.0), ("a", 3.0), ("b", 4.0)])
    assert result == {"a": 4.0, "b": 6.0}
