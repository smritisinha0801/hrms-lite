import re
from datetime import datetime

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def is_valid_email(email: str) -> bool:
    return bool(email and EMAIL_RE.match(email.strip()))

def parse_date(date_str: str):
    # Expect YYYY-MM-DD
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None

def require_fields(payload: dict, fields: list[str]):
    missing = [f for f in fields if not payload.get(f)]
    return missing
