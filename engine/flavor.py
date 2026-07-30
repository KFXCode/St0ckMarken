"""Moon phase, moon zodiac sign, and date numerology.
Same 'flavor' layer as the MLB engine: clearly labeled, minor weight, never the driver."""
import math
from datetime import datetime, timezone

SYNODIC = 29.53058867
EPOCH_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)

ZODIAC = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra",
          "Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
ELEMENT = {"Aries":"fire","Leo":"fire","Sagittarius":"fire",
           "Taurus":"earth","Virgo":"earth","Capricorn":"earth",
           "Gemini":"air","Libra":"air","Aquarius":"air",
           "Cancer":"water","Scorpio":"water","Pisces":"water"}

def moon_phase(dt):
    """Return (phase_name, illumination_pct, waxing: bool)."""
    days = (dt - EPOCH_NEW_MOON).total_seconds() / 86400.0
    age = days % SYNODIC
    illum = round((1 - math.cos(2 * math.pi * age / SYNODIC)) / 2 * 100)
    waxing = age < SYNODIC / 2
    if age < 1.85: name = "New Moon"
    elif age < 5.54: name = "Waxing Crescent"
    elif age < 9.23: name = "First Quarter"
    elif age < 12.92: name = "Waxing Gibbous"
    elif age < 16.61: name = "Full Moon"
    elif age < 20.30: name = "Waning Gibbous"
    elif age < 23.99: name = "Last Quarter"
    elif age < 27.68: name = "Waning Crescent"
    else: name = "New Moon"
    return name, illum, waxing

def moon_sign(dt):
    """Low-precision moon ecliptic longitude -> zodiac sign."""
    d = (dt - datetime(2000, 1, 1, 12, tzinfo=timezone.utc)).total_seconds() / 86400.0
    lon = (218.316 + 13.176396 * d) % 360.0
    return ZODIAC[int(lon // 30)]

def numerology(dt):
    n = sum(int(c) for c in dt.strftime("%Y%m%d"))
    while n > 9 and n not in (11, 22):
        n = sum(int(c) for c in str(n))
    return n

def flavor_score(dt):
    """Return (score 0-100 where >50 leans bullish, notes list).
    Waxing moon = mild bullish bias; waning = mild bearish bias.
    Fire/air moon sign = risk-on tilt; earth/water = risk-off tilt.
    Odd numerology day = momentum bias; even = mean-reversion bias."""
    name, illum, waxing = moon_phase(dt)
    sign = moon_sign(dt)
    elem = ELEMENT[sign]
    num = numerology(dt)
    score = 50.0
    notes = []
    score += 8 if waxing else -8
    notes.append(f"{name} ({illum}% illuminated) -> {'mild bullish bias' if waxing else 'mild bearish bias'}")
    if elem in ("fire", "air"):
        score += 5; notes.append(f"Moon in {sign} ({elem} sign) -> risk-on tilt")
    else:
        score -= 5; notes.append(f"Moon in {sign} ({elem} sign) -> risk-off tilt")
    if num % 2 == 1:
        score += 3; notes.append(f"Date reduces to {num} -> momentum bias")
    else:
        score -= 3; notes.append(f"Date reduces to {num} -> mean-reversion bias")
    return max(0, min(100, score)), notes, {"phase": name, "illum": illum, "sign": sign, "numerology": num}
