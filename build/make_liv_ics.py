#!/usr/bin/env python3
from datetime import date, timedelta

TV = "FOX, FS1, FS2, Fox Business, LIV Golf app"

FORMAT_NOTE = ("2026 format: 72 holes over four days, no cut, 57-player field. "
               "Individual and team titles decided at every event.")

EVENTS = [
    dict(slug="liv-new-york", name="LIV Golf New York",
         start=date(2026, 8, 6),
         venue="Trump National Golf Club Bedminster",
         street="900 Lamington Rd, Bedminster, NJ 07921, USA",
         lat=40.653751, lon=-74.696966,
         cat="LIV Golf - Regular Season",
         notes="LIV returns to Bedminster. Round 1 coverage starts 12:00 UTC "
               "(8am ET) on Thursday 6 August. " + FORMAT_NOTE),
    dict(slug="liv-indianapolis", name="LIV Golf Indianapolis",
         start=date(2026, 8, 20),
         venue="The Club at Chatham Hills",
         street="1100 Chatham Hills Blvd, Westfield, IN 46074, USA",
         lat=40.082065, lon=-86.138633,
         cat="LIV Golf - Regular Season",
         notes="REGULAR-SEASON FINALE and the LIV Golf Individual "
               "Championship - the season's individual title is decided here, "
               "as it was in 2025. Pete Dye course. Second straight year at "
               "Chatham Hills.\n\nAlso flagged by Front Office Sports as at "
               "risk, but currently still scheduled to go ahead - and if "
               "Michigan falls, this becomes LIV's 2026 season finale. Purse "
               "expected around $30m. " + FORMAT_NOTE),
    dict(slug="liv-team-championship",
         name="Aramco LIV Golf Michigan Team Championship",
         start=date(2026, 8, 27),
         venue="The Cardinal at Saint John's",
         street="44045 Five Mile Rd, Plymouth, MI 48170, USA",
         lat=42.393536, lon=-83.478617,
         cat="LIV Golf - Team Championship",
         notes="*** EXPECTED TO BE CANCELLED - NOT YET OFFICIAL ***\n\n"
               "Status as of Wed 29 July 2026: LIV has NOT announced anything. "
               "But this is no longer one person's speculation - it was first "
               "reported by Tom Hobbs (Flushing It) and then confirmed by "
               "sources to Front Office Sports, with Golf Channel, Yahoo and "
               "others carrying it. An official announcement was expected "
               "Wednesday.\n\n"
               "Supporting signs: contractors report travel and accommodation "
               "cancelled with money still owed; the Detroit News reported no "
               "infrastructure had been built at the course; the championship "
               "rings reportedly remain unpaid for.\n\n"
               "Background: PIF announced in April it would stop funding LIV "
               "after this season, and the money has dried up sooner than "
               "expected. LIV is seeking up to $350m from new investors and "
               "is working to a 1 September deadline to fund 2027. This would "
               "be the second cancelled event of 2026 after Louisiana.\n\n"
               "As scheduled: $40m purse (down from $50m), $11.2m to the "
               "winning team, at The Cardinal at Saint John's."),
]

DAYS = ["Round 1", "Round 2", "Round 3", "Round 4 (Final Round)"]


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
    "PRODID:-//Claude//LIV Golf 2026 Upcoming Schedule//EN",
    "CALSCALE:GREGORIAN",
    "X-WR-CALNAME:\u26f3 LIV Golf 2026 - Upcoming",
    fold("X-WR-CALDESC:" + esc(
        "Remaining 2026 LIV Golf season: New York, Indianapolis and the Team "
        "Championship in Michigan.")),
    "X-WR-TIMEZONE:UTC",
]

stamp = "20260727T090000Z"
count = 0

for ev in EVENTS:
    finish = ev["start"] + timedelta(days=3)
    window = (f"{ev['start'].strftime('%a %-d %b')} - "
              f"{finish.strftime('%a %-d %b %Y')}")
    for i, label in enumerate(DAYS):
        day = ev["start"] + timedelta(days=i)
        desc = (
            f"{label} - {day.strftime('%A %-d %B %Y')}\n"
            f"\n"
            f"TV\n"
            f"{TV}\n"
            f"\n"
            f"Venue: {ev['venue']}\n"
            f"Address: {ev['street']}\n"
            f"Tournament dates: {window}\n"
            f"Purse: $25M individual + $5M team (approx.)\n"
            f"Event type: {ev['cat']}\n"
            f"\n"
            f"Notes\n"
            f"{ev['notes']}\n"
            f"\n"
            f"Tee times confirmed the week of the event - livgolf.com/schedule\n"
            f"Broadcast listings can change."
        )
        lines += [
            "BEGIN:VEVENT",
            f"UID:{ev['slug']}-2026-d{i+1}@claude-liv-cal",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{day.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(day + timedelta(days=1)).strftime('%Y%m%d')}",
            fold("SUMMARY:" + esc(f"\u26f3 {ev['name']}")),
            fold("LOCATION:" + esc(f"{ev['venue']}, {ev['street']}")),
            f"GEO:{ev['lat']};{ev['lon']}",
            fold(f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;'
                 f'X-ADDRESS="{ev["street"]}";X-APPLE-RADIUS=150;'
                 f'X-TITLE="{ev["venue"]}":geo:{ev["lat"]},{ev["lon"]}'),
            fold("DESCRIPTION:" + esc(desc)),
            fold("CATEGORIES:" + esc("LIV Golf") + "," + esc(ev["cat"])),
            "URL:https://www.livgolf.com/schedule",
            "TRANSP:TRANSPARENT",
        "STATUS:TENTATIVE" if ev["slug"] == "liv-team-championship"
        else "STATUS:CONFIRMED",
        "END:VEVENT",
        ]
        count += 1

lines.append("END:VCALENDAR")

out = "../docs/liv-golf.ics"
with open(out, "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")

print(f"Wrote {count} events across {len(EVENTS)} tournaments.")
