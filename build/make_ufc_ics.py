#!/usr/bin/env python3
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")
GLOVE, CUP = "\U0001F94A", "\U0001F3C6"

TV = ("Paramount+ - every card, US. There is NO pay-per-view in 2026; "
      "it is included with a Paramount+ subscription. Select numbered events "
      "also simulcast on CBS.")

V = {
    "belgrade": ("Belgrade Arena", "Bulevar Arsenija Carnojevica 58, 11070 Beograd, Serbia", 44.814434, 20.421276),
    "philly": ("Xfinity Mobile Arena", "3601 S Broad St, Philadelphia, PA 19148, USA", 39.901202, -75.171979),
    "sacramento": ("Golden 1 Center", "500 David J Stern Walk, Sacramento, CA 95814, USA", 38.580205, -121.499660),
    "shanghai": ("Shanghai Oriental Sports Center", "Yanjiang Rd, Pudong, Shanghai 200126, China", 31.155555, 121.473030),
    "paris": ("Accor Arena", "8 Bd de Bercy, 75012 Paris, France", 48.838604, 2.378470),
    "glendale": ("Desert Diamond Arena", "9400 W Maryland Ave, Glendale, AZ 85305, USA", 33.532074, -112.261216),
    "la": ("Crypto.com Arena", "1111 S Figueroa St, Los Angeles, CA 90015, USA", 34.043018, -118.267254),
    "edmonton": ("Rogers Place", "10220 104 Ave NW, Edmonton, AB T5J 0H6, Canada", 53.546975, -113.497800),
}

# (uid, name, numbered?, main-card ET datetime OR date if TBC, prelims ET or None,
#  venue key, note)
EVENTS = [
    ("fn-medic-rodriguez", "UFC Fight Night: Medic vs. Rodriguez", False,
     (2026, 8, 1, 13, 0), (2026, 8, 1, 10, 0), "belgrade",
     "Welterweight main event: #14 Uros Medic v #15 Daniel Rodriguez. Early "
     "start for US viewers because it is a European card. NOT simulcast on "
     "CBS - Paramount+ only."),
    ("fn-gamrot-salkilld", "UFC Fight Night: Gamrot vs. Salkilld", False,
     (2026, 8, 8, 17, 0), None, "belgrade",
     "First UFC main event for Australian prospect Quillan Salkilld. Note: "
     "Paramount+ lists Belgrade Arena for a second straight week, which is "
     "unusual - worth reconfirming the venue closer to the date."),
    ("ufc-330", "UFC 330: Makhachev vs. Machado Garry", True,
     (2026, 8, 15, 21, 0), None, "philly",
     "Islam Makhachev defends the welterweight title against Ian Machado "
     "Garry. The promotion's fourth visit to Philadelphia."),
    ("fn-hernandez-rodrigues", "UFC Fight Night: Hernandez vs. Rodrigues", False,
     (2026, 8, 22, 20, 0), None, "sacramento",
     "Middleweight main event: Anthony Hernandez v Gregory Rodrigues."),
    ("fn-nurmagomedov-song", "UFC Fight Night: Nurmagomedov vs. Song", False,
     (2026, 8, 29, 6, 0), None, "shanghai",
     "Bantamweight main event: Umar Nurmagomedov v Song Yadong. A 6 AM ET "
     "start - this is a morning card in the US and an evening one in China."),
    ("fn-paris", "UFC Fight Night: Paris", False,
     date(2026, 9, 5), None, "paris",
     "UFC returns to Paris. Main event not yet announced, and no start time "
     "published - the UFC confirms cards and times roughly 8-12 weeks out."),
    ("noche-ufc", "Noche UFC", False,
     date(2026, 9, 12), None, "glendale",
     "The annual Mexican Independence Day card. Main event and start time not "
     "yet announced."),
    ("ufc-331", "UFC 331", True,
     date(2026, 9, 19), None, "la",
     "Numbered event at Crypto.com Arena. Main event and start time not yet "
     "announced."),
    ("fn-edmonton", "UFC Fight Night: Edmonton", False,
     date(2026, 10, 17), None, "edmonton",
     "UFC returns to Edmonton. Main event and start time not yet announced."),
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
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Claude//UFC 2026//EN",
    "CALSCALE:GREGORIAN", f"X-WR-CALNAME:{GLOVE} UFC 2026 - Upcoming",
    fold("X-WR-CALDESC:" + esc(
        "Upcoming UFC numbered events and Fight Nights. All on Paramount+ in "
        "the US.")),
    "X-WR-TIMEZONE:America/New_York",
]
stamp = "20260728T090000Z"
timed = allday = 0

for uid, name, numbered, main, prelim, vkey, note in EVENTS:
    venue, street, lat, lon = V[vkey]
    kind = "Numbered event" if numbered else "Fight Night"
    emoji = CUP if numbered else GLOVE
    is_timed = isinstance(main, tuple)

    if is_timed:
        start = datetime(*main, tzinfo=ET)
        end = start + timedelta(hours=4)
        pre = datetime(*prelim, tzinfo=ET) if prelim else None
        times = (f"Main card: {start.strftime('%-I:%M %p')} ET  |  "
                 f"{start.astimezone(UTC).strftime('%H:%M')} UTC\n")
        if pre:
            times += (f"Prelims:   {pre.strftime('%-I:%M %p')} ET  |  "
                      f"{pre.astimezone(UTC).strftime('%H:%M')} UTC\n")
        else:
            times += "Prelims:   not yet announced\n"
        dt = [f"DTSTART:{z(start)}", f"DTEND:{z(end)}"]
        day_str = start.strftime('%A %-d %B %Y')
        timed += 1
    else:
        times = ("START TIME NOT YET ANNOUNCED. The UFC confirms cards and "
                 "start times about 8-12 weeks before an event, so this is an "
                 "all-day entry until then.\n")
        dt = [f"DTSTART;VALUE=DATE:{main.strftime('%Y%m%d')}",
              f"DTEND;VALUE=DATE:{(main + timedelta(days=1)).strftime('%Y%m%d')}"]
        day_str = main.strftime('%A %-d %B %Y')
        allday += 1

    desc = (f"{name}\n{kind}\n{day_str}\n\nStart times\n{times}\n"
            f"Venue: {venue}\nAddress: {street}\n\nTV\n{TV}\n\nNotes\n{note}\n"
            f"\nCards change often - check ufc.com closer to the date.")
    lines += [
        "BEGIN:VEVENT", f"UID:{uid}-2026@claude-ufc-cal", f"DTSTAMP:{stamp}",
        *dt,
        fold("SUMMARY:" + esc(f"{emoji} {name}")),
        fold("LOCATION:" + esc(f"{venue}, {street}")),
        f"GEO:{lat};{lon}",
        fold(f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-ADDRESS="{street}";'
             f'X-APPLE-RADIUS=200;X-TITLE="{venue}":geo:{lat},{lon}'),
        fold("DESCRIPTION:" + esc(desc)),
        fold("CATEGORIES:" + esc("UFC") + "," + esc(kind)),
        "URL:https://www.ufc.com/events",
        "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
    ]

lines.append("END:VCALENDAR")
with open("../docs/ufc-2026-upcoming.ics", "w",
          encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print(f"Wrote {timed + allday} events ({timed} timed, {allday} time TBC).")
