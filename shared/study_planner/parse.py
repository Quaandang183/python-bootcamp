import csv
from datetime import datetime
from shared.contract import Task

def parse_csv(path: str) -> list[Task]:
    tasks = []
    
    with open(path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        # Skip header row
        next(reader, None)
        
        # Start counting at line 2 because line 1 is the header
        for line_num, row in enumerate(reader, start=2):
            if not row:
                continue
                
            try:
                title = row[0].strip()
                importance = int(row[1].strip())
                effort_h = float(row[2].strip())
                deadline = datetime.strptime(row[3].strip(), "%Y-%m-%d").date()
                
                tasks.append(Task(
                    title=title,
                    importance=importance,
                    effort_h=effort_h,
                    deadline=deadline
                ))
            except (IndexError, ValueError) as e:
                # Raise ValueError with the exact line number on failure
                raise ValueError(f"Invalid data at line {line_num}: {e}") from e
                
    return tasks
