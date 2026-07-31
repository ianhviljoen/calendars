#!/usr/bin/env python3
from datetime import date, timedelta

CH = "\u265F"

OLY_VENUE = "Silk Road International Exhibition Centre"
OLY_STREET = "Silk Road Samarkand, Samarqand 140100, Uzbekistan"
OLY_LAT, OLY_LON = 39.658180, 67.063452

# FIDE schedule released 20 April 2026
OLYMPIAD = [
    (date(2026, 9, 15), "Opening Ceremony, Media Day & Technical Meeting"),
    (date(2026, 9, 16), "Round 1"),
    (date(2026, 9, 17), "Round 2"),
    (date(2026, 9, 18), "Round 3"),
    (date(2026, 9, 19), "Round 4"),
    (date(2026, 9, 20), "Round 5"),
    (date(2026, 9, 21), "Round 6"),
    (date(2026, 9, 22), "REST DAY - no play"),
    (date(2026, 9, 23), "Round 7"),
    (date(2026, 9, 24), "Round 8"),
    (date(2026, 9, 25), "Round 9"),
    (date(2026, 9, 26), "Round 10"),
    (date(2026, 9, 27), "Round 11 & Closing Ceremony"),
]

OLY_NOTES = (
    "46th Chess Olympiad, Samarkand, Uzbekistan.\n"
    "\n"
    "Around 200 teams across the Open and Women's sections, 11 rounds on the "
    "Swiss system over 14 days. India defend the titles they won in Budapest "
    "in 2024, taking gold in both sections.\n"
    "\n"
    "Watch for Javokhir Sindarov on home soil - he plays here for Uzbekistan "
    "two months before challenging Gukesh for the world title, and Gukesh is "
    "expected to play for India.\n"
    "\n"
    "Round start times were not in FIDE's published schedule, so these are "
    "all-day entries. Samarkand is UTC+5."
)

WCC_NOTES = (
    "FIDE World Chess Championship 2026\n"
    "Gukesh Dommaraju (India, defending champion) v Javokhir Sindarov "
    "(Uzbekistan, challenger).\n"
    "\n"
    "The youngest world championship match in history - both players are 20. "
    "Sindarov won the 2026 Candidates in Cyprus with 10/14, unbeaten, "
    "clinching it with a round to spare. He is also the youngest ever World "
    "Cup winner.\n"
    "\n"
    "Minimum prize fund USD 2.5 million; total event budget around USD 8.5 "
    "million.\n"
    "\n"
    "TWO THINGS UNCONFIRMED:\n"
    "1. HOST CITY. FIDE opened bidding with a deadline of 31 May 2026 and had "
    "not announced a winner at the time this calendar was built. India and "
    "Uzbekistan are the obvious candidates; Sindarov has said he would prefer "
    "somewhere warm, like Cyprus.\n"
    "2. GAME SCHEDULE. Which days are games and which are rest days has not "
    "been published, so this is the full 25-day window."
)

RB_NOTES = (
    "PROVISIONAL ENTRY - dates and host NOT yet announced by FIDE.\n"
    "\n"
    "The individual FIDE World Rapid and Blitz Championships have been held "
    "in the last week of December in recent years - the 2025 edition ran "
    "26-30 December in Doha, Qatar, where Magnus Carlsen took a sixth rapid "
    "title and Aleksandra Goryachkina won the women's rapid.\n"
    "\n"
    "This entry is a placeholder on that customary window so the slot is "
    "blocked out. Replace it once FIDE confirms the 2026 host and dates.\n"
    "\n"
    "Note this is the INDIVIDUAL championship, not the team event - the World "
    "Team Rapid and Blitz Championships were held in Hong Kong in June 2026, "
    "won by Dragon Chilling in both formats."
)


def esc(t):
    return (t.replace("\\", "\\\\").replace(";", "\\;")
             .replace(",", "\\,").replace("\n", "\\n"))


def fold(line):
    out, cur = [], ""
    for ch in line:
        if len(cur.encode("utf-8")) + len(ch.encode("utf-8")) > 73:
            out.append(cur)
            cur = " "
        cur += ch
    out.append(cur)
    return "\r\n".join(out)


lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0",
    "PRODID:-//Claude//FIDE Chess 2026//EN", "CALSCALE:GREGORIAN",
    f"X-WR-CALNAME:{CH} FIDE Chess - Upcoming",
    fold("X-WR-CALDESC:" + esc(
        "46th Chess Olympiad, the Gukesh v Sindarov World Championship match, "
        "and the World Rapid & Blitz Championships.")),
    "X-WR-TIMEZONE:UTC",
]
stamp = "20260728T090000Z"
n = 0


def emit(uid, summary, start, end_excl, desc, loc, street, geo, cat):
    global n
    body = [
        "BEGIN:VEVENT", f"UID:{uid}@claude-chess-cal", f"DTSTAMP:{stamp}",
        f"DTSTART;VALUE=DATE:{start.strftime('%Y%m%d')}",
        f"DTEND;VALUE=DATE:{end_excl.strftime('%Y%m%d')}",
        fold("SUMMARY:" + esc(summary)),
    ]
    if loc:
        body.append(fold("LOCATION:" + esc(f"{loc}, {street}")))
    if geo:
        body += [f"GEO:{geo[0]};{geo[1]}",
                 fold(f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;'
                      f'X-ADDRESS="{street}";X-APPLE-RADIUS=200;'
                      f'X-TITLE="{loc}":geo:{geo[0]},{geo[1]}')]
    body += [
        fold("DESCRIPTION:" + esc(desc)),
        fold("CATEGORIES:" + esc("Chess") + "," + esc(cat)),
        "URL:https://www.fide.com/", "TRANSP:TRANSPARENT",
        "STATUS:CONFIRMED", "END:VEVENT",
    ]
    lines.extend(body)
    n += 1


# --- Olympiad: one entry per day, labelled with FIDE's round schedule ---
for i, (day, label) in enumerate(OLYMPIAD):
    desc = (f"46th Chess Olympiad\n{label}\n{day.strftime('%A %-d %B %Y')}\n"
            f"\nDay {i+1} of {len(OLYMPIAD)}\n"
            f"Venue: {OLY_VENUE}\nAddress: {OLY_STREET}\n"
            f"Dates: Tue 15 Sep - Sun 27 Sep 2026\n\nNotes\n{OLY_NOTES}")
    emit(f"olympiad-2026-d{i+1}", f"{CH} Chess Olympiad - {label}",
         day, day + timedelta(days=1), desc, OLY_VENUE, OLY_STREET,
         (OLY_LAT, OLY_LON), "Chess Olympiad")

# --- World Championship match: full 25-day window ---
wcc_start, wcc_end = date(2026, 11, 23), date(2026, 12, 17)
total = (wcc_end - wcc_start).days + 1
for i in range(total):
    day = wcc_start + timedelta(days=i)
    if i == 0:
        tag = "Match begins"
    elif i == total - 1:
        tag = "Final scheduled day"
    else:
        tag = f"Day {i+1} of {total}"
    desc = (f"World Chess Championship 2026 - Gukesh v Sindarov\n{tag}\n"
            f"{day.strftime('%A %-d %B %Y')}\n"
            f"\nMatch window: Mon 23 Nov - Thu 17 Dec 2026\n"
            f"Host city: TO BE CONFIRMED\n\nNotes\n{WCC_NOTES}")
    emit(f"wcc-2026-d{i+1}", f"{CH} World Chess Championship - {tag}",
         day, day + timedelta(days=1), desc, "", "", None,
         "World Championship")

# --- World Rapid & Blitz: single provisional block ---
emit("world-rapid-blitz-2026",
     f"{CH} World Rapid & Blitz Championships (PROVISIONAL)",
     date(2026, 12, 26), date(2027, 1, 1),
     f"FIDE World Rapid and Blitz Championships 2026\n"
     f"Provisional window: Sat 26 Dec 2026 - Thu 31 Dec 2026\n"
     f"Host: TO BE CONFIRMED\n\nNotes\n{RB_NOTES}",
     "", "", None, "World Rapid & Blitz")

lines.append("END:VCALENDAR")
with open("../docs/fide-chess.ics", "w",
          encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print(f"Wrote {n} events.")
