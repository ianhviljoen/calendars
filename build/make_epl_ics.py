#!/usr/bin/env python3
"""Premier League 2026/27 -> docs/premier-league.ics

Reads epl.txt (openfootball/england 1-premierleague.txt), which update.sh
downloads. Kick-off times in the file are UK local; stored here as UTC.
"""
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

UK, UTC = ZoneInfo("Europe/London"), ZoneInfo("UTC")
BALL = "\u26BD"

SHORT = {
 "Arsenal FC": "Arsenal", "Aston Villa FC": "Aston Villa",
 "AFC Bournemouth": "Bournemouth", "Brentford FC": "Brentford",
 "Brighton & Hove Albion FC": "Brighton", "Chelsea FC": "Chelsea",
 "Coventry City FC": "Coventry", "Crystal Palace FC": "Crystal Palace",
 "Everton FC": "Everton", "Fulham FC": "Fulham", "Hull City AFC": "Hull City",
 "Ipswich Town FC": "Ipswich", "Leeds United FC": "Leeds",
 "Liverpool FC": "Liverpool", "Manchester City FC": "Man City",
 "Manchester United FC": "Man United", "Newcastle United FC": "Newcastle",
 "Nottingham Forest FC": "Nott'm Forest", "Sunderland AFC": "Sunderland",
 "Tottenham Hotspur FC": "Tottenham",
}
LOGO = {
 "Arsenal": "\U0001F534", "Aston Villa": "\U0001F981",
 "Bournemouth": "\U0001F352", "Brentford": "\U0001F41D",
 "Brighton": "\U0001F426", "Chelsea": "\U0001F535",
 "Coventry": "\U0001F418", "Crystal Palace": "\U0001F985",
 "Everton": "\U0001F36C", "Fulham": "\U0001F3E0", "Hull City": "\U0001F42F",
 "Ipswich": "\U0001F69C", "Leeds": "\U0001F99A", "Liverpool": "\u2764\uFE0F",
 "Man City": "\U0001F499", "Man United": "\U0001F608",
 "Newcastle": "\U0001F3F0", "Nott'm Forest": "\U0001F333",
 "Sunderland": "\U0001F408", "Tottenham": "\U0001F413",
}
GROUND = {
 "Arsenal": "Emirates Stadium, London", "Aston Villa": "Villa Park, Birmingham",
 "Bournemouth": "Vitality Stadium, Bournemouth",
 "Brentford": "Gtech Community Stadium, London",
 "Brighton": "Amex Stadium, Falmer", "Chelsea": "Stamford Bridge, London",
 "Coventry": "Coventry Building Society Arena, Coventry",
 "Crystal Palace": "Selhurst Park, London",
 "Everton": "Hill Dickinson Stadium, Liverpool",
 "Fulham": "Craven Cottage, London", "Hull City": "MKM Stadium, Hull",
 "Ipswich": "Portman Road, Ipswich", "Leeds": "Elland Road, Leeds",
 "Liverpool": "Anfield, Liverpool", "Man City": "Etihad Stadium, Manchester",
 "Man United": "Old Trafford, Manchester",
 "Newcastle": "St James' Park, Newcastle upon Tyne",
 "Nott'm Forest": "City Ground, Nottingham",
 "Sunderland": "Stadium of Light, Sunderland",
 "Tottenham": "Tottenham Hotspur Stadium, London",
}
MONTHS = {m: i for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}


def parse(path="epl.txt"):
    md = cur_date = cur_time = None
    year = None
    prev_month = 0
    out = []
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = re.match(r"\u25AA\s*Matchday\s+(\d+)", line.strip())
        if m:
            md = int(m.group(1)); continue
        d = re.match(r"\s+\w{3}\s+(\w{3})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$", line)
        if d:
            mon, day, yr = MONTHS[d.group(1)], int(d.group(2)), d.group(3)
            if yr:
                year = int(yr)
            elif prev_month and mon < prev_month:
                year += 1                      # December -> January rollover
            prev_month = mon
            cur_date = (year, mon, day)
            cur_time = None
            continue
        g = re.match(r"\s+(?:(\d{2}):(\d{2}))?\s+(.+?)\s+v\s+(.+?)\s*$", line)
        if g and cur_date:
            if g.group(1):
                cur_time = (int(g.group(1)), int(g.group(2)))
            if not cur_time:
                continue
            home, away = g.group(3).strip(), g.group(4).strip()
            if home not in SHORT or away not in SHORT:
                continue
            out.append((md, cur_date, cur_time, SHORT[home], SHORT[away]))
    return out


def esc(t):
    return (t.replace("\\", "\\\\").replace(";", "\\;")
             .replace(",", "\\,").replace("\n", "\\n"))


def fold(line):
    out, cur = [], ""
    for ch in line:
        if len(cur.encode("utf-8")) + len(ch.encode("utf-8")) > 73:
            out.append(cur); cur = " "
        cur += ch
    out.append(cur)
    return "\r\n".join(out)


def z(dt):
    return dt.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


matches = parse()
lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0",
    "PRODID:-//Claude//Premier League//EN", "CALSCALE:GREGORIAN",
    f"X-WR-CALNAME:{BALL} Premier League",
    "X-APPLE-CALENDAR-COLOR:#37003C",
    fold("X-WR-CALDESC:" + esc(
        "Premier League 2026/27, all 380 fixtures. Each club has its own "
        "emoji. Kick-off times UK local, stored in UTC.")),
    "X-WR-TIMEZONE:Europe/London",
]
stamp, seen = "20260731T090000Z", set()

for md, (y, mo, d), (hh, mi), home, away in matches:
    start = datetime(y, mo, d, hh, mi, tzinfo=UK)
    end = start + timedelta(hours=2)
    uid = f"epl-{y}{mo:02d}{d:02d}-{home[:3]}-{away[:3]}".replace("'", "")
    while uid in seen:
        uid += "x"
    seen.add(uid)
    desc = (
        f"{LOGO[home]} {home} v {LOGO[away]} {away}\n"
        f"Matchweek {md} - {start.strftime('%A %-d %B %Y')}\n"
        f"\n"
        f"Kick-off\n{start.strftime('%H:%M')} UK  |  "
        f"{start.astimezone(UTC).strftime('%H:%M')} UTC\n"
        f"\n"
        f"Ground\n{GROUND[home]}\n"
        f"\n"
        f"KICK-OFF TIMES MOVE. Only the next few matchweeks are fixed. "
        f"Broadcasters select matches around five to six weeks ahead, and any "
        f"fixture can shift day or time for TV, or be postponed for cup ties "
        f"and European commitments. Later rounds here show provisional slots."
    )
    lines += [
        "BEGIN:VEVENT", f"UID:{uid}@claude-epl", f"DTSTAMP:{stamp}",
        f"DTSTART:{z(start)}", f"DTEND:{z(end)}",
        fold("SUMMARY:" + esc(
            f"{BALL} {LOGO[home]} {home} v {LOGO[away]} {away} (MW{md})")),
        fold("LOCATION:" + esc(GROUND[home])),
        fold("DESCRIPTION:" + esc(desc)),
        fold("CATEGORIES:" + esc("Premier League") + "," +
             esc(f"Matchweek {md}")),
        "URL:https://www.premierleague.com/fixtures",
        "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
    ]

lines.append("END:VCALENDAR")
with open("../docs/premier-league.ics", "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print(f"Wrote {len(matches)} fixtures across "
      f"{len({m[0] for m in matches})} matchweeks.")
