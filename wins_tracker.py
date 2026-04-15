"""
Tracks wins logged via 'Win: [description]' messages.
Storage is a local CSV file (wins.csv) — simple, zero-dependency, portable.

CSV columns:
  timestamp     — ISO-8601 datetime string (e.g. 2026-04-14T15:30:00.123456)
  phone_number  — Sender's WhatsApp number (e.g. whatsapp:+16314082331)
  description   — The win description the user typed
"""

import csv
import os
from datetime import datetime, date

WINS_FILE = "wins.csv"
FIELDNAMES = ["timestamp", "phone_number", "description"]


def _ensure_file() -> None:
    """Create the CSV file with a header row if it doesn't already exist."""
    if not os.path.exists(WINS_FILE):
        with open(WINS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def save_win(phone_number: str, description: str) -> None:
    """
    Append a single win to the CSV.

    Args:
        phone_number: The sender's WhatsApp number (e.g. 'whatsapp:+16314082331').
        description:  The win text the user provided after 'Win: '.
    """
    _ensure_file()
    with open(WINS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(
            {
                "timestamp": datetime.now().isoformat(),
                "phone_number": phone_number,
                "description": description,
            }
        )


def get_todays_wins(phone_number: str) -> list[str]:
    """
    Return a list of win descriptions logged today for a given phone number.

    Filters by:
      - Today's date (first 10 chars of the ISO timestamp match YYYY-MM-DD).
      - The provided phone_number.

    Args:
        phone_number: WhatsApp number to filter by.

    Returns:
        A list of win description strings (may be empty).
    """
    _ensure_file()
    today = date.today().isoformat()  # e.g. "2026-04-14"
    wins: list[str] = []

    with open(WINS_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_date = row["timestamp"][:10]  # YYYY-MM-DD portion
            if row_date == today and row["phone_number"] == phone_number:
                wins.append(row["description"])

    return wins


def get_all_wins(phone_number: str) -> list[dict]:
    """
    Return every logged win for a given phone number (across all dates).
    Useful for future features like weekly/monthly summaries.

    Returns:
        List of dicts with keys: timestamp, phone_number, description.
    """
    _ensure_file()
    wins: list[dict] = []

    with open(WINS_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["phone_number"] == phone_number:
                wins.append(dict(row))

    return wins
