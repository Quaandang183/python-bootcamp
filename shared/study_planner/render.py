from contract import Block


def render(blocks: list[Block]) -> str:
    if not blocks:
        return "No study plan available."

    lines = ["=== STUDY PLAN ==="]
    total_allocated_hours = 0.0

    for idx, block in enumerate(blocks, start=1):
        task = block.task
        allocated_h = block.hours
        lines.append(
            f"{idx}. {task.name} | "
            f"Allocated: {allocated_h:.1f}h / {task.duration:.1f}h | "
            f"Importance: {task.importance}"
        )
        total_allocated_hours += allocated_h

    lines.append("-" * 32)
    lines.append(f"Total study time: {total_allocated_hours:.1f}h")

    return "\n".join(lines)