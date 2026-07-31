#!/usr/bin/env python3
import csv, collections
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ET, UTC = ZoneInfo("America/New_York"), ZoneInfo("UTC")
BALL, STAR, NOTE = "\U0001F3C8", "\u2B50", "\U0001F4CB"

TEAM = {
 "ARI": "Cardinals", "ATL": "Falcons", "BAL": "Ravens", "BUF": "Bills",
 "CAR": "Panthers", "CHI": "Bears", "CIN": "Bengals", "CLE": "Browns",
 "DAL": "Cowboys", "DEN": "Broncos", "DET": "Lions", "GB": "Packers",
 "HOU": "Texans", "IND": "Colts", "JAX": "Jaguars", "KC": "Chiefs",
 "LA": "Rams", "LAC": "Chargers", "LV": "Raiders", "MIA": "Dolphins",
 "MIN": "Vikings", "NE": "Patriots", "NO": "Saints", "NYG": "Giants",
 "NYJ": "Jets", "PHI": "Eagles", "PIT": "Steelers", "SEA": "Seahawks",
 "SF": "49ers", "TB": "Buccaneers", "TEN": "Titans", "WAS": "Commanders",
}
BY_NAME = {v: k for k, v in TEAM.items()}

LOGO = {
 "BUF": "\U0001F9AC", "MIA": "\U0001F42C", "NE": "\U0001F3A9", "NYJ": "\u2708\uFE0F",
 "BAL": "\U0001FAB6", "CIN": "\U0001F405", "CLE": "\U0001F7EB", "PIT": "\u2692\uFE0F",
 "HOU": "\U0001F402", "IND": "\U0001F40E", "JAX": "\U0001F406", "TEN": "\u2694\uFE0F",
 "DEN": "\U0001F434", "KC": "\U0001F3F9", "LV": "\u2620\uFE0F", "LAC": "\u26A1",
 "DAL": "\u2B50", "NYG": "\U0001F5FD", "PHI": "\U0001F985", "WAS": "\U0001F396\uFE0F",
 "CHI": "\U0001F43B", "DET": "\U0001F981", "GB": "\U0001F9C0", "MIN": "\U0001FA93",
 "ATL": "\U0001F426", "CAR": "\U0001F43E", "NO": "\u269C\uFE0F", "TB": "\u2693",
 "ARI": "\U0001F335", "LA": "\U0001F40F", "SF": "\u26CF\uFE0F", "SEA": "\U0001F30A",
}

STADIUM_FIX = {
 "Reliant Stadium": "NRG Stadium",
 "Bernabeu": "Estadio Santiago Bernabeu",
 "FC Bayern Munich Stadium": "Allianz Arena",
 "Maracana Stadium": "Estadio do Maracana",
 "Estadio Banorte": "Estadio Banorte (Azteca)",
}
INTL = {
 "Melbourne Cricket Ground": "Melbourne, Australia - the NFL's first regular-season game in Australia.",
 "Estadio do Maracana": "Rio de Janeiro, Brazil.",
 "Tottenham Hotspur Stadium": "London, England.",
 "Wembley Stadium": "London, England.",
 "Stade de France": "Saint-Denis, Paris - the NFL's first regular-season game in France.",
 "Estadio Santiago Bernabeu": "Madrid, Spain.",
 "Allianz Arena": "Munich, Germany.",
 "Estadio Banorte (Azteca)": "Mexico City.",
}

# ---- preseason: (date, ET time, away, home, tv) ----
PRE = [
 # Week 1
 ("2026-08-13","19:00","Packers","Steelers","NFL Network",1),
 ("2026-08-13","19:00","Lions","Bengals","Local",1),
 ("2026-08-13","19:30","Colts","Patriots","Local",1),
 ("2026-08-13","20:00","Chargers","Texans","Local",1),
 ("2026-08-13","20:00","Cardinals","Raiders","ESPN App",1),
 ("2026-08-13","21:00","Titans","49ers","NFL Network",1),
 ("2026-08-14","19:00","Broncos","Falcons","ESPN App",1),
 ("2026-08-14","19:00","Buccaneers","Jets","NFL Network",1),
 ("2026-08-14","19:00","Dolphins","Commanders","Local",1),
 ("2026-08-15","13:00","Panthers","Bills","Local",1),
 ("2026-08-15","13:00","Browns","Bears","NFL Network",1),
 ("2026-08-15","13:00","Vikings","Giants","ESPN App",1),
 ("2026-08-15","16:00","Rams","Chiefs","NFL Network",1),
 ("2026-08-15","16:00","Jaguars","Saints","ESPN App",1),
 ("2026-08-15","19:00","Eagles","Ravens","ESPN App",1),
 ("2026-08-15","20:00","Cowboys","Seahawks","NFL Network",1),
 # Week 2
 ("2026-08-20","20:00","Raiders","Texans","ESPN (national)",2),
 ("2026-08-20","22:00","49ers","Chargers","NFL Network",2),
 ("2026-08-21","19:00","Jets","Steelers","NFL Network",2),
 ("2026-08-21","19:30","Panthers","Jaguars","ESPN App",2),
 ("2026-08-21","21:00","Packers","Broncos","NFL Network",2),
 ("2026-08-22","12:00","Commanders","Lions","Local",2),
 ("2026-08-22","13:00","Bills","Browns","NFL Network",2),
 ("2026-08-22","13:00","Falcons","Colts","Local",2),
 ("2026-08-22","13:00","Ravens","Vikings","ESPN App",2),
 ("2026-08-22","16:00","Saints","Rams","ESPN App",2),
 ("2026-08-22","16:00","Giants","Dolphins","NFL Network",2),
 ("2026-08-22","19:00","Bears","Bengals","Local",2),
 ("2026-08-22","19:00","Eagles","Patriots","NFL Network",2),
 ("2026-08-22","19:30","Chiefs","Buccaneers","ESPN App",2),
 ("2026-08-22","22:00","Cowboys","Cardinals","NFL Network",2),
 ("2026-08-23","20:00","Seahawks","Titans","FOX (national)",2),
 # Week 3
 ("2026-08-27","19:00","Steelers","Bills","NFL Network",3),
 ("2026-08-27","20:00","Patriots","Browns","Prime Video (national)",3),
 ("2026-08-27","20:00","49ers","Raiders","ESPN App",3),
 ("2026-08-27","22:00","Rams","Chargers","NFL Network",3),
 ("2026-08-28","18:00","Commanders","Ravens","NFL Network",3),
 ("2026-08-28","19:00","Falcons","Dolphins","Local",3),
 ("2026-08-28","19:00","Texans","Panthers","Local",3),
 ("2026-08-28","19:30","Giants","Jets","Local",3),
 ("2026-08-28","19:30","Buccaneers","Jaguars","Local",3),
 ("2026-08-28","20:00","Saints","Cowboys","ESPN App",3),
 ("2026-08-28","20:00","Cardinals","Packers","Local",3),
 ("2026-08-28","20:00","Seahawks","Chiefs","ESPN App",3),
 ("2026-08-28","20:00","Bengals","Eagles","CBS (national)",3),
 ("2026-08-28","21:00","Vikings","Broncos","NFL Network",3),
 ("2026-08-29","13:00","Lions","Colts","NFL Network",3),
 ("2026-08-29","18:00","Bears","Titans","NFL Network",3),
]

KEY = [
 ("2026-08-08","12:00","Hall of Fame Class of 2026 enshrinement",
  "Canton, Ohio. The 2026 class is headlined by Drew Brees, Larry "
  "Fitzgerald, Luke Kuechly, Adam Vinatieri and Roger Craig.", 180),
 ("2026-08-30","18:00","Roster cutdown - 90 to 53",
  "All 32 clubs must cut to a 53-man roster by 6:00pm ET. Earlier than "
  "usual this year because the season opens on a Wednesday.", 30),
 ("2026-08-31","13:00","Waiver claims / practice squads form",
  "Waiver claims processed at 1:00pm ET, then practice squads are built "
  "from the players who clear.", 30),
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


rows = [r for r in csv.DictReader(open("nfl.csv")) if r["season"] == "2026"]
# most common home venue per team, for preseason locations
home_ct = collections.defaultdict(collections.Counter)
for r in rows:
    home_ct[r["home_team"]][STADIUM_FIX.get(r["stadium"], r["stadium"])] += 1
HOME = {t: c.most_common(1)[0][0] for t, c in home_ct.items()}

lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0",
    "PRODID:-//Claude//NFL 2026 Full Season//EN", "CALSCALE:GREGORIAN",
    f"X-WR-CALNAME:{BALL} NFL 2026 Season",
    "X-APPLE-CALENDAR-COLOR:#013369",
    fold("X-WR-CALDESC:" + esc(
        "The complete 2026 NFL season - Hall of Fame Game, all 48 preseason "
        "games and all 272 regular-season games, plus roster deadlines. Each "
        "team has its own emoji. Times Eastern, stored in UTC.")),
    "X-WR-TIMEZONE:America/New_York",
]
stamp, n_pre, n_reg, n_key = "20260729T090000Z", 0, 0, 0


def emit(uid, summary, start, mins, desc, loc, cats):
    lines.extend([
        "BEGIN:VEVENT", f"UID:{uid}@claude-nfl", f"DTSTAMP:{stamp}",
        f"DTSTART:{z(start)}",
        f"DTEND:{z(start + timedelta(minutes=mins))}",
        fold("SUMMARY:" + esc(summary)),
    ] + ([fold("LOCATION:" + esc(loc))] if loc else []) + [
        fold("DESCRIPTION:" + esc(desc)),
        fold("CATEGORIES:" + esc("NFL") + "," + esc(cats)),
        "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
    ])


# ---------- Hall of Fame Game ----------
hof = datetime(2026, 8, 6, 20, 0, tzinfo=ET)
emit("nfl-2026-hof", f"{BALL} {LOGO['ARI']} Cardinals vs {LOGO['CAR']} "
     f"Panthers (Hall of Fame Game)", hof, 195,
     f"{LOGO['ARI']} Cardinals vs {LOGO['CAR']} Panthers\n"
     f"Pro Football Hall of Fame Game - {hof.strftime('%A %-d %B %Y')}\n\n"
     f"Kick-off\n8:00 PM ET  |  {hof.astimezone(UTC).strftime('%H:%M')} UTC\n\n"
     f"TV\nNBC / Peacock / NFL+\n\n"
     f"Venue\nTom Benson Hall of Fame Stadium, Canton, Ohio\n\n"
     f"Notes\nThe first game of the 2026 season, a week before preseason "
     f"proper. Arizona and Carolina therefore play four preseason games "
     f"while everyone else plays three. The Hall of Fame class is enshrined "
     f"two days later.\n\nNo overtime in preseason - level scores end as ties.",
     "Tom Benson Hall of Fame Stadium, Canton, Ohio", "Preseason")
n_pre += 1

# ---------- Preseason ----------
for date_s, time_s, away, home, tv, wk in PRE:
    y, m, d = map(int, date_s.split("-"))
    hh, mm = map(int, time_s.split(":"))
    start = datetime(y, m, d, hh, mm, tzinfo=ET)
    at, ht = BY_NAME[away], BY_NAME[home]
    emit(f"nfl-2026-pre{wk}-{at}-{ht}",
         f"{BALL} {LOGO[at]} {away} @ {LOGO[ht]} {home} (Pre Wk {wk})",
         start, 195,
         f"{LOGO[at]} {away} @ {LOGO[ht]} {home}\n"
         f"Preseason Week {wk} - {start.strftime('%A %-d %B %Y')}\n\n"
         f"Kick-off\n{start.strftime('%-I:%M %p')} ET  |  "
         f"{start.astimezone(UTC).strftime('%H:%M')} UTC\n\n"
         f"TV\n{tv}\n\n"
         f"Venue\n{HOME[ht]}\n\n"
         f"Notes\nExhibition - results do not count. Starters play sparingly, "
         f"and there is no overtime, so level scores end as ties.\n\n"
         f"Only five preseason games are national: NBC on 6 Aug, ESPN on "
         f"20 Aug, FOX on 23 Aug, Prime Video on 27 Aug and CBS on 28 Aug. "
         f"NFL Network and the ESPN App carry out-of-market games, blacked "
         f"out in the participating teams' markets.",
         HOME[ht], f"Preseason Week {wk}")
    n_pre += 1

# ---------- Key dates ----------
for date_s, time_s, title, note, mins in KEY:
    y, m, d = map(int, date_s.split("-"))
    hh, mm = map(int, time_s.split(":"))
    start = datetime(y, m, d, hh, mm, tzinfo=ET)
    emit(f"nfl-2026-key-{date_s}", f"{NOTE} {title}", start, mins,
         f"{title}\n{start.strftime('%A %-d %B %Y')}\n\n"
         f"Time\n{start.strftime('%-I:%M %p')} ET  |  "
         f"{start.astimezone(UTC).strftime('%H:%M')} UTC\n\nNotes\n{note}",
         "", "Key date")
    n_key += 1

# ---------- Regular season ----------
for r in sorted(rows, key=lambda r: (r["gameday"], r["gametime"])):
    y, m, d = map(int, r["gameday"].split("-"))
    hh, mm = map(int, r["gametime"].split(":"))
    start = datetime(y, m, d, hh, mm, tzinfo=ET)
    away, home = TEAM[r["away_team"]], TEAM[r["home_team"]]
    wk, wd = int(r["week"]), r["weekday"]
    venue = STADIUM_FIX.get(r["stadium"], r["stadium"])

    slot = ""
    if wd == "Thursday" and hh >= 19:
        slot = "Thursday Night Football"
    elif wd == "Monday":
        slot = "Monday Night Football"
    elif wd == "Sunday" and hh >= 20:
        slot = "Sunday Night Football"
    elif wd == "Sunday" and hh == 9:
        slot = "International - early morning US kick-off"
    if start.date() == datetime(2026, 11, 26).date():
        slot = (slot + " / " if slot else "") + "THANKSGIVING"
    if wd == "Wednesday" and wk == 1:
        slot = "SEASON OPENER (Wednesday night)"

    extra = f"\n\nINTERNATIONAL GAME\n{INTL[venue]}" if venue in INTL else ""
    market = ""
    if r["spread_line"] and r["total_line"]:
        sp = float(r["spread_line"])
        fav = home if sp > 0 else away
        market = (f"\n\nOpening line\n{fav} by {abs(sp)}  |  "
                  f"Total {r['total_line']}\n(Books post lines a few weeks "
                  f"out, so this appears on early-season games only.)")

    desc = (
        f"{LOGO[r['away_team']]} {away} @ {LOGO[r['home_team']]} {home}\n"
        f"Week {wk} - {start.strftime('%A %-d %B %Y')}\n\n"
        f"Kick-off\n{start.strftime('%-I:%M %p')} ET  |  "
        f"{start.astimezone(UTC).strftime('%H:%M')} UTC\n"
        + (f"\nSlot\n{slot}\n" if slot else "")
        + f"\nVenue\n{venue} ({r['roof']}, {r['surface']})\n"
        + ("\nDivision game\nYes - counts double in the standings.\n"
           if r["div_game"] == "1" else "")
        + f"\nCoaches\n{LOGO[r['away_team']]} {away}: {r['away_coach'] or 'TBC'}\n"
          f"{LOGO[r['home_team']]} {home}: {r['home_coach'] or 'TBC'}"
        + market + extra
        + "\n\nSunday afternoon kick-offs from Week 5 are subject to FLEX "
          "SCHEDULING - the league can move games in or out of primetime at "
          "about 12 days' notice."
    )
    emit(r["game_id"], f"{BALL} {LOGO[r['away_team']]} {away} @ "
         f"{LOGO[r['home_team']]} {home} (Wk {wk})", start, 195, desc,
         venue, f"Week {wk}")
    n_reg += 1

lines.append("END:VCALENDAR")
with open("../docs/nfl.ics", "w",
          encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print(f"Wrote {n_pre} preseason + {n_key} key dates + {n_reg} regular season "
      f"= {n_pre + n_key + n_reg} events")
