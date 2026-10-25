"""Unit test suite covering module functions for member ykeban2516 (Week 1)."""

import pytest

from members.ykeban2516.w1.grades import summary
from members.ykeban2516.w1.rules import can_register_thesis, missing
from members.ykeban2516.w1.text_tools import word_count, top_k
from members.ykeban2516.w1.timetable import by_day
from members.ykeban2516.w1.translate import transpose


def test_grades_summary_basic() -> None:
    """Test standard calculation of summary statistics (min, max, mean, median) for a list of grades."""
    scores = [8.0, 9.0, 7.0, 10.0]
    res = summary(scores)
    assert res["min"] == 7.0
    assert res["max"] == 10.0
    assert res["mean"] == 8.5
    assert res["median"] == 8.5


def test_rules_can_register_thesis() -> None:
    """Test thesis registration rules validation and detailed missing requirement reason logging."""
    assert can_register_thesis(120, 2.0) is True
    assert can_register_thesis(119, 3.5) is False
    assert can_register_thesis(130, 1.9) is False

    reasons = missing(110, 1.8)
    assert "need 10 more credits" in reasons
    assert "need GPA of at least 2.0" in reasons


def test_text_tools_top_k() -> None:
    """Test text parsing tools for word counting and extracting top-k most frequent words."""
    text = "Python, Java, Python! C++, Python, Java."
    counts = word_count(text)
    assert counts["python"] == 3
    assert counts["java"] == 2

    top2 = top_k(text, 2)
    assert top2 == [("python", 3), ("java", 2)]


def test_timetable_by_day() -> None:
    """Test timetable aggregation by weekday with alphabetically sorted course lists."""
    data = [("Math", "Mon"), ("Physics", "Mon"), ("Chemistry", "Tue"), ("Algebra", "Mon")]
    res = by_day(data)
    # Course names within each day must be sorted in alphabetical order
    assert res["Mon"] == ["Algebra", "Math", "Physics"]
    assert res["Tue"] == ["Chemistry"]


def test_translate_transpose() -> None:
    """Test 2D matrix transposition logic for converting rows to columns."""
    matrix = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    expected = [
        [1, 4],
        [2, 5],
        [3, 6]
    ]
    assert transpose(matrix) == expected


def test_grades_summary_edge_case_empty_list() -> None:
    """Test edge case handling when passing an empty list to summary(), expecting ValueError."""
    with pytest.raises(ValueError, match="List is empty"):
        summary([])