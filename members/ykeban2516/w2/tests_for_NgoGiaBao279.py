# ruff: noqa: N999
# Assignment requires the reviewee's username in the filename.

from importlib import import_module

import pytest


PREFIX = "members.NgoGiaBao279.w1"


def test_summary():
    module = import_module(f"{PREFIX}.grades")

    assert module.summary([7.5, 9, 6, 8]) == {
        "min": 6,
        "max": 9,
        "mean": 7.62,
        "median": 7.75,
    }


def test_summary_empty():
    module = import_module(f"{PREFIX}.grades")

    with pytest.raises(ValueError):
        module.summary([])


def test_word_count():
    module = import_module(f"{PREFIX}.text_tools")

    assert module.word_count("Git is fun. Git is fast!") == {
        "git": 2,
        "is": 2,
        "fun": 1,
        "fast": 1,
    }


def test_top_k_alphabetical_tie():
    module = import_module(f"{PREFIX}.text_tools")

    assert module.top_k("zebra apple zebra apple", 2) == [
        ("apple", 2),
        ("zebra", 2),
    ]


def test_thesis_boundary():
    module = import_module(f"{PREFIX}.rules")

    assert module.can_register_thesis(120, 2.0)
    assert not module.can_register_thesis(119, 2.0)
    assert not module.can_register_thesis(120, 1.99)


def test_missing_both_requirements():
    module = import_module(f"{PREFIX}.rules")

    assert len(module.missing(100, 1.5)) == 2


def test_timetable_sorting():
    module = import_module(f"{PREFIX}.timetable")

    assert module.by_day([
        ("Z", "Mon"),
        ("A", "Mon"),
        ("B", "Tue"),
    ]) == {
        "Mon": ["A", "Z"],
        "Tue": ["B"],
    }
