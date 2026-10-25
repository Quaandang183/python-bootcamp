from datetime import date, datetime, timedelta

WEEKDAYS = {
    "mon": 0, "tue": 1, "wed": 2, "thu": 3,
    "fri": 4, "sat": 5, "sun": 6
}

def parse_due(text: str, today: date) -> date:
    text_clean = text.strip().lower()
    
    # 1. Định dạng YYYY-MM-DD
    try:
        return datetime.strptime(text_clean, "%Y-%m-%d").date()
    except ValueError:
        pass
    
    # 2. Định dạng "tomorrow"
    if text_clean == "tomorrow":
        return today + timedelta(days=1)
    
    # 3. Định dạng "in N days"
    if text_clean.startswith("in ") and text_clean.endswith(" days"):
        parts = text_clean.split()
        if len(parts) == 3 and parts[1].isdigit():
            n_days = int(parts[1])
            return today + timedelta(days=n_days)
            
    if text_clean[:3] in WEEKDAYS:
        target_weekday = WEEKDAYS[text_clean[:3]]
        current_weekday = today.weekday()
        days_ahead = (target_weekday - current_weekday) % 7
        if days_ahead == 0:
            days_ahead = 7 
        return today + timedelta(days=days_ahead)

    raise ValueError(f"Unknown date text format: {text}")