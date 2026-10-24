def can_register_thesis(credits: int, gpa: float) -> bool:
  """Kiểm tra điều kiện đăng ký làm luận văn (tín chỉ >= 120 và GPA >= 2.0)."""
  return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list:
  """Xuất ra lý do bằng văn bản nếu chưa đủ điều kiện."""
  reasons = []

  if credits < 120:
    needed_credits = 120 - credits
    reasons.append(f"need {needed_credits} more credits")

  if gpa < 2.0:
    reasons.append("need higher GPA (at least 2.0)")

  return reasons