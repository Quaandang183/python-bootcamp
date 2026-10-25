"""Student grades analysis utilities."""

import statistics


def grade_sum(score):
    """Tính các thông số thống kê (min, max, mean, median) từ danh sách điểm."""
    try :
        if not score:
            raise ValueError("Danh sách điểm số không được để trống!")
        

        result = {
            "min": round(min(score),2),
            "max": round (max (score),2),
            "mean": round (sum(score)/ len(score) , 2),
            "median": round(statistics.median(score),2),
        }

        return result
    
    except ValueError as e :
       print(f"lôi{e}")
       raise

scores_list = [8.5, 9.0, 7.5, 6.0, 8.0]
print("Kết quả:", grade_sum(scores_list))