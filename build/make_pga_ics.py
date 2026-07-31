#!/usr/bin/env python3
from datetime import date, timedelta

CBS = "ESPN+, CBS, Golf Chnl, Paramount+"
CBS_E = "ESPN, ESPN+, CBS, Golf Chnl, Paramount+"
NBC = "ESPN+, NBC, Golf Chnl, Peacock"
FALL = "ESPN+, Golf Chnl"
INTL = "Golf Chnl, SiriusXM"

# venue -> (street address, latitude, longitude)
PLACES = {
    "Detroit Golf Club": ("17911 Hamilton Rd, Detroit, MI 48203, USA", 42.426280, -83.126246),
    "Sedgefield Country Club": ("3201 Forsyth Dr, Greensboro, NC 27407, USA", 36.014392, -79.886843),
    "TPC Southwind": ("3325 Club at Southwind, Memphis, TN 38125, USA", 35.057345, -89.779162),
    "Bellerive Country Club": ("12925 Ladue Rd, St. Louis, MO 63141, USA", 38.659447, -90.482938),
    "East Lake Golf Club": ("2575 Alston Dr SE, Atlanta, GA 30317, USA", 33.743386, -84.302761),
    "The Cliffs at Walnut Cove": ("40 Club Village Way, Arden, NC 28704, USA", 35.462683, -82.602450),
    "Medinah Country Club (Course No. 3)": ("6N001 Medinah Rd, Medinah, IL 60157, USA", 41.966380, -88.048044),
    "Black Desert Resort": ("250 S Weiskopf Way, Ivins, UT 84738, USA", 37.164395, -113.645869),
    "Yokohama Country Club": ("1025 Imaicho, Hodogaya Ward, Yokohama, Kanagawa 240-0035, Japan", 35.445905, 139.548955),
    "Port Royal Golf Course": ("5 Port Royal Golf Course Rd, Southampton SB 03, Bermuda", 32.262181, -64.873898),
    "Vidanta Vallarta": ("Puerto Vallarta, Jalisco 48291, Mexico", 20.689906, -105.259960),
    "El Cardonal at Diamante": ("Diamante Blvd, Cabo San Lucas, B.C.S. 23473, Mexico", 22.901367, -109.987110),
    "Omni Barton Creek Resort & Spa (Fazio Canyons)": ("8212 Barton Club Dr, Austin, TX 78735, USA", 30.291258, -97.858300),
    "Sea Island Golf Club": ("100 Retreat Ave, St Simons Island, GA 31522, USA", 31.138277, -81.405702),
}

EVENTS = [
    dict(slug="rocket-classic", name="Rocket Classic",
         start=date(2026, 7, 30), venue="Detroit Golf Club",
         loc="Detroit, Michigan, USA", purse="$9.6M (approx.)", tv=CBS,
         cat="FedExCup Regular Season",
         notes="Defending champion: Aldrich Potgieter. One of two events left "
               "for players on the FedExCup bubble to force their way into the "
               "top 70."),
    dict(slug="wyndham-championship", name="Wyndham Championship",
         start=date(2026, 8, 6), venue="Sedgefield Country Club",
         loc="Greensboro, North Carolina, USA", purse="$8.2M (approx.)", tv=CBS,
         cat="FedExCup Regular Season",
         notes="Regular-season finale. The top 70 in the FedExCup standings "
               "after this week advance to the Playoffs. Defending champion: "
               "Cameron Young."),
    dict(slug="fedex-st-jude", name="FedEx St. Jude Championship",
         start=date(2026, 8, 13), venue="TPC Southwind",
         loc="Memphis, Tennessee, USA", purse="$20M (approx.)", tv=CBS_E,
         cat="FedExCup Playoffs (1 of 3)",
         notes="Playoffs opener. Field of 70, cut to the top 50 for the BMW. "
               "Defending champion: Justin Rose."),
    dict(slug="bmw-championship", name="BMW Championship",
         start=date(2026, 8, 20), venue="Bellerive Country Club",
         loc="St. Louis, Missouri, USA", purse="$20M (approx.)", tv=CBS_E,
         cat="FedExCup Playoffs (2 of 3)",
         notes="No cut. Field of 50, reduced to the top 30 for the TOUR "
               "Championship. Defending champion: Scottie Scheffler."),
    dict(slug="tour-championship", name="TOUR Championship",
         start=date(2026, 8, 27), venue="East Lake Golf Club",
         loc="Atlanta, Georgia, USA", purse="$40M (approx.)", tv=NBC,
         cat="FedExCup Playoffs (3 of 3)",
         notes="Season finale. Top 30 only, and the 20th edition of the "
               "FedExCup. Winner takes the FedExCup title. Defending champion: "
               "Scottie Scheffler."),
    dict(slug="biltmore-championship", name="Biltmore Championship Asheville",
         start=date(2026, 9, 17), venue="The Cliffs at Walnut Cove",
         loc="Asheville, North Carolina, USA", purse="$5M", tv=FALL,
         cat="FedExCup Fall",
         notes="NEW EVENT. Opens the FedExCup Fall and brings the PGA TOUR back "
               "to Asheville for the first time in more than 80 years. Likely to "
               "draw a strong field as it falls the week before the Presidents "
               "Cup."),
    dict(slug="presidents-cup", name="Presidents Cup",
         start=date(2026, 9, 24), venue="Medinah Country Club (Course No. 3)",
         loc="Medinah, Illinois, USA", purse="No purse - team match play",
         tv="NBC, Golf Chnl", cat="Team Event",
         notes="16th edition. USA (Captain Brandt Snedeker) v International Team "
               "(Captain Geoff Ogilvy). Medinah also hosted the 2012 Ryder Cup.",
         days=["Day 1 - Foursomes", "Day 2 - Four-ball",
               "Day 3 - Foursomes & Four-ball", "Day 4 - Singles"]),
    dict(slug="bank-of-utah-championship", name="Bank of Utah Championship",
         start=date(2026, 10, 1), venue="Black Desert Resort",
         loc="Ivins, Utah, USA", purse="$6M", tv=FALL, cat="FedExCup Fall",
         notes="Defending champion: Michael Brennan."),
    dict(slug="baycurrent-classic", name="Baycurrent Classic",
         start=date(2026, 10, 8), venue="Yokohama Country Club",
         loc="Yokohama, Japan", purse="$8M", tv="Golf Chnl",
         cat="FedExCup Fall",
         notes="Richest event of the FedExCup Fall. Defending champion: Xander "
               "Schauffele. Heads up - Japan is 13 hours ahead of US Eastern, "
               "so play airs overnight in the States."),
    dict(slug="butterfield-bermuda", name="Butterfield Bermuda Championship",
         start=date(2026, 10, 22), venue="Port Royal Golf Course",
         loc="Southampton, Bermuda", purse="$6M", tv=INTL, cat="FedExCup Fall",
         notes="Defending champion: Adam Schenk. Wind off the Atlantic is "
               "usually the defence at Port Royal."),
    dict(slug="vidantaworld-mexico-open", name="VidantaWorld Mexico Open",
         start=date(2026, 10, 29), venue="Vidanta Vallarta",
         loc="Puerto Vallarta, Mexico", purse="$6M", tv=INTL,
         cat="FedExCup Fall",
         notes="Moved from its traditional spring slot into the FedExCup Fall. "
               "First leg of the new two-week Mexico swing."),
    dict(slug="wwt-championship", name="World Wide Technology Championship",
         start=date(2026, 11, 5), venue="El Cardonal at Diamante",
         loc="Los Cabos, Mexico", purse="$6M", tv=INTL, cat="FedExCup Fall",
         notes="Played on the Tiger Woods-designed El Cardonal. Second leg of "
               "the Mexico swing. Defending champion: Ben Griffin."),
    dict(slug="good-good-championship", name="Good Good Championship",
         start=date(2026, 11, 12),
         venue="Omni Barton Creek Resort & Spa (Fazio Canyons)",
         loc="Austin, Texas, USA", purse="$6M", tv=FALL, cat="FedExCup Fall",
         notes="NEW EVENT. Inaugural playing, sponsored by the Good Good golf "
               "media brand, and the TOUR's return to Austin after a three-year "
               "absence."),
    dict(slug="rsm-classic", name="The RSM Classic",
         start=date(2026, 11, 19), venue="Sea Island Golf Club",
         loc="St. Simons Island, Georgia, USA", purse="$7.4M", tv=FALL,
         cat="FedExCup Fall",
         notes="Season closer. Final FedExCup Fall standings are set here - the "
               "top 100 keep 2027 PGA TOUR cards (down from 125), and Nos. 51-60 "
               "earn spots in two early 2027 Signature Events. Defending "
               "champion: Sami Valimaki."),
]

DEFAULT_DAYS = ["Round 1", "Round 2", "Round 3 (Moving Day)", "Round 4 (Final Round)"]


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
    "PRODID:-//Claude//PGA TOUR 2026 Upcoming Schedule//EN",
    "CALSCALE:GREGORIAN",
    "X-WR-CALNAME:\u26f3 PGA Tour",
    fold("X-WR-CALDESC:" + esc(
        "All 56 remaining round-days of the 2026 PGA TOUR season: FedExCup "
        "regular season, Playoffs, Presidents Cup and FedExCup Fall.")),
    "X-WR-TIMEZONE:UTC",
]

stamp = "20260727T090000Z"
count = 0

for ev in EVENTS:
    day_labels = ev.get("days", DEFAULT_DAYS)
    finish = ev["start"] + timedelta(days=3)
    window = (f"{ev['start'].strftime('%a %-d %b')} - "
              f"{finish.strftime('%a %-d %b %Y')}")
    street, lat, lon = PLACES[ev["venue"]]
    for i, label in enumerate(day_labels):
        day = ev["start"] + timedelta(days=i)
        desc = (
            f"{label} - {day.strftime('%A %-d %B %Y')}\n"
            f"\n"
            f"Venue: {ev['venue']}\n"
            f"Address: {street}\n"
            f"Tournament dates: {window}\n"
            f"Purse: {ev['purse']}\n"
            f"Event type: {ev['cat']}\n"
            f"\n"
            f"Notes\n"
            f"{ev['notes']}\n"
            f"\n"
            f"Tee times are confirmed the week of the event - pgatour.com/schedule\n"
        )
        lines += [
            "BEGIN:VEVENT",
            f"UID:{ev['slug']}-2026-d{i+1}@claude-pga-cal",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{day.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(day + timedelta(days=1)).strftime('%Y%m%d')}",
            fold("SUMMARY:" + esc(f"\u26f3 {ev['name']}")),
            fold("LOCATION:" + esc(f"{ev['venue']}, {street}")),
            f"GEO:{lat};{lon}",
            fold(f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-ADDRESS="{street}";'
                 f'X-APPLE-RADIUS=150;X-TITLE="{ev["venue"]}":'
                 f'geo:{lat},{lon}'),
            fold("DESCRIPTION:" + esc(desc)),
            fold("CATEGORIES:" + esc("PGA TOUR") + "," + esc(ev["cat"])),
            "URL:https://www.pgatour.com/schedule",
            "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
        ]
        count += 1

lines.append("END:VCALENDAR")

out = "../docs/pga-tour.ics"
with open(out, "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")

print(f"Wrote {count} events across {len(EVENTS)} tournaments.")
