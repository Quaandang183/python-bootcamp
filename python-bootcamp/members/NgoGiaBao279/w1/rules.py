def can_register_thesis(credits, gpa):
    return credits >= 120 and gpa >= 2.0


def missing(credits, gpa):
    reasons = []

    if credits < 120 and gpa < 2.0:
        reasons.append(
            f"Bạn cần hoàn thành thêm {120 - credits} tín chỉ và nâng GPA lên ít nhất 2.0 để đủ điều kiện đăng ký luận văn."
        )
    elif credits < 120:
        reasons.append(
            f"Bạn cần hoàn thành thêm {120 - credits} tín chỉ để đủ điều kiện đăng ký luận văn."
        )
    elif gpa < 2.0:
        reasons.append("Bạn cần nâng GPA lên ít nhất 2.0 để đủ điều kiện đăng ký luận văn.")

    return reasons


if __name__ == "__main__":
    test_credits = 115
    test_gpa = 1.9
    print("Có đủ điều kiện đăng ký khóa luận không?:", can_register_thesis(test_credits, test_gpa))
    print("Các lý do chưa đạt:", missing(test_credits, test_gpa))
