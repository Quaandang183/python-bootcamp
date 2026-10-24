from shared.contract import Task, Block

def allocate(tasks: list[Task], hours: float) -> list[Block]:
    remaining_hours = hours
    allocated_blocks: list[Block] = []

    for task in tasks:
        if remaining_hours <= 0:
            break
        allocated_time = min(task.effort_h, remaining_hours)
        
        if allocated_time > 0:
            allocated_blocks.append(Block(task=task, hours=allocated_time))
            remaining_hours -= allocated_time

    return allocated_blocks