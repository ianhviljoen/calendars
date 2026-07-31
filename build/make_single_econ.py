#!/usr/bin/env python3
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

ET, UTC = ZoneInfo("America/New_York"), ZoneInfo("UTC")

TIERS = {
    "high":   ("\U0001F534", "#D50000", "High impact"),
    "medium": ("\U0001F7E1", "#F6BF26", "Medium impact"),
    "low":    ("\U0001F7E2", "#0B8043", "Low impact"),
}

OMB = "Official - OMB/OIRA Principal Federal Economic Indicators schedule 2026."
FEDSRC = "Official - Federal Reserve FOMC calendar."
ISMSRC = "Official - ISM PMI Reports release calendar."
NARSRC = "Official - NAR Statistical News Release Schedule 2026."
DER = "DERIVED from the usual release pattern - not an published date."

E = []


def add(tier, name, t, src, note, mins=30):
    E.append((tier, name, t, src, note, mins))


# ---------------- FED ----------------
for (y, m, d), sep in [((2026, 7, 29), False), ((2026, 9, 16), True),
                       ((2026, 10, 28), False), ((2026, 12, 9), True)]:
    x = " Dot plot and Summary of Economic Projections land with it." if sep else ""
    add("high", "Fed Interest Rate Decision", (y, m, d, 14, 0), FEDSRC,
        f"Policy statement at 2:00pm ET.{x}", 30)
    add("high", "Fed Press Conference", (y, m, d, 14, 30), FEDSRC,
        "Chair press conference. Frequently moves the index more than the "
        "decision itself.", 60)
    mn = date(y, m, d) + timedelta(weeks=3)
    add("medium", "FOMC Minutes", (mn.year, mn.month, mn.day, 14, 0), DER,
        f"Minutes of the {date(y, m, d).strftime('%-d %B')} meeting. Published "
        f"about three weeks after each decision.")

# ---------------- CPI: four separate lines ----------------
CPI = [(8, 12, "July"), (9, 11, "August"), (10, 14, "September"),
       (11, 10, "October"), (12, 10, "November")]
for m, d, ref in CPI:
    for line in ["Inflation Rate MoM", "Inflation Rate YoY",
                 "Core Inflation Rate MoM", "Core Inflation Rate YoY"]:
        add("high", f"{line} ({ref})", (2026, m, d, 8, 30), OMB,
            f"Part of the BLS Consumer Price Index release for {ref} 2026. "
            f"All four CPI lines print together at 8:30am ET.")

for m, d, ref in [(8, 13, "July"), (9, 10, "August"), (10, 15, "September"),
                  (11, 13, "October"), (12, 15, "November")]:
    add("medium", f"PPI MoM ({ref})", (2026, m, d, 8, 30), OMB,
        f"Producer Price Index for {ref} 2026 - wholesale inflation. Lands a "
        f"day either side of CPI and feeds the PCE estimate.")

# ---------------- Employment Situation ----------------
for m, d, ref in [(8, 7, "July"), (9, 4, "August"), (10, 2, "September"),
                  (11, 6, "October"), (12, 4, "November")]:
    add("high", f"Non Farm Payrolls ({ref})", (2026, m, d, 8, 30), OMB,
        f"BLS Employment Situation for {ref} 2026.")
    add("high", f"Unemployment Rate ({ref})", (2026, m, d, 8, 30), OMB,
        f"Released in the same 8:30am Employment Situation report as payrolls.")

# ---------------- BEA: Personal Income & Outlays + GDP ----------------
PIO = [(7, 30, "June"), (8, 26, "July"), (9, 30, "August"),
       (10, 29, "September"), (11, 25, "October"), (12, 23, "November")]
for m, d, ref in PIO:
    add("high", f"Core PCE Price Index MoM ({ref})", (2026, m, d, 8, 30), OMB,
        f"The Fed's target inflation gauge, in the {ref} 2026 Personal Income "
        f"and Outlays report.")
    add("medium", f"Personal Spending MoM ({ref})", (2026, m, d, 8, 30), OMB,
        f"Same release as Core PCE. Feeds GDP nowcasts.")
    add("low", f"Personal Income MoM ({ref})", (2026, m, d, 8, 30), OMB,
        f"Same release as Core PCE. Rarely trades on its own.")

for m, d, q in [(7, 30, "Q2 2026"), (10, 29, "Q3 2026")]:
    add("high", f"GDP Growth Rate QoQ Adv ({q})", (2026, m, d, 8, 30), OMB,
        f"First estimate of {q} GDP. The advance print is the one that moves.")
for m, d, q in [(8, 26, "Q2 2026"), (11, 25, "Q3 2026")]:
    add("low", f"GDP Growth Rate QoQ 2nd Est ({q})", (2026, m, d, 8, 30), OMB,
        f"Second estimate of {q} GDP. Revisions are usually small and the "
        f"data is already stale.")

# ---------------- Census ----------------
for m, d, ref in [(8, 14, "July"), (9, 16, "August"), (10, 15, "September"),
                  (11, 17, "October"), (12, 16, "November")]:
    add("high", f"Retail Sales MoM ({ref})", (2026, m, d, 8, 30), OMB,
        f"Advance retail and food services sales for {ref} 2026. The consumer "
        f"read - drives discretionary names and the broad tape.")

for m, d, ref in [(8, 18, "July"), (9, 17, "August"), (10, 20, "September"),
                  (11, 18, "October"), (12, 17, "November")]:
    add("medium", f"Housing Starts ({ref})", (2026, m, d, 8, 30), OMB,
        f"New Residential Construction, {ref} 2026.")
    add("medium", f"Building Permits Prel ({ref})", (2026, m, d, 8, 30), OMB,
        f"Preliminary permits, same 8:30am release as housing starts. The more "
        f"forward-looking of the two.")

for m, d, ref in [(8, 26, "July"), (9, 25, "August"), (10, 27, "September"),
                  (11, 25, "October"), (12, 23, "November")]:
    add("medium", f"Durable Goods Orders MoM ({ref})", (2026, m, d, 8, 30), OMB,
        f"Advance report for {ref} 2026. Watch the core capital goods "
        f"ex-aircraft line rather than the volatile headline.")

# ---------------- ISM (official calendar) ----------------
for m, d, ref in [(8, 3, "July"), (9, 1, "August"), (10, 1, "September"),
                  (11, 2, "October"), (12, 1, "November")]:
    add("high", f"ISM Manufacturing PMI ({ref})", (2026, m, d, 10, 0), ISMSRC,
        f"First business day of the month, 10:00am ET. Above 50 = expansion.")
for m, d, ref in [(8, 5, "July"), (9, 3, "August"), (10, 5, "September"),
                  (11, 4, "October"), (12, 3, "November")]:
    add("high", f"ISM Services PMI ({ref})", (2026, m, d, 10, 0), ISMSRC,
        f"Third business day, 10:00am ET. Services is around 70% of the "
        f"economy, so this usually outweighs the manufacturing print.")

# ---------------- NAR (official calendar) ----------------
for m, d, ref in [(8, 11, "July"), (9, 10, "August"), (10, 13, "September"),
                  (11, 12, "October"), (12, 9, "November")]:
    add("low", f"Existing Home Sales ({ref})", (2026, m, d, 10, 0), NARSRC,
        f"National Association of Realtors, {ref} 2026. All NAR releases are "
        f"10:00am ET.")


# ---------------- derived: JOLTS + Michigan ----------------
def nth_weekday(y, m, wd, n):
    d, c = date(y, m, 1), 0
    while True:
        if d.weekday() == wd:
            c += 1
            if c == n:
                return d
        d += timedelta(days=1)


for m in (8, 9, 10, 11, 12):
    j = nth_weekday(2026, m, 1, 1)
    add("medium", "JOLTs Job Openings", (j.year, j.month, j.day, 10, 0), DER,
        "Job Openings and Labor Turnover Survey, BLS, 10:00am ET. Lags the "
        "reference month by about five weeks and is not on the OMB "
        "principal-indicator schedule.")
    u = nth_weekday(2026, m, 4, 2)
    add("medium", "Michigan Consumer Sentiment Prel",
        (u.year, u.month, u.day, 10, 0), DER,
        "University of Michigan preliminary reading, normally the second "
        "Friday at 10:00am ET. Watch the inflation-expectations component - "
        "that is the part the Fed quotes.")



CAT = [
    ("FOMC Minutes",        "\U0001F4DD", "Fed"),
    ("Fed ",                "\U0001F3DB", "Fed"),
    ("ISM ",                "\U0001F3ED", "PMI"),
    ("GDP",                 "\U0001F4CA", "Growth"),
    ("JOLT",                "\U0001F477", "Labour"),
    ("Non Farm Payrolls",   "\U0001F477", "Labour"),
    ("Unemployment Rate",   "\U0001F477", "Labour"),
    ("Core PCE",            "\U0001F4C8", "Inflation"),
    ("Inflation Rate",      "\U0001F4C8", "Inflation"),
    ("PPI",                 "\U0001F4C8", "Inflation"),
    ("Retail Sales",        "\U0001F6D2", "Consumer"),
    ("Personal Spending",   "\U0001F6D2", "Consumer"),
    ("Michigan",            "\U0001F642", "Consumer"),
    ("Personal Income",     "\U0001F4B5", "Income"),
    ("Durable Goods",       "\U0001F4E6", "Manufacturing"),
    ("Housing Starts",      "\U0001F3E0", "Housing"),
    ("Building Permits",    "\U0001F3E0", "Housing"),
    ("Existing Home Sales", "\U0001F3E0", "Housing"),
]


def category(name):
    for key, emoji, label in CAT:
        if key in name:
            return emoji, label
    return "\U0001F4C5", "Other"



PRIOR = {
 "Fed Interest Rate Decision|2026-07-29": "Previous 3.75%  |  Consensus 3.75%  |  Forecast 3.75%",
 "Core PCE Price Index MoM (June)": "Previous 0.3%  |  Consensus 0.2%  |  Forecast 0.1%",
 "GDP Growth Rate QoQ Adv (Q2 2026)": "Previous 2.1%  |  Consensus 2.1%  |  Forecast 2.2%",
 "Personal Income MoM (June)": "Previous 0.7%  |  Consensus 0.3%  |  Forecast 0.4%",
 "Personal Spending MoM (June)": "Previous 0.7%  |  Consensus 0.3%  |  Forecast 0.2%",
 "ISM Manufacturing PMI (July)": "Previous 53.3  |  Forecast 52.8",
 "JOLTs Job Openings|2026-08-04": "Previous 7.594M  |  Forecast 6.9M",
 "ISM Services PMI (July)": "Previous 54.0",
 "Non Farm Payrolls (July)": "Previous 57K",
 "Unemployment Rate (July)": "Previous 4.2%",
 "Existing Home Sales (July)": "Previous 4.09M",
 "Core Inflation Rate MoM (July)": "Previous 0%",
 "Core Inflation Rate YoY (July)": "Previous 2.6%",
 "Inflation Rate MoM (July)": "Previous -0.4%",
 "Inflation Rate YoY (July)": "Previous 3.5%",
 "PPI MoM (July)": "Previous -0.3%",
 "Retail Sales MoM (July)": "Previous 0.2%",
 "Building Permits Prel (July)": "Previous 1.374M",
 "Housing Starts (July)": "Previous 1.427M",
}


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


stamp = "20260728T090000Z"
rows = sorted(E, key=lambda x: x[2])
lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0",
    "PRODID:-//Claude//US Economic Data 2026//EN", "CALSCALE:GREGORIAN",
    "X-WR-CALNAME:US Economic Data 2026",
    fold("X-WR-CALDESC:" + esc(
        "US economic releases with exact Eastern times, stored in UTC so they "
        "render in your local zone.")),
    "X-WR-TIMEZONE:America/New_York",
]
seen = set()
for tier, name, t, srcnote, note, mins in rows:
    start = datetime(*t, tzinfo=ET)
    end = start + timedelta(minutes=mins)
    cat_emoji, cat_label = category(name)
    fig = PRIOR.get(f"{name}|{start.date()}") or PRIOR.get(name)
    figblock = f"\n\nFigures (as of 28 Jul 2026)\n{fig}" if fig else ""
    desc = (f"{cat_emoji} {name}\n{start.strftime('%A %-d %B %Y')}\n\n"
            f"Type\n{cat_label}\n\n"
            f"Release time\n{start.strftime('%-I:%M %p')} ET  |  "
            f"{start.astimezone(UTC).strftime('%H:%M')} UTC"
            f"{figblock}\n\n"
            f"Date status\n{srcnote}\n\nNotes\n{note}")
    uid = f"econ-{start.strftime('%Y%m%d%H%M')}-{abs(hash(name)) % 999999}"
    while uid in seen:
        uid += "x"
    seen.add(uid)
    lines += [
        "BEGIN:VEVENT", f"UID:{uid}@claude-econ", f"DTSTAMP:{stamp}",
        f"DTSTART:{z(start)}", f"DTEND:{z(end)}",
        fold("SUMMARY:" + esc(f"{cat_emoji} {name}")),
        fold("DESCRIPTION:" + esc(desc)),
        fold("CATEGORIES:" + esc("US Economic Data") + "," + esc(cat_label)),
        "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
    ]
lines.append("END:VCALENDAR")
with open("../docs/us-economic-data-2026.ics", "w",
          encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print(f"Wrote {len(rows)} events, {len([r for r in rows if PRIOR.get(r[1])])} "
      f"with consensus figures.")
