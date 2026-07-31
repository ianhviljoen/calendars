#!/usr/bin/env python3
"""Upcoming SpaceX launches -> docs/spacex-launches.ics

Reads launches.json (Launch Library 2, /launch/upcoming/), which update.sh
downloads. All times are UTC in the source and stored as UTC here.

IMPORTANT: LL2 parks vaguely-scheduled launches on placeholder dates - a whole
year's worth of "sometime in Q2 2027" missions all sit on 30 June 2027. Those
are dropped. Only launches with day-level precision or better are included.
"""
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

UTC = ZoneInfo("UTC")
ROCKET = "\U0001F680"

# Vague precisions get placeholder dates in LL2 (a whole quarter's launches
# dumped on one day), so they are excluded. Anything sharper than a day gets a
# real time; day-level becomes an all-day entry. Using a denylist rather than an
# allowlist so new precision names do not silently drop launches.
VAGUE_WORDS = ("week", "month", "quarter", "half", "year")


def bucket(precision_name):
    p = (precision_name or "").strip().lower()
    if not p or any(w in p for w in VAGUE_WORDS):
        return None                   # skip
    return "day" if p == "day" else "timed"

# status abbrev -> plain english
STATUS = {
    "Go": "Go for launch - date and time confirmed",
    "TBC": "To be confirmed - date is likely but not final",
    "TBD": "To be determined - date is a rough estimate",
    "Hold": "ON HOLD - launch paused",
    "Success": "Launched",
    "Failure": "Launch failed",
    "Partial Failure": "Partial failure",
    "In Flight": "In flight",
}


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


def clip(text, n=600):
    if not text:
        return ""
    text = " ".join(text.split())
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + "..."


data = json.load(open("launches.json", encoding="utf-8"))
results = data.get("results", [])

lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0",
    "PRODID:-//Claude//Rocket Launches//EN", "CALSCALE:GREGORIAN",
    f"X-WR-CALNAME:{ROCKET} SpaceX Launches",
    "X-APPLE-CALENDAR-COLOR:#0B3D91",
    fold("X-WR-CALDESC:" + esc(
        "Upcoming SpaceX launches - Falcon 9, Falcon Heavy and Starship - "
        "from the Launch Library 2 API. Only launches with a real date are "
        "included; vaguely scheduled missions are left out. Times UTC.")),
    "X-WR-TIMEZONE:UTC",
]
stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
n_timed = n_day = n_skipped = 0

for L in results:
    if "spacex" not in ((L.get("launch_service_provider") or {})
                        .get("name", "")).lower():
        n_skipped += 1
        continue

    prec = ((L.get("net_precision") or {}).get("name") or "").strip()
    kind = bucket(prec)
    if kind is None:
        n_skipped += 1
        continue

    net = L.get("net")
    if not net:
        n_skipped += 1
        continue
    start = datetime.fromisoformat(net.replace("Z", "+00:00")).astimezone(UTC)
    if start < datetime.now(UTC) - timedelta(hours=12):
        n_skipped += 1
        continue

    name = L.get("name") or "Launch"
    rocket = ((L.get("rocket") or {}).get("configuration") or {})
    provider = (L.get("launch_service_provider") or {}).get("name", "Unknown")
    mission = L.get("mission") or {}
    pad = L.get("pad") or {}
    loc = (pad.get("location") or {})
    status = (L.get("status") or {})
    orbit = ((mission.get("orbit") or {}).get("name") or "")

    where = ", ".join(x for x in [pad.get("name"), loc.get("name")]
                      if x and x != "Unknown Pad")
    if not where:
        where = loc.get("name") or "Location TBC"

    body = [f"{name}", ""]
    body.append("Status")
    body.append(STATUS.get(status.get("abbrev", ""),
                           status.get("name", "Unknown")))
    body.append("")
    if kind == "timed":
        body.append("Lift-off")
        body.append(f"{start.strftime('%H:%M')} UTC, "
                    f"{start.strftime('%A %-d %B %Y')}")
    else:
        body.append("Lift-off")
        body.append(f"{start.strftime('%A %-d %B %Y')} - time not yet set")
    body += ["", "Provider", provider, "", "Site", where]
    if orbit:
        body += ["", "Orbit", orbit]
    if mission.get("description"):
        body += ["", "Mission", clip(mission["description"])]
    body += ["", "LAUNCH DATES SLIP CONSTANTLY - weather, technical holds and "
             "range availability move them, often by days and sometimes by "
             "hours on the day itself. This calendar rebuilds daily, but "
             "always check before setting an alarm."]

    uid = f"launch-{L.get('id','x')}@claude-launches"
    if kind == "timed":
        dt = [f"DTSTART:{z(start)}",
              f"DTEND:{z(start + timedelta(hours=1))}"]
        n_timed += 1
    else:
        d = start.date()
        dt = [f"DTSTART;VALUE=DATE:{d.strftime('%Y%m%d')}",
              f"DTEND;VALUE=DATE:{(d + timedelta(days=1)).strftime('%Y%m%d')}"]
        n_day += 1

    lines += [
        "BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{stamp}", *dt,
        fold("SUMMARY:" + esc(f"{ROCKET} {name}")),
        fold("LOCATION:" + esc(where)),
        fold("DESCRIPTION:" + esc("\n".join(body))),
        fold("CATEGORIES:" + esc("SpaceX") + "," + esc(rocket.get("name", "Launch"))),
        "URL:https://nextspaceflight.com/launches/",
        "TRANSP:TRANSPARENT",
        "STATUS:" + ("CONFIRMED" if status.get("abbrev") == "Go"
                     else "TENTATIVE"),
        "END:VEVENT",
    ]

lines.append("END:VCALENDAR")
with open("../docs/spacex-launches.ics", "w", encoding="utf-8",
          newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print(f"Wrote {n_timed + n_day} launches ({n_timed} timed, {n_day} date-only); "
      f"skipped {n_skipped} with placeholder dates.")
