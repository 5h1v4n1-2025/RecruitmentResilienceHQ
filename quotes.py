"""
Motivational quotes for the 'Motivation' keyword.
Each quote is returned with a warm, varied intro so repeated requests
don't feel robotic.
"""

import random

QUOTES = [
    "\"The most common way people give up their power is by thinking they don't have any.\" — Alice Walker",
    "\"It always seems impossible until it's done.\" — Nelson Mandela",
    "\"You didn't come this far to only come this far.\" — Unknown",
    "\"Success is not final, failure is not fatal: it is the courage to continue that counts.\" — Winston Churchill",
    "\"The comeback is always stronger than the setback.\" — Unknown",
    "\"Believe you can and you're halfway there.\" — Theodore Roosevelt",
    "\"What you get by achieving your goals is not as important as what you become by achieving your goals.\" — Zig Ziglar",
    "\"Hardships often prepare ordinary people for an extraordinary destiny.\" — C.S. Lewis",
    "\"You are braver than you believe, stronger than you seem, and smarter than you think.\" — A.A. Milne",
    "\"Don't watch the clock; do what it does. Keep going.\" — Sam Levenson",
    "\"The secret of getting ahead is getting started.\" — Mark Twain",
    "\"It's not whether you get knocked down, it's whether you get up.\" — Vince Lombardi",
    "\"Every strike brings me closer to the next home run.\" — Babe Ruth",
    "\"Perseverance is not a long race; it is many short races one after the other.\" — Walter Elliot",
    "\"Fall seven times, stand up eight.\" — Japanese Proverb",
    "\"The harder the battle, the sweeter the victory.\" — Les Brown",
    "\"Great things never come from comfort zones.\" — Unknown",
    "\"In the middle of every difficulty lies opportunity.\" — Albert Einstein",
    "\"Tough times never last, but tough people do.\" — Dr. Robert H. Schuller",
    "\"Rejection is redirection.\" — Unknown",
    "\"Keep going. Everything you need will come to you at the perfect time.\" — Unknown",
    "\"You are enough. You have enough. You do enough.\" — Brené Brown",
    "\"The key to success is to start before you are ready.\" — Marie Forleo",
    "\"Small steps in the right direction can turn out to be the biggest step of your life.\" — Unknown",
    "\"Our greatest glory is not in never falling, but in rising every time we fall.\" — Confucius",
    "\"The only way to achieve the impossible is to believe it is possible.\" — Charles Kingsleigh",
    "\"You don't have to be perfect to be amazing.\" — Unknown",
    "\"Act as if what you do makes a difference. It does.\" — William James",
    "\"With the new day comes new strength and new thoughts.\" — Eleanor Roosevelt",
    "\"Start where you are. Use what you have. Do what you can.\" — Arthur Ashe",
]

INTROS = [
    "Here's something worth sitting with today:\n\n",
    "A little wisdom for the road:\n\n",
    "Your quote for today:\n\n",
    "This one's for you, Shivani:\n\n",
    "Pin this one up:\n\n",
    "Carry this with you today:\n\n",
]

OUTROS = [
    "\n\nYou've got this. 💙",
    "\n\nNow go make something happen. 🔥",
    "\n\nKeep going. 🚀",
    "\n\nBelieve it. 🌟",
    "\n\nThe search is a season, not a sentence. 💪",
]


def get_motivational_quote() -> str:
    """Return a random motivational quote with a warm intro and outro."""
    return random.choice(INTROS) + random.choice(QUOTES) + random.choice(OUTROS)
