#!/usr/bin/env python3
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

UTC = ZoneInfo("UTC")
ET = ZoneInfo("America/New_York")

TV = ("Apple TV - every practice, qualifying, sprint and race session. "
      "Select races and all practice free in the Apple TV app.")

# Official 2026 round numbers (formula1.com) keyed by the dataset slug.
# The dataset carries an extra Sepang round that is NOT on the official
# calendar, so it is excluded and rounds are renumbered to match F1.com.
META = {
    "dutch-grand-prix": dict(rd=12, short="Dutch GP", tz="Europe/Amsterdam",
        venue="Circuit Zandvoort",
        street="Burgemeester van Alphenstraat 108, 2041 KP Zandvoort, Netherlands",
        notes="Sprint weekend. Zandvoort is due to drop off the F1 calendar "
              "after this season, so this is scheduled to be the last Dutch "
              "Grand Prix for now."),
    "italian-grand-prix": dict(rd=13, short="Italian GP", tz="Europe/Rome",
        venue="Autodromo Nazionale Monza",
        street="Viale di Vedano 5, 20900 Monza MB, Italy",
        notes="The Temple of Speed - lowest-downforce setup and the highest "
              "average speeds of the year."),
    "spanish-grand-prix": dict(rd=14, short="Spanish GP", tz="Europe/Madrid",
        venue="MADRING",
        street="Av. del Partenon 5, Barajas, 28042 Madrid, Spain",
        notes="NEW CIRCUIT. First F1 race in Madrid, on a new part-street "
              "layout around the IFEMA centre. Spain's second round of 2026."),
    "azerbaijan-grand-prix": dict(rd=15, short="Azerbaijan GP", tz="Asia/Baku",
        venue="Baku City Circuit",
        street="93 Zarifa Aliyeva, Baku, Azerbaijan",
        notes="SATURDAY RACE. The weekend runs Thursday to Saturday - one of "
              "only two Saturday Grands Prix in 2026."),
    "singapore-grand-prix": dict(rd=16, short="Singapore GP", tz="Asia/Singapore",
        venue="Marina Bay Street Circuit",
        street="1 Republic Blvd, Marina Bay, Singapore 038975",
        notes="Sprint weekend for the first time. Night race, and usually the "
              "most physically punishing event of the season."),
    "us-grand-prix": dict(rd=17, short="United States GP",
        tz="America/Chicago",
        venue="Circuit of The Americas",
        street="9201 Circuit of the Americas Blvd, Del Valle, TX 78617, USA",
        notes="Austin. Reverts to a traditional weekend after hosting a "
              "sprint last year."),
    "mexican-grand-prix": dict(rd=18, short="Mexico City GP",
        tz="America/Mexico_City",
        venue="Autodromo Hermanos Rodriguez",
        street="Viad. Rio de la Piedad S/N, Iztacalco, 08400 Ciudad de Mexico, Mexico",
        notes="Highest race on the calendar at roughly 2,200m. Thin air means "
              "maximum-downforce wings and serious cooling problems."),
    "brazilian-grand-prix": dict(rd=19, short="Sao Paulo GP",
        tz="America/Sao_Paulo",
        venue="Autodromo Jose Carlos Pace (Interlagos)",
        street="Av. Sen. Teotonio Vilela 261, Sao Paulo - SP, 04801-000, Brazil",
        notes="Interlagos reverts to a traditional weekend after running the "
              "sprint format every year since 2021. Weather is famously "
              "unpredictable here."),
    "las-vegas-grand-prix": dict(rd=20, short="Las Vegas GP",
        tz="America/Los_Angeles",
        venue="Las Vegas Strip Circuit (Grand Prix Plaza)",
        street="4400 Koval Ln, Las Vegas, NV 89109, USA",
        notes="SATURDAY RACE, and a late one - lights out 20:00 local on the "
              "Strip. Sessions run deep into the night, so UTC dates land a "
              "day later than the local date."),
    "qatar-grand-prix": dict(rd=21, short="Qatar GP", tz="Asia/Qatar",
        venue="Lusail International Circuit",
        street="Al Wusail, North Relief Road, Doha, Qatar",
        notes="Night race under lights. Penultimate round of the season."),
    "abu-dhabi-grand-prix": dict(rd=22, short="Abu Dhabi GP", tz="Asia/Dubai",
        venue="Yas Marina Circuit",
        street="Yas Leisure Dr, Yas Island, Abu Dhabi, United Arab Emirates",
        notes="SEASON FINALE, round 22 of 22, run into the Gulf sunset. If the "
              "title race goes the distance it is settled here."),
}

# session key -> (display name, emoji, duration minutes, category)
SESSIONS = {
    "fp1":              ("Practice 1", "\U0001F527", 60, "Practice"),
    "fp2":              ("Practice 2", "\U0001F527", 60, "Practice"),
    "fp3":              ("Practice 3", "\U0001F527", 60, "Practice"),
    "sprintQualifying": ("Sprint Qualifying", "\u23F1", 45, "Qualifying"),
    "sprint":           ("SPRINT", "\U0001F3CE", 45, "Sprint"),
    "qualifying":       ("QUALIFYING", "\u23F1", 60, "Qualifying"),
    "gp":               ("RACE", "\U0001F3C1", 120, "Race"),
}
ORDER = ["fp1", "fp2", "fp3", "sprintQualifying", "sprint", "qualifying", "gp"]


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


def z(dt):
    return dt.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


data = json.load(open("f1.json"))
races = {r["slug"]: r for r in data["races"]}

lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0",
    "PRODID:-//Claude//F1 2026 Sessions//EN",
    "CALSCALE:GREGORIAN",
    "X-WR-CALNAME:\U0001F3C1 F1 2026 - Sessions",
    fold("X-WR-CALDESC:" + esc(
        "Every remaining session of the 2026 F1 season, rounds 12-22, with "
        "exact start times. Times stored in UTC and shown in your local zone.")),
    "X-WR-TIMEZONE:UTC",
]

stamp = "20260728T090000Z"
count = 0
summary_rows = []

for slug, meta in META.items():
    race = races[slug]
    track_tz = ZoneInfo(meta["tz"])
    keys = [k for k in ORDER if k in race["sessions"]]
    is_sprint = "sprint" in race["sessions"]

    for k in keys:
        name, emoji, mins, cat = SESSIONS[k]
        start = datetime.fromisoformat(race["sessions"][k].replace("Z", "+00:00"))
        end = start + timedelta(minutes=mins)
        loc_t = start.astimezone(track_tz)
        et_t = start.astimezone(ET)

        desc = (
            f"{meta['short']} - {name}\n"
            f"Round {meta['rd']} of 22\n"
            f"\n"
            f"Start times\n"
            f"Track local: {loc_t.strftime('%a %-d %b, %H:%M %Z')}\n"
            f"US Eastern:  {et_t.strftime('%a %-d %b, %-I:%M %p %Z')}\n"
            f"\n"
            f"TV\n"
            f"{TV}\n"
            f"\n"
            f"Circuit: {meta['venue']}\n"
            f"Address: {meta['street']}\n"
            f"Weekend format: {'Sprint weekend' if is_sprint else 'Traditional weekend'}\n"
            f"\n"
            f"Notes\n"
            f"{meta['notes']}\n"
            f"\n"
            f"Session times occasionally shift - confirm on formula1.com."
        )
        lines += [
            "BEGIN:VEVENT",
            f"UID:{slug}-2026-{k}@claude-f1-cal",
            f"DTSTAMP:{stamp}",
            f"DTSTART:{z(start)}",
            f"DTEND:{z(end)}",
            fold("SUMMARY:" + esc(f"{emoji} {meta['short']} - {name}")),
            fold("LOCATION:" + esc(f"{meta['venue']}, {meta['street']}")),
            f"GEO:{race['latitude']};{race['longitude']}",
            fold(f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;'
                 f'X-ADDRESS="{meta["street"]}";X-APPLE-RADIUS=200;'
                 f'X-TITLE="{meta["venue"]}":'
                 f'geo:{race["latitude"]},{race["longitude"]}'),
            fold("DESCRIPTION:" + esc(desc)),
            fold("CATEGORIES:" + esc("Formula 1") + "," + esc(cat)),
            "URL:https://www.formula1.com/en/racing/2026",
            "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
        ]
        count += 1
        if k == "gp":
            summary_rows.append(
                (meta["rd"], meta["short"],
                 loc_t.strftime("%a %-d %b %H:%M local"),
                 et_t.strftime("%-I:%M %p ET"), len(keys)))

lines.append("END:VCALENDAR")

with open("../docs/f1-2026-sessions.ics", "w",
          encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")

print(f"Wrote {count} timed sessions across {len(META)} race weekends.\n")
for rd, nm, loc, et, ns in summary_rows:
    print(f"  R{rd:>2} {nm:<18} RACE {loc:<22} {et:<12} ({ns} sessions)")
