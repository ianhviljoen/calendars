#!/usr/bin/env python3
from datetime import date, timedelta

M1000_TV = "Tennis Channel, Tennis Channel+, Tennis TV (ATP streaming)"
SLAM_TV = "ESPN, ESPN2, ABC (finals), ESPN+"

# (uid, title, start, end, venue, street, lat, lon, surface, draw, purse, tv,
#  category, notes)
TOURNAMENTS = [
    dict(slug="canadian-open", name="National Bank Open (Canadian Open)",
         start=date(2026, 8, 2), end=date(2026, 8, 13),
         venue="IGA Stadium",
         street="285 Rue Gary-Carter, Montreal, QC H2R 2W1, Canada",
         lat=45.533300, lon=-73.627289,
         surface="Outdoor hard", draw="96", purse="$9,415,724",
         tv=M1000_TV, cat="ATP Masters 1000",
         notes="Men's event is in Montreal this year (it alternates with "
               "Toronto). Now a 12-day format, so the final lands on a "
               "Thursday and overlaps with the start of Cincinnati."),
    dict(slug="cincinnati-open", name="Cincinnati Open",
         start=date(2026, 8, 13), end=date(2026, 8, 23),
         venue="Lindner Family Tennis Center",
         street="5460 Courseview Dr, Mason, OH 45040, USA",
         lat=39.350498, lon=-84.275102,
         surface="Outdoor hard", draw="96", purse="$9,415,725",
         tv=M1000_TV, cat="ATP Masters 1000",
         notes="Final US Open tune-up. Expanded to the 12-day format for "
               "2026."),
    dict(slug="us-open", name="US Open",
         start=date(2026, 8, 30), end=date(2026, 9, 13),
         venue="USTA Billie Jean King National Tennis Center",
         street="Flushing Meadows Corona Park, Flushing, NY 11368, USA",
         lat=40.749998, lon=-73.846996,
         surface="Outdoor hard (Laykold)", draw="128",
         purse="Record prize pool - see usopen.org",
         tv=SLAM_TV, cat="Grand Slam",
         notes="Fourth and final Grand Slam of the season. Main draw runs "
               "Aug 30 - Sep 13; Fan Week and qualifying open the grounds "
               "Aug 23-29. The only Slam with no scheduled rest day. Night "
               "sessions on Arthur Ashe start 7:00pm ET.",
         extras=[(date(2026, 9, 10), "Women's Semi-Finals"),
                 (date(2026, 9, 11), "Men's Semi-Finals"),
                 (date(2026, 9, 12), "Women's Singles Final"),
                 (date(2026, 9, 13), "Men's Singles Final")]),
    dict(slug="shanghai-masters", name="Rolex Shanghai Masters",
         start=date(2026, 10, 7), end=date(2026, 10, 18),
         venue="Qizhong Forest Sports City Arena",
         street="5500 Yuanjiang Rd, Minhang, Shanghai 201111, China",
         lat=31.039904, lon=121.359025,
         surface="Outdoor hard", draw="96", purse="$9,415,725",
         tv=M1000_TV, cat="ATP Masters 1000",
         notes="Biggest stop of the Asian swing. Shanghai is 12 hours ahead "
               "of US Eastern, so matches air overnight and early morning in "
               "the States. Venue sits well outside the city centre with "
               "limited public transport."),
    dict(slug="paris-masters", name="Rolex Paris Masters",
         start=date(2026, 11, 2), end=date(2026, 11, 8),
         venue="Paris La Defense Arena",
         street="99 Jardin de l'Arche, 92000 Nanterre, France",
         lat=48.895666, lon=2.229626,
         surface="Indoor hard", draw="56", purse="EUR 6,309,095",
         tv=M1000_TV, cat="ATP Masters 1000",
         notes="Last Masters 1000 of the season and the final chance to "
               "qualify for the ATP Finals in Turin. One-week event with a "
               "56-player draw, played indoors in Nanterre."),
    dict(slug="atp-finals", name="Nitto ATP Finals",
         start=date(2026, 11, 15), end=date(2026, 11, 22),
         venue="Inalpi Arena",
         street="Corso Sebastopoli 123, 10134 Torino TO, Italy",
         lat=45.041529, lon=7.652191,
         surface="Indoor hard", draw="8 singles / 8 doubles",
         purse="approx. $15M (2026 figure TBC)",
         tv=M1000_TV, cat="ATP Finals",
         notes="Season-ending championship for the top 8 singles players and "
               "top 8 doubles teams. Round-robin groups of four first, then "
               "knockout semi-finals and final - so every player is guaranteed "
               "three matches. Sixth consecutive year in Turin. Qualification "
               "is settled by the Paris Masters the week before.",
         extras=[(date(2026, 11, 15), "Round Robin - Day 1"),
                 (date(2026, 11, 16), "Round Robin - Day 2"),
                 (date(2026, 11, 17), "Round Robin - Day 3"),
                 (date(2026, 11, 18), "Round Robin - Day 4"),
                 (date(2026, 11, 19), "Round Robin - Day 5"),
                 (date(2026, 11, 20), "Round Robin - Day 6"),
                 (date(2026, 11, 21), "Semi-Finals"),
                 (date(2026, 11, 22), "Singles & Doubles Finals")]),
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


def d(day):
    return day.strftime("%Y%m%d")


BALL = "\U0001F3BE"
lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0",
    "PRODID:-//Claude//Tennis 2026 ATP 1000 + Slams//EN",
    "CALSCALE:GREGORIAN",
    f"X-WR-CALNAME:{BALL} Tennis 2026 - ATP 1000 & Slams",
    fold("X-WR-CALDESC:" + esc(
        "Remaining 2026 ATP Masters 1000 events and the US Open. "
        "US broadcast listings.")),
    "X-WR-TIMEZONE:UTC",
]

stamp = "20260727T090000Z"
count = 0


def emit(uid, summary, start, end_excl, ev, headline):
    """end_excl is the exclusive DTEND date."""
    global count
    desc = (
        f"{headline}\n"
        f"\n"
        f"TV\n"
        f"{ev['tv']}\n"
        f"\n"
        f"Venue: {ev['venue']}\n"
        f"Address: {ev['street']}\n"
        f"Tournament dates: {ev['start'].strftime('%a %-d %b')} - "
        f"{ev['end'].strftime('%a %-d %b %Y')}\n"
        f"Surface: {ev['surface']}\n"
        f"Singles draw: {ev['draw']}\n"
        f"Prize money: {ev['purse']}\n"
        f"Category: {ev['cat']}\n"
        f"\n"
        f"Notes\n"
        f"{ev['notes']}\n"
        f"\n"
        f"Order of play is published the evening before each day.\n"
        f"US broadcast listings can change."
    )
    lines.extend([
        "BEGIN:VEVENT",
        f"UID:{uid}@claude-tennis-cal",
        f"DTSTAMP:{stamp}",
        f"DTSTART;VALUE=DATE:{d(start)}",
        f"DTEND;VALUE=DATE:{d(end_excl)}",
        fold("SUMMARY:" + esc(summary)),
        fold("LOCATION:" + esc(f"{ev['venue']}, {ev['street']}")),
        f"GEO:{ev['lat']};{ev['lon']}",
        fold(f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;'
             f'X-ADDRESS="{ev["street"]}";X-APPLE-RADIUS=150;'
             f'X-TITLE="{ev["venue"]}":geo:{ev["lat"]},{ev["lon"]}'),
        fold("DESCRIPTION:" + esc(desc)),
        fold("CATEGORIES:" + esc("Tennis") + "," + esc(ev["cat"])),
        "URL:https://www.atptour.com/en/tournaments",
        "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
    ])
    count += 1


for ev in TOURNAMENTS:
    total = (ev["end"] - ev["start"]).days + 1
    named = dict(ev.get("extras", []))
    for i in range(total):
        day = ev["start"] + timedelta(days=i)
        if day in named:
            label = named[day]
        elif i == total - 1:
            label = "Final"
        else:
            label = f"Day {i + 1} of {total}"
        emit(f"{ev['slug']}-2026-d{i + 1}",
             f"{BALL} {ev['name']}",
             day, day + timedelta(days=1), ev,
             f"{label} - {day.strftime('%A %-d %B %Y')}")

lines.append("END:VCALENDAR")

out = "../docs/tennis-2026-atp1000-slams.ics"
with open(out, "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")

print(f"Wrote {count} events across {len(TOURNAMENTS)} tournaments.")
