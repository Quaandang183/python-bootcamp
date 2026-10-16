import csv
from datetime import date
from shared.contract import Task

def parse_csv(path: str) -> list[Task]:
    """
    Đọc file CSV và trả về danh sách các đối tượng Task.
    Nếu dòng dữ liệu không hợp lệ, phát sinh ValueError kèm số dòng.
    """
    tasks = []
    
    with open(path, mode='r', encoding='utf-8') as f:
        # DictReader tự động đọc dòng đầu tiên làm header
        reader = csv.DictReader(f)
        
        # Bắt đầu từ dòng 2 (vì dòng 1 là header)
        line_num = 2 
        
        for row in reader:
            try:
                # Trích xuất và ép kiểu dữ liệu
                title = row['title'].strip()
                importance = int(row['importance'].strip())
                effort_h = float(row['effort_h'].strip())
                deadline = date.fromisoformat(row['deadline'].strip())
                
                # Khởi tạo đối tượng Task và đẩy vào mảng
                task = Task(title=title, importance=importance, effort_h=effort_h, deadline=deadline)
                tasks.append(task)
                
            except (ValueError, KeyError) as e:
                # Phát sinh lỗi ValueError theo yêu cầu, báo chính xác dòng bị lỗi
                raise ValueError(f"Dữ liệu không hợp lệ tại dòng {line_num}: {e}")
            
            line_num += 1
            
    return tasks