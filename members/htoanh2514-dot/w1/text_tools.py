import re
from collections import Counter


def word_count(text: str) -> Counter:
  """Đếm tần suất xuất hiện của từ (bỏ qua dấu câu, không phân biệt hoa thường)."""
  # Chuyển về chữ thường
  text = text.lower()
  # Loại bỏ dấu câu cơ bản (, . ! ? ; :)
  text = re.sub(r"[,.!?;:]", "", text)
  # Tách từ theo khoảng trắng
  words = text.split()
  # Dùng Counter để đếm
  return Counter(words)


def top_k(text: str, k: int) -> list:
  """Lấy K từ xuất hiện nhiều nhất.

  Sắp xếp giảm dần theo số lượng, nếu bằng nhau thì sắp xếp theo bảng chữ cái
  (tăng dần).
  """
  counter = word_count(text)
  sorted_words = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
  return [word for word, count in sorted_words[:k]]