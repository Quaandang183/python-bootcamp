# ruff: noqa: N999
import sys
from pathlib import Path

current_file = Path(__file__).resolve()
possible_bootcamp_roots = [
    current_file.parents[2],
    current_file.parent.parent / "python-bootcamp",
    Path(r"c:\Users\gbao1\Downloads\python-bootcamp"),
]

for root in possible_bootcamp_roots:
    if root.exists() and str(root) not in sys.path:
        sys.path.insert(0, str(root))

from members.Quaandang183.w1.grades import summary
from members.Quaandang183.w1.rules import can_register_thesis, missing
from members.Quaandang183.w1.text_tools import top_k, word_count
from members.Quaandang183.w1.timetable import by_day
from members.Quaandang183.w1.translate import binary_search


# ==============================================================================
# 1. Test W1-1: Grade summary (grades.py)
# ==============================================================================
def test_grades_summary_standard():
    """Kiểm tra hàm summary với danh sách điểm số thông thường."""
    scores = [7.0, 8.5, 9.0, 6.5, 10.0]
    result = summary(scores)
    assert result["min"] == 6.5
    assert result["max"] == 10.0
    assert result["mean"] == 8.2
    assert result["median"] == 8.5


# ==============================================================================
# 2. Test W1-2: Word counter & Top K (text_tools.py)
# ==============================================================================
def test_text_tools_word_count_and_top_k():
    """Kiểm tra word_count và top_k khi văn bản có dấu câu và chữ hoa thường."""
    text = "Python is great! Python is fast, and Python is easy."
    counts = word_count(text)
    assert counts["python"] == 3
    assert counts["is"] == 3
    assert counts["fast"] == 1

    top2 = top_k(text, 2)
    assert top2 == [("is", 3), ("python", 3)]


# ==============================================================================
# 3. Test W1-3: Thesis eligibility (rules.py)
# ==============================================================================
def test_rules_thesis_eligibility():
    """Kiểm tra điều kiện làm khóa luận (credits >= 120, gpa >= 2.0) và lý do thiếu."""
    assert can_register_thesis(120, 2.0) is True
    assert missing(120, 2.0) == []

    assert can_register_thesis(110, 1.8) is False
    reasons = missing(110, 1.8)
    assert len(reasons) == 2
    assert any("need 10 more credits" in r for r in reasons)
    assert any("1.8" in r for r in reasons)


# ==============================================================================
# 4. Test W1-5: Timetable grouping (timetable.py)
# ==============================================================================
def test_timetable_by_day_sorting():
    """Kiểm tra gom nhóm môn học theo ngày và sắp xếp bảng chữ cái các môn trong ngày."""
    data = [
        ("Web Development", "Mon"),
        ("Database Systems", "Tue"),
        ("Algorithms", "Mon"),
        ("Machine Learning", "Tue"),
    ]
    res = by_day(data)
    assert res["Mon"] == ["Algorithms", "Web Development"]
    assert res["Tue"] == ["Database Systems", "Machine Learning"]


# ==============================================================================
# 5. Test W1-4: Binary search (translate.py - TV 1 của Quân)
# ==============================================================================
def test_translate_binary_search_positions():
    """Kiểm tra tìm kiếm nhị phân tại các vị trí đầu, giữa, cuối của mảng có thứ tự."""
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    assert binary_search(arr, 2) == 0
    assert binary_search(arr, 91) == 9
    assert binary_search(arr, 16) == 4
    assert binary_search(arr, 15) == -1


# ==============================================================================
# 6. EDGE CASES (Trường hợp biên mà test của giảng viên chưa đề cập)
# ==============================================================================
def test_edge_case_binary_search_special():
    """EDGE CASE 1: Tìm kiếm nhị phân với mảng chỉ có 1 phần tử và mảng chứa số âm."""
    assert binary_search([42], 42) == 0
    assert binary_search([42], 100) == -1

    negative_arr = [-50, -20, -5, 0, 7, 15]
    assert binary_search(negative_arr, -20) == 1
    assert binary_search(negative_arr, 0) == 3
    assert binary_search(negative_arr, -99) == -1


def test_edge_case_text_tools_all_punctuations_and_k_overflow():
    """EDGE CASE 2: Chuỗi chỉ chứa toàn dấu câu / khoảng trắng và k lớn hơn số từ."""
    punct_only = "... ,,, ??? !!! ::: ;;;   "
    assert word_count(punct_only) == {}
    assert top_k(punct_only, 5) == []

    simple_text = "hello world"
    assert len(top_k(simple_text, 100)) == 2


def test_edge_case_grades_identical_values():
    """EDGE CASE 3: Tất cả các điểm số trong danh sách đều giống hệt nhau."""
    same_scores = [8.0, 8.0, 8.0, 8.0]
    res = summary(same_scores)
    assert res["min"] == 8.0
    assert res["max"] == 8.0
    assert res["mean"] == 8.0
    assert res["median"] == 8.0


def test_edge_case_rules_exact_boundary():
    """EDGE CASE 4: Điểm biên sát nút (119 tín chỉ hoặc 1.99 GPA)."""
    assert can_register_thesis(119, 4.0) is False
    assert missing(119, 4.0) == ["need 1 more credits"]

    assert can_register_thesis(120, 1.99) is False
    assert len(missing(120, 1.99)) == 1
