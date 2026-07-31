#!/usr/bin/env python3
from datetime import date, timedelta

DART = "\U0001F3AF"

TOURNAMENTS = [
    dict(slug="world-grand-prix", name="World Grand Prix",
         start=date(2026, 9, 28), end=date(2026, 10, 4),
         venue="Mattioli Arena",
         street="12 Memory Ln, Leicester LE1 3UL, UK",
         lat=52.643982, lon=-1.131009,
         purse="GBP 750,000 (winner GBP 150,000)",
         field="32 players - top 16 Order of Merit plus 16 ProTour qualifiers",
         tv="Sky Sports (UK) / DAZN, PDCTV and other international partners",
         notes="29th staging. The only event on the PDC circuit played "
               "DOUBLE IN, DOUBLE OUT - players must start a leg on a double "
               "or the bullseye as well as finish on one, which makes for very "
               "different scoring patterns. Set format throughout, getting "
               "longer as the tournament progresses. Luke Littler is defending "
               "champion after beating Luke Humphries 6-1 in the 2025 final. "
               "Prize fund is up from GBP 600,000."),
    dict(slug="grand-slam", name="Grand Slam of Darts",
         start=date(2026, 11, 14), end=date(2026, 11, 22),
         venue="WV Active Aldersley (Aldersley Leisure Village)",
         street="Aldersley Rd, Wolverhampton WV6 9NW, UK",
         lat=52.605753, lon=-2.150396,
         purse="GBP 650,000 approx. (2025 figure - 2026 TBC)",
         field="32 players in a group stage, then knockout",
         tv="Sky Sports (UK) / PDCTV and international partners",
         notes="20th staging. The only PDC major with a GROUP STAGE - four "
               "round-robin groups feed a straight knockout, so the opening "
               "days carry several matches each. Historically brought together "
               "PDC and BDO/WDF qualifiers. Luke Littler is defending champion."),
    dict(slug="world-championship", name="World Darts Championship",
         start=date(2026, 12, 10), end=date(2027, 1, 3),
         venue="Alexandra Palace",
         street="Alexandra Palace Way, London N22 7AY, UK",
         lat=51.594238, lon=-0.130811,
         purse="GBP 5,000,000 approx. (winner GBP 1,000,000 in 2025/26)",
         field="128 players, top 32 on the Order of Merit seeded",
         tv="Sky Sports (UK) / PDCTV and international partners",
         notes="The 34th PDC World Championship and the 20th at Alexandra "
               "Palace - but the FIRST in the venue's Great Hall, having "
               "outgrown the West Hall. Set format, final is first to 7 sets. "
               "Luke Littler is defending champion. Note the PDC traditionally "
               "pauses play over Christmas, so expect rest days around "
               "24-26 December - confirm against the schedule of play."),
]


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
    "PRODID:-//Claude//PDC Darts 2026//EN", "CALSCALE:GREGORIAN",
    f"X-WR-CALNAME:{DART} PDC Darts - Upcoming Majors",
    fold("X-WR-CALDESC:" + esc(
        "World Grand Prix, Grand Slam of Darts and the World Darts "
        "Championship.")),
    "X-WR-TIMEZONE:Europe/London",
]
stamp = "20260728T090000Z"
count = 0

for ev in TOURNAMENTS:
    total = (ev["end"] - ev["start"]).days + 1
    window = (f"{ev['start'].strftime('%a %-d %b')} - "
              f"{ev['end'].strftime('%a %-d %b %Y')}")
    for i in range(total):
        day = ev["start"] + timedelta(days=i)
        if i == 0:
            label = f"Day 1 of {total} - opening day"
        elif i == total - 1:
            label = f"Day {total} of {total} - FINALS DAY"
        else:
            label = f"Day {i + 1} of {total}"
        desc = (
            f"{ev['name']}\n{label}\n{day.strftime('%A %-d %B %Y')}\n"
            f"\n"
            f"Session times\n"
            f"NOT YET PUBLISHED. The PDC releases its schedule of play "
            f"(afternoon/evening session start times and the order of matches) "
            f"a few weeks before each major, so this is an all-day entry for "
            f"now.\n"
            f"\n"
            f"Venue: {ev['venue']}\n"
            f"Address: {ev['street']}\n"
            f"Tournament dates: {window}\n"
            f"Field: {ev['field']}\n"
            f"Prize fund: {ev['purse']}\n"
            f"\n"
            f"TV\n"
            f"{ev['tv']}\n"
            f"\n"
            f"Notes\n"
            f"{ev['notes']}"
        )
        lines += [
            "BEGIN:VEVENT",
            f"UID:{ev['slug']}-d{i+1}@claude-darts-cal",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{day.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(day + timedelta(days=1)).strftime('%Y%m%d')}",
            fold("SUMMARY:" + esc(f"{DART} {ev['name']}")),
            fold("LOCATION:" + esc(f"{ev['venue']}, {ev['street']}")),
            f"GEO:{ev['lat']};{ev['lon']}",
            fold(f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;'
                 f'X-ADDRESS="{ev["street"]}";X-APPLE-RADIUS=150;'
                 f'X-TITLE="{ev["venue"]}":geo:{ev["lat"]},{ev["lon"]}'),
            fold("DESCRIPTION:" + esc(desc)),
            fold("CATEGORIES:" + esc("Darts") + "," + esc("PDC Major")),
            "URL:https://www.pdc.tv/calendar/",
            "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
        ]
        count += 1

lines.append("END:VCALENDAR")
with open("../docs/pdc-darts-2026.ics", "w",
          encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print(f"Wrote {count} days across {len(TOURNAMENTS)} tournaments.")
