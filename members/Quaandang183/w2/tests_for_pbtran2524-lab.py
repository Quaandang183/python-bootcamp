"""Extra tests for the W1 modules (grades, rules, text_tools, timetable, translate).

Run with:
    pytest -v python-bootcamp/tests/test_w1_extra.py --member <your_folder>
"""
import pytest


# ---------- grades.py / rules.py (thesis eligibility) ----------
@pytest.mark.parametrize("module", ["grades", "rules"])
@pytest.mark.parametrize(
    ("credits", "gpa", "expected"),
    [
        (120, 2.0, True),
        (119, 2.0, False),
        (120, 1.99, False),
        (200, 4.0, True),
    ],
)
def test_can_register_thesis_boundaries(load, module, credits, gpa, expected):
    m = load("w1", module)
    assert m.can_register_thesis(credits, gpa) is expected


@pytest.mark.parametrize("module", ["grades", "rules"])
def test_missing_lists_every_reason(load, module):
    m = load("w1", module)
    assert m.missing(100, 1.5) == ["need 20 more credits", "gpa must be at least 2.0"]
    assert m.missing(120, 1.9) == ["gpa must be at least 2.0"]
    assert m.missing(125, 3.0) == []


# ---------- text_tools.py ----------
def test_word_count_ignores_case_and_punctuation(load):
    t = load("w1", "text_tools")
    assert t.word_count("Git, git! GIT?") == {"git": 3}
    assert t.word_count("a; b: a.") == {"a": 2, "b": 1}


def test_top_k_orders_by_count_then_alphabet(load):
    t = load("w1", "text_tools")
    assert t.top_k("b a b a c", 3) == [("a", 2), ("b", 2), ("c", 1)]
    assert t.top_k("b a b a c", 1) == [("a", 2)]


def test_edge_top_k_zero_and_k_larger_than_vocabulary(load):
    """EDGE CASE."""
    t = load("w1", "text_tools")
    assert t.top_k("x y", 0) == []
    assert t.top_k("x y", 10) == [("x", 1), ("y", 1)]


def test_edge_punctuation_only_text_gives_empty_result(load):
    """EDGE CASE."""
    t = load("w1", "text_tools")
    assert t.word_count("...!!! ?;:") == {}
    assert t.top_k("...!!!", 3) == []


# ---------- timetable.py ----------
def test_group_timetable_groups_and_sorts(load):
    tt = load("w1", "timetable")
    got = tt.group_timetable([("B2", "Mon"), ("A1", "Tue"), ("A0", "Mon")])
    assert got == {"Mon": ["A0", "B2"], "Tue": ["A1"]}
    assert tt.group_timetable([]) == {}


# ---------- translate.py (gcd) ----------
def test_gcd_basic_cases(load):
    tr = load("w1", "translate")
    assert tr.gcd(12, 18) == 6
    assert tr.gcd(17, 5) == 1
    assert tr.gcd(7, 0) == 7
    assert tr.gcd(0, 0) == 0


@pytest.mark.xfail(strict=True, reason="gcd(12, -18) return -6 instead of 6")
def test_edge_gcd_is_never_negative(load):
    """EDGE CASE: gcd can't be negative."""
    tr = load("w1", "translate")
    assert tr.gcd(12, -18) == 6
    assert tr.gcd(-12, -18) == 6
