import statistics


def grade_summary(scores: list) -> dict:
  """Nhận vào một list điểm số, trả về dictionary chứa min, max, mean, median (làm tròn 2 chữ số thập phân)."""
  if not scores:
    raise ValueError("List điểm số không được để trống.")

  min_val = round(min(scores), 2)
  max_val = round(max(scores), 2)
  mean_val = round(sum(scores) / len(scores), 2)
  median_val = round(statistics.median(scores), 2)

  return {
      "min": min_val,
      "max": max_val,
      "mean": mean_val,
      "median": median_val,
  }