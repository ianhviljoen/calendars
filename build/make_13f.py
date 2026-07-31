#!/usr/bin/env python3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ET, UTC = ZoneInfo("America/New_York"), ZoneInfo("UTC")
FILE, CAM = "\U0001F4CB", "\U0001F4F8"

LAG = ("REMEMBER THE LAG. A 13F shows positions as of the QUARTER-END date, "
       "not the filing date - roughly six weeks stale on arrival. A fund that "
       "held something on the snapshot date may already be out of it. Good for "
       "spotting multi-quarter accumulation and understanding a manager's "
       "approach; useless as a short-term signal.")

WHAT = ("Long US equity positions only. No shorts, no bonds, no cash, no "
        "non-US listings, and confidential-treatment requests can hide "
        "positions temporarily.")

# (kind, label, quarter, snapshot, ET datetime, mins, confirmed, extra)
E = [
 ("deadline", "Q2 2026 holdings", "30 June 2026", (2026, 8, 14, 16, 0), 90, True,
  "Friday deadline, so no weekend roll-forward. Falls the same day as July "
  "retail sales and Michigan sentiment prelim."),
 ("snapshot", "Q3 2026", "30 September 2026", (2026, 9, 30, 16, 0), 30, True,
  "Positions held at this close are what appears in the November filings. "
  "Also quarter-end, so rebalancing flows are in the tape."),
 ("deadline", "Q3 2026 holdings", "30 September 2026", (2026, 11, 16, 16, 0), 90, True,
  "ROLLED FORWARD. The nominal 45-day date is Saturday 14 November, so the "
  "deadline moves to Monday 16 November. If your compliance calendar still "
  "says the 14th, it is wrong."),
 ("snapshot", "Q4 2026", "31 December 2026", (2026, 12, 31, 16, 0), 30, True,
  "Year-end snapshot - the one most widely cited in press coverage, and the "
  "basis for the February filings."),
 ("deadline", "Q4 2026 holdings", "31 December 2026", (2027, 2, 16, 16, 0), 90, False,
  "DOUBLE ROLL-FORWARD. The 45-day date is Sunday 14 February 2027, and "
  "Monday the 15th is Washington's Birthday, so it lands on Tuesday the 16th. "
  "Derived from the rule - the SEC FAQ publishes exact dates through 2028, "
  "worth confirming there."),
 ("snapshot", "Q1 2027", "31 March 2027", (2027, 3, 31, 16, 0), 30, False,
  "Quarter-end snapshot for the May filings."),
 ("deadline", "Q1 2027 holdings", "31 March 2027", (2027, 5, 17, 16, 0), 90, False,
  "ROLLED FORWARD - the 45-day date is Saturday 15 May 2027, so it moves to "
  "Monday the 17th. Derived from the rule."),
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
    "PRODID:-//Claude//SEC 13F Deadlines//EN", "CALSCALE:GREGORIAN",
    "X-WR-CALNAME:\U0001F4CB SEC 13F Deadlines",
    "X-APPLE-CALENDAR-COLOR:#546E7A",
    fold("X-WR-CALDESC:" + esc(
        "SEC Form 13F deadlines and the quarter-end snapshot dates the "
        "holdings actually refer to. Times Eastern, stored in UTC.")),
    "X-WR-TIMEZONE:America/New_York",
]
stamp = "20260729T090000Z"

for kind, label, snap, t, mins, conf, extra in E:
    start = datetime(*t, tzinfo=ET)
    end = start + timedelta(minutes=mins)
    tick = "" if conf else "~ "
    if kind == "deadline":
        title = f"13F Deadline - {label}"
        emoji = FILE
        body = (
            f"Filing deadline for Form 13F covering positions held on "
            f"{snap}.\n"
            f"\n"
            f"Timing\n"
            f"Filings trickle in from quarter-end onwards, but the big names "
            f"cluster in the final hours. EDGAR treats submissions after "
            f"5:30pm ET as filed the next business day, so 5:30pm is the "
            f"effective cut-off and the point at which the data set is "
            f"complete.\n"
            f"\n"
            f"Who files\n"
            f"Any institutional manager with at least $100m in Section 13(f) "
            f"securities. No extensions are granted; late filers are told to "
            f"submit as soon as possible.\n"
            f"\n"
            f"What you get\n{WHAT}\n"
            f"\n{LAG}\n"
            f"\n"
            f"Note Schedule 13G quarterly amendments share these same four "
            f"dates.\n"
            f"\n"
            f"Notes\n{extra}"
        )
    else:
        title = f"13F Snapshot Date - {label}"
        emoji = CAM
        body = (f"Quarter-end close. Positions held at this moment are what "
                f"gets disclosed in the 13F filings roughly six weeks later.\n"
                f"\n{extra}\n\n{LAG}")
    desc = (f"{title}\n{start.strftime('%A %-d %B %Y')}\n\n"
            f"Time\n{start.strftime('%-I:%M %p')} ET  |  "
            f"{start.astimezone(UTC).strftime('%H:%M')} UTC\n\n{body}")
    lines += [
        "BEGIN:VEVENT",
        f"UID:13f-{kind}-{start.strftime('%Y%m%d')}@claude-13f",
        f"DTSTAMP:{stamp}", f"DTSTART:{z(start)}", f"DTEND:{z(end)}",
        fold("SUMMARY:" + esc(f"{emoji} {tick}{title}")),
        fold("DESCRIPTION:" + esc(desc)),
        fold("CATEGORIES:" + esc("SEC Filings") + "," +
             esc("13F Deadline" if kind == "deadline" else "Snapshot")),
        "URL:https://www.sec.gov/divisions/investment/13ffaq.htm",
        "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
    ]

lines.append("END:VCALENDAR")
with open("../docs/sec-13f.ics", "w",
          encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print(f"Wrote {len(E)} events.")
