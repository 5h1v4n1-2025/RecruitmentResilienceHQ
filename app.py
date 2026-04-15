"""
RecruitmentResilienceHQ — WhatsApp Motivational Bot
====================================================
A Flask + Twilio WhatsApp bot for Shivani Bajaj's recruitment journey.

Supported keywords (case-insensitive):
  PepTalk          → Personalized pep talk drawn from her background
  Motivation       → Random motivational quote
  Win: <text>      → Log a win; end-of-day summary sent at 6 PM PT

Environment variables required (see .env.example):
  TWILIO_ACCOUNT_SID      Your Twilio Account SID
  TWILIO_AUTH_TOKEN       Your Twilio Auth Token
  TWILIO_WHATSAPP_NUMBER  Twilio sandbox number (default: whatsapp:+14155238886)
  YOUR_WHATSAPP_NUMBER    Your own WhatsApp number (e.g. whatsapp:+16314082331)
  EOD_HOUR                Hour (24h, Pacific Time) to send EOD summary (default: 18)
  EOD_MINUTE              Minute for EOD summary (default: 0)
"""

import os
import logging

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from pep_talks import get_pep_talk
from quotes import get_motivational_quote
from wins_tracker import save_win, get_todays_wins

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

load_dotenv()  # Load variables from .env file into os.environ

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Twilio client — used for proactive EOD summary messages
# ---------------------------------------------------------------------------

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
YOUR_WHATSAPP_NUMBER = os.environ["YOUR_WHATSAPP_NUMBER"]  # e.g. whatsapp:+16314082331

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ---------------------------------------------------------------------------
# Webhook — Twilio calls this URL whenever you send a WhatsApp message
# ---------------------------------------------------------------------------

HELP_TEXT = (
    "Hey Shivani! I'm your RecruitmentResilienceHQ bot. Here's what I can do:\n\n"
    "💪 *PepTalk* — Get a personalized pep talk\n"
    "✨ *Motivation* — Get an inspirational quote\n"
    "🏆 *Win: [description]* — Log a win (e.g. *Win: Got a callback from Google!*)\n\n"
    "I'll also send you a wins recap at the end of the day. You've got this! 🚀"
)


@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Twilio calls this endpoint with a POST request every time a WhatsApp
    message is sent to the sandbox number.

    Required Twilio form fields:
      Body  — The message text
      From  — The sender's WhatsApp number
    """
    incoming_msg: str = request.values.get("Body", "").strip()
    sender: str = request.values.get("From", "")

    logger.info("Incoming message from %s: %r", sender, incoming_msg)

    # MessagingResponse is the Twilio helper that builds the TwiML XML reply
    resp = MessagingResponse()
    msg = resp.message()

    reply = _route_message(incoming_msg, sender)
    msg.body(reply)

    logger.info("Replying: %r", reply[:80])
    return str(resp)


def _route_message(text: str, sender: str) -> str:
    """
    Determine the correct reply based on the message content.

    Matching rules (all case-insensitive):
      - "peptalk"       → personalized pep talk
      - "motivation"    → motivational quote
      - "win: ..."      → log the win and confirm
      - anything else   → help menu
    """
    lower = text.lower()

    if lower == "peptalk":
        return get_pep_talk()

    if lower == "motivation":
        return get_motivational_quote()

    if lower.startswith("win:"):
        description = text[4:].strip()  # Everything after "Win:"
        if not description:
            return (
                "Almost! Add a description after the colon — for example:\n"
                "*Win: Got a callback from Stripe!*"
            )
        save_win(sender, description)
        logger.info("Win saved for %s: %r", sender, description)
        return (
            f"WIN LOGGED! That's huge, Shivani! 🏆\n\n"
            f"\"{description}\"\n\n"
            f"Keep stacking those wins — I'll send you a full recap at end of day. 💪"
        )

    # Default: show the help menu
    return HELP_TEXT


# ---------------------------------------------------------------------------
# End-of-day wins summary (proactive message sent via Twilio REST API)
# ---------------------------------------------------------------------------

def send_eod_summary() -> None:
    """
    Proactively send Shivani a recap of all wins logged today.
    Called by APScheduler at the configured hour/minute (Pacific Time).
    """
    logger.info("Running end-of-day summary job.")
    wins = get_todays_wins(YOUR_WHATSAPP_NUMBER)

    if not wins:
        body = (
            "Hey Shivani — end of day check-in. 🌙\n\n"
            "No wins logged today, and that's okay. The job search is a marathon.\n\n"
            "Remember: you raised $1.5B, got promoted twice at McKinsey in one year, "
            "and bootstrapped Jugnu to a 10x return. Tomorrow is another shot. Rest up. 💙"
        )
    else:
        win_lines = "\n".join(f"  {i + 1}. {w}" for i, w in enumerate(wins))
        plural = "win" if len(wins) == 1 else "wins"
        body = (
            f"Shivani's Wins — EOD Recap 🌟\n\n"
            f"You stacked {len(wins)} {plural} today:\n\n"
            f"{win_lines}\n\n"
            f"Every win is evidence of who you are. "
            f"The right opportunity is finding its way to you. Keep going! 🚀"
        )

    try:
        twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=YOUR_WHATSAPP_NUMBER,
            body=body,
        )
        logger.info("EOD summary sent to %s.", YOUR_WHATSAPP_NUMBER)
    except Exception as e:
        logger.error("Failed to send EOD summary: %s", e)


# ---------------------------------------------------------------------------
# APScheduler setup — fires send_eod_summary daily at EOD_HOUR:EOD_MINUTE PT
# ---------------------------------------------------------------------------

def _start_scheduler() -> BackgroundScheduler:
    eod_hour = int(os.environ.get("EOD_HOUR", 18))    # 6 PM default
    eod_minute = int(os.environ.get("EOD_MINUTE", 0))

    scheduler = BackgroundScheduler(timezone="America/Los_Angeles")
    scheduler.add_job(
        send_eod_summary,
        trigger="cron",
        hour=eod_hour,
        minute=eod_minute,
        id="eod_summary",
    )
    scheduler.start()
    logger.info("Scheduler started — EOD summary will fire at %02d:%02d PT.", eod_hour, eod_minute)
    return scheduler


# Only start the scheduler when running the app directly (not during testing)
if __name__ == "__main__":
    scheduler = _start_scheduler()
    # use_reloader=False prevents APScheduler from running twice in debug mode
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port, use_reloader=False)
