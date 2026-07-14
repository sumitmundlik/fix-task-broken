import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected_summary():
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def test_report_exists():
    """Success criterion 1: report.json exists."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"


def test_report_is_valid_json():
    """Success criterion 1: report.json contains valid JSON."""
    try:
        json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        raise AssertionError(f"report.json is not valid JSON: {e}")


def test_report_has_required_fields():
    """Success criterion 2: required fields and types."""
    data = json.loads(REPORT_PATH.read_text())
    assert isinstance(data.get("total_requests"), int), (
        "total_requests missing or not an int"
    )
    assert isinstance(data.get("unique_ips"), int), (
        "unique_ips missing or not an int"
    )
    assert isinstance(data.get("top_path"), str), (
        "top_path missing or not a string"
    )


def test_report_matches_expected_values():
    """Success criterion 3: values match parsed log."""
    expected = _expected_summary()
    actual = json.loads(REPORT_PATH.read_text())
    assert actual.get("total_requests") == expected["total_requests"], (
        f"total_requests: expected {expected['total_requests']}, "
        f"got {actual.get('total_requests')}"
    )
    assert actual.get("unique_ips") == expected["unique_ips"], (
        f"unique_ips: expected {expected['unique_ips']}, "
        f"got {actual.get('unique_ips')}"
    )
    assert actual.get("top_path") == expected["top_path"], (
        f"top_path: expected {expected['top_path']!r}, "
        f"got {actual.get('top_path')!r}"
    )