#!/usr/bin/env python3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")
CAR = "\U0001F3CE"

# (uid, race label, ET datetime, venue, street, lat, lon, tv, phase, note)
R = [
    ("iowa", "Iowa Speedway", (2026, 8, 9, 15, 30),
     "Iowa Speedway", "3333 Rusty Wallace Dr, Newton, IA 50208, USA",
     41.676843, -93.011004, "USA Network", "Regular season",
     "Back from the summer off-weekend of August 2."),
    ("richmond", "Richmond Raceway", (2026, 8, 15, 19, 0),
     "Richmond Raceway", "600 E Laburnum Ave, Richmond, VA 23222, USA",
     37.588318, -77.421959, "USA Network", "Regular season",
     "Saturday night short-track race."),
    ("newhampshire", "New Hampshire Motor Speedway", (2026, 8, 23, 15, 0),
     "New Hampshire Motor Speedway", "1122 NH-106, Loudon, NH 03307, USA",
     43.362680, -71.460573, "USA Network", "Regular season",
     "Penultimate race of the regular season."),
    ("daytona-aug", "Daytona (Regular-Season Finale)", (2026, 8, 29, 19, 30),
     "Daytona International Speedway", "1801 W International Speedway Blvd, Daytona Beach, FL 32114, USA",
     29.185167, -81.070694, "NBC", "Regular season",
     "REGULAR-SEASON FINALE. Saturday night at Daytona - the last chance to "
     "make the playoff field."),

    ("darlington", "Southern 500 (Darlington)", (2026, 9, 6, 17, 0),
     "Darlington Raceway", "1301 Harry Byrd Hwy, Darlington, SC 29532, USA",
     34.297315, -79.905162, "USA Network", "Playoffs - race 1 of 10",
     "PLAYOFF OPENER on Labor Day weekend. The Southern 500 is one of the "
     "sport's crown-jewel races."),
    ("gateway", "World Wide Technology Raceway", (2026, 9, 13, 15, 0),
     "World Wide Technology Raceway", "700 Raceway Blvd, Madison, IL 62060, USA",
     38.650754, -90.135355, "USA Network", "Playoffs - race 2 of 10", ""),
    ("bristol", "Bristol Motor Speedway", (2026, 9, 19, 19, 30),
     "Bristol Motor Speedway", "151 Speedway Blvd, Bristol, TN 37620, USA",
     36.515694, -82.256967, "USA Network", "Playoffs - race 3 of 10",
     "The Bristol night race under the lights."),
    ("kansas", "Kansas Speedway", (2026, 9, 27, 15, 0),
     "Kansas Speedway", "400 Speedway Blvd, Kansas City, KS 66111, USA",
     39.116987, -94.834390, "USA Network", "Playoffs - race 4 of 10", ""),
    ("vegas", "Las Vegas Motor Speedway", (2026, 10, 4, 17, 30),
     "Las Vegas Motor Speedway", "7000 Las Vegas Blvd N, Las Vegas, NV 89115, USA",
     36.273357, -115.011441, "USA Network", "Playoffs - race 5 of 10", ""),
    ("roval", "Charlotte ROVAL", (2026, 10, 11, 15, 0),
     "Charlotte Motor Speedway (ROVAL)", "5555 Concord Pkwy S, Concord, NC 28027, USA",
     35.352626, -80.685659, "USA Network", "Playoffs - race 6 of 10",
     "Run on the road-course layout inside the oval."),
    ("phoenix", "Phoenix Raceway", (2026, 10, 18, 15, 0),
     "Phoenix Raceway", "7602 Jimmie Johnson Dr, Avondale, AZ 85323, USA",
     33.375042, -112.311154, "USA Network", "Playoffs - race 7 of 10",
     "Phoenix hosted the title decider for the past six seasons - not in 2026."),
    ("talladega", "Talladega Superspeedway", (2026, 10, 25, 14, 0),
     "Talladega Superspeedway", "3366 Speedway Blvd, Lincoln, AL 35096, USA",
     33.566227, -86.069868, "NBC", "Playoffs - race 8 of 10",
     "Biggest track on the circuit and the biggest wildcard of the playoffs."),
    ("martinsville", "Martinsville Speedway", (2026, 11, 1, 14, 0),
     "Martinsville Speedway", "340 Speedway Rd, Ridgeway, VA 24148, USA",
     36.634027, -79.851677, "NBC", "Playoffs - race 9 of 10",
     "Last race before the finale."),
    ("homestead", "CHAMPIONSHIP RACE (Homestead-Miami)", (2026, 11, 8, 15, 0),
     "Homestead-Miami Speedway", "One Ralph Sanchez Speedway Blvd, Homestead, FL 33035, USA",
     25.453285, -80.409305, "NBC", "Playoffs - CHAMPIONSHIP",
     "SEASON FINALE. The title race returns to Homestead-Miami for the first "
     "time since 2019, after six years at Phoenix."),
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


def z(dt):
    return dt.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0",
    "PRODID:-//Claude//NASCAR Cup Series 2026//EN", "CALSCALE:GREGORIAN",
    f"X-WR-CALNAME:{CAR} NASCAR Cup",
    fold("X-WR-CALDESC:" + esc(
        "Remaining 2026 NASCAR Cup Series races with green-flag times. "
        "US broadcast listings.")),
    "X-WR-TIMEZONE:America/New_York",
]
stamp = "20260728T090000Z"

for uid, label, t, venue, street, lat, lon, tv, phase, note in R:
    start = datetime(*t, tzinfo=ET)
    end = start + timedelta(hours=3, minutes=30)
    desc = (
        f"{label}\n{start.strftime('%A %-d %B %Y')}\n"
        f"\n"
        f"Green flag\n"
        f"{start.strftime('%-I:%M %p')} ET  |  {z(start)[9:11]}:{z(start)[11:13]} UTC\n"
        f"\n"
        f"Track: {venue}\n"
        f"Address: {street}\n"
        f"Stage: {phase}\n"
        + (f"\nNotes\n{note}\n" if note else "")
        + f"\nEnd time is an estimate - races typically run 3 to 4 hours "
          f"including cautions. Practice and qualifying times are released "
          f"roughly two weeks before each event."
    )
    lines += [
        "BEGIN:VEVENT", f"UID:nascar-{uid}-2026@claude-nascar-cal",
        f"DTSTAMP:{stamp}", f"DTSTART:{z(start)}", f"DTEND:{z(end)}",
        fold("SUMMARY:" + esc(f"{CAR} NASCAR Cup - {label}")),
        fold("LOCATION:" + esc(f"{venue}, {street}")),
        f"GEO:{lat};{lon}",
        fold(f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-ADDRESS="{street}";'
             f'X-APPLE-RADIUS=300;X-TITLE="{venue}":geo:{lat},{lon}'),
        fold("DESCRIPTION:" + esc(desc)),
        fold("CATEGORIES:" + esc("NASCAR Cup Series") + "," + esc(phase)),
        "URL:https://www.nascar.com/nascar-cup-series/2026/schedule/",
        "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
    ]

lines.append("END:VCALENDAR")
with open("../docs/nascar.ics", "w",
          encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print(f"Wrote {len(R)} races.")
