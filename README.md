# RecruitmentResilienceHQ — WhatsApp Motivational Bot

A personal WhatsApp bot that sends personalized pep talks, motivational quotes, and tracks daily wins during Shivani's recruitment journey.

---

## Project Structure

```
RecruitementResilienceHQ/
├── app.py            # Flask app + Twilio webhook + APScheduler
├── pep_talks.py      # 10 personalized pep talks based on your background
├── quotes.py         # 30 motivational quotes with varied intros/outros
├── wins_tracker.py   # CSV-based win logging + retrieval
├── requirements.txt
├── .env.example      # Template — copy to .env and fill in your values
├── .gitignore
└── wins.csv          # Auto-created on first 'Win:' message
```

---

## Setup (one-time)

### 1. Python environment

```bash
cd ~/Desktop/RecruitementResilienceHQ
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Twilio Sandbox

1. Sign up at [twilio.com](https://www.twilio.com) (free trial is fine).
2. Go to **Messaging → Try it out → Send a WhatsApp message**.
3. Follow the sandbox join instructions — send the join code from your WhatsApp to `+1 415 523 8886`.
4. Copy your **Account SID** and **Auth Token** from the Twilio console dashboard.

### 3. Environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
YOUR_WHATSAPP_NUMBER=whatsapp:+1XXXXXXXXXX   ← your real number
EOD_HOUR=18
EOD_MINUTE=0
```

### 4. Expose your local server with ngrok

Twilio needs a public URL to call your webhook. ngrok creates a temporary tunnel:

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 5000
```

Copy the `https://xxxx.ngrok-free.app` URL it gives you.

### 5. Set the Twilio webhook URL

In the Twilio console:

1. Go to **Messaging → Try it out → Send a WhatsApp message**.
2. In the **Sandbox settings** section, set:
   - **When a message comes in** → `https://xxxx.ngrok-free.app/webhook`
   - Method: `HTTP POST`
3. Save.

### 6. Run the bot

```bash
source venv/bin/activate
python app.py
```

---

## Usage

Send any of these messages from your WhatsApp to the Twilio sandbox number (`+1 415 523 8886`):

| Message | Response |
|---|---|
| `PepTalk` | Personalized pep talk drawn from your background |
| `Motivation` | Random motivational quote |
| `Win: Got a callback from Stripe!` | Logs the win + confirms |
| Anything else | Help menu |

**End-of-day summary:** At 6 PM Pacific Time, the bot proactively sends a recap of every win you logged that day (or an encouraging message if none were logged).

---

## Customizing the EOD time

Change `EOD_HOUR` and `EOD_MINUTE` in your `.env`:

```
EOD_HOUR=17    # 5 PM
EOD_MINUTE=30  # :30
```

Timezone is fixed to `America/Los_Angeles` (Stanford/SF). To change it, edit the `_start_scheduler()` function in `app.py`.

---

## Adding more pep talks or quotes

- **Pep talks:** Add a new string to the `PEP_TALKS` list in `pep_talks.py`.
- **Quotes:** Add a new string to the `QUOTES` list in `quotes.py`.

No other changes needed — `random.choice()` handles the rest.

---

## Key dependencies

| Package | Version | Purpose |
|---|---|---|
| Flask | 3.0.3 | Web framework / webhook server |
| twilio | 9.3.0 | WhatsApp API client + TwiML helpers |
| python-dotenv | 1.0.1 | Load `.env` variables |
| APScheduler | 3.10.4 | Background scheduler for EOD summary |
