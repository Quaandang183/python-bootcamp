# ruff: noqa: N999
# Assignment requires the reviewee's username in the filename.

import pytest

from members.NgoGiaBao279.w1.grades import grade_sum
from members.NgoGiaBao279.w1.rules import can_register_thesis, missing
from members.NgoGiaBao279.w1.text_tools import top_K, word_count
from members.NgoGiaBao279.w1.timetable import group_timetable


def test_grade_sum_standard():
    assert grade_sum([7.5, 9, 6, 8]) == {
        "min": 6,
        "max": 9,
        "mean": 7.62,
        "median": 7.75,
    }


def test_grade_sum_empty():
    with pytest.raises(ValueError):
        grade_sum([])


def test_word_count():
    assert word_count("Git is fun. Git is fast!") == {
        "git": 2,
        "is": 2,
        "fun": 1,
        "fast": 1,
    }


def test_top_k_alphabetical_tie():
    assert top_K("zebra apple zebra apple", 2) == [
        ("apple", 2),
        ("zebra", 2),
    ]


def test_thesis_boundary():
    assert can_register_thesis(120, 2.0)
    assert not can_register_thesis(119, 2.0)
    assert not can_register_thesis(120, 1.99)


def test_missing_both_requirements():
    reasons = missing(100, 1.5)
    assert len(reasons) == 1
    assert "20" in reasons[0]
    assert "GPA" in reasons[0]


def test_timetable_sorting():
    assert group_timetable([("Z", "Mon"), ("A", "Mon"), ("B", "Tue")]) == {
        "Mon": ["A", "Z"],
        "Tue": ["B"],
    }
