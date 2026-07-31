#!/usr/bin/env python3
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

ET, UTC = ZoneInfo("America/New_York"), ZoneInfo("UTC")


def third_friday(y, m):
    d, c = date(y, m, 1), 0
    while True:
        if d.weekday() == 4:
            c += 1
            if c == 3:
                return d
        d += timedelta(days=1)


def nth_friday(y, m, n):
    d, c = date(y, m, 1), 0
    while True:
        if d.weekday() == 4:
            c += 1
            if c == n:
                return d
        d += timedelta(days=1)


CALS = {}


def cal(key, name, colour, desc):
    CALS[key] = dict(name=name, colour=colour, desc=desc, events=[])


def ev(key, emoji, title, t, mins, note):
    CALS[key]["events"].append((emoji, title, t, mins, note))


# ============================================================
cal("futures-roll", "Futures Roll", "#455A64",
    "Quarterly roll and final settlement for CME equity index futures "
    "(ES, NQ, YM, RTY).")

for m, q in [(9, "Sep"), (12, "Dec")]:
    tf = third_friday(2026, m)
    roll = tf - timedelta(days=8)
    ev("futures-roll", "\U0001F504", f"Futures Roll - {q} to "
       f"{'Dec' if m == 9 else 'Mar 2027'} contract",
       (roll.year, roll.month, roll.day, 9, 30), 390,
       f"Roll date for ES, NQ, YM and RTY - eight days before expiry. Volume "
       f"and open interest shift to the next contract from here, so quoted "
       f"'front month' prices change reference. Anything held past this needs "
       f"rolling or it settles on {tf.strftime('%-d %b')}.")
    ev("futures-roll", "\U0001F3C1", f"Futures Final Settlement - {q} contract",
       (tf.year, tf.month, tf.day, 9, 30), 30,
       "Expiring quarterly contracts settle to the Special Opening Quotation "
       "calculated from the opening prices of the index constituents. The SOQ "
       "can print well away from where the future last traded.")

# ============================================================
cal("options-expiry", "Options Expiration", "#F57C00",
    "Monthly and quarterly equity/index options expiration plus VIX "
    "settlement.")

for m in (8, 9, 10, 11, 12):
    tf = third_friday(2026, m)
    quad = m in (9, 12)
    ev("options-expiry", "\u26A1",
       "QUADRUPLE WITCHING" if quad else "Monthly Options Expiration",
       (tf.year, tf.month, tf.day, 16, 0), 30,
       ("Index futures, index options, single-stock options and single-stock "
        "futures all expire together. Routinely the highest-volume session of "
        "the quarter, with an enormous closing auction. Index rebalances trade "
        "at this close too, so the final hour is flow rather than information."
        if quad else
        "Third-Friday equity and index options expiry. Dealer gamma unwinds "
        "around pinned strikes, and the week after monthly expiry tends to "
        "carry higher realised volatility."))
    ny, nm = (2026, m + 1) if m < 12 else (2027, 1)
    vix = third_friday(ny, nm) - timedelta(days=30)
    extra = ""
    if vix == date(2026, 9, 16):
        extra = "\n\nFOMC decision the same afternoon."
    if vix == date(2026, 11, 18):
        extra = "\n\nFOMC minutes at 2:00pm the same day."
    ev("options-expiry", "\u26A1", "VIX Expiration",
       (vix.year, vix.month, vix.day, 9, 30), 30,
       f"VIX futures and options settle on the opening SOQ. Falls on the "
       f"Wednesday 30 days before the following month's third Friday. "
       f"Volatility positions unwind into this and the settlement print can "
       f"sit far from where VIX last traded.{extra}")

# ============================================================
cal("rebalance-sp500", "S&P 500 Rebalance", "#CC0000",
    "S&P Dow Jones Indices quarterly rebalance of the S&P 500.")

for m, q in [(9, "September"), (12, "December")]:
    ann = nth_friday(2026, m, 1)
    tf = third_friday(2026, m)
    eff = tf + timedelta(days=3)
    ev("rebalance-sp500", "\U0001F4E2", f"S&P 500 {q} Rebalance - announcement",
       (ann.year, ann.month, ann.day, 17, 15), 45,
       "S&P DJI normally announces quarterly constituent changes on the first "
       "Friday of the rebalance month, after the close. Added names typically "
       "gap on the announcement, not on the effective date. Date derived from "
       "that pattern - S&P confirms nearer the time.")
    ev("rebalance-sp500", "\u267B", f"S&P 500 {q} Rebalance - trade at close",
       (tf.year, tf.month, tf.day, 16, 0), 30,
       "Index funds execute the rebalance in the closing auction of the third "
       "Friday, alongside quadruple witching. This is where the volume is.")
    ev("rebalance-sp500", "\u267B", f"S&P 500 {q} Rebalance - effective",
       (eff.year, eff.month, eff.day, 9, 30), 30,
       f"Changes take effect prior to the open on the Monday after the third "
       f"Friday. The June 2026 cycle ran the same way - announced 5 June, "
       f"effective before the open on 22 June.")

# ============================================================
cal("rebalance-dow", "Dow Jones Rebalance", "#0F2B5B",
    "Dow Jones Industrial Average quarterly share and divisor updates.")

for m, q in [(9, "September"), (12, "December")]:
    tf = third_friday(2026, m)
    eff = tf + timedelta(days=3)
    ev("rebalance-dow", "\u267B", f"DJIA {q} Rebalance - effective",
       (eff.year, eff.month, eff.day, 9, 30), 30,
       "Quarterly share-count and divisor updates for the Dow, run by S&P DJI "
       "on the same third-Friday cycle as the S&P 500.\n\nNote the Dow is "
       "price-weighted with only 30 members, and COMPONENT changes are made "
       "ad hoc by committee rather than on this schedule - they can be "
       "announced at any time, usually triggered by a merger or a split.")

# ============================================================
cal("rebalance-nasdaq", "Nasdaq-100 Rebalance", "#0796D3",
    "Nasdaq-100 quarterly rank-based reviews and the December annual "
    "reconstitution.")

tf9 = third_friday(2026, 9)
ev("rebalance-nasdaq", "\u267B", "Nasdaq-100 September Review - effective",
   ((tf9 + timedelta(days=3)).year, (tf9 + timedelta(days=3)).month,
    (tf9 + timedelta(days=3)).day, 9, 30), 30,
   "Quarterly rank-based review, effective at the open of the first trading "
   "day after the third Friday. From 2026 the NDX runs this review every "
   "quarter, so membership can change year-round rather than only in December.")
ev("rebalance-nasdaq", "\U0001F4E2",
   "Nasdaq-100 Annual Reconstitution - announcement",
   (2026, 12, 11, 20, 0), 30,
   "Nasdaq publishes the annual reconstitution in mid-December, normally the "
   "second Friday after the close. Date derived from that pattern.")
tf12 = third_friday(2026, 12)
ev("rebalance-nasdaq", "\u267B",
   "Nasdaq-100 Annual Reconstitution + Q4 Review - effective",
   ((tf12 + timedelta(days=3)).year, (tf12 + timedelta(days=3)).month,
    (tf12 + timedelta(days=3)).day, 9, 30), 30,
   "The annual reconstitution and the quarterly rebalance go effective on the "
   "same morning. The largest scheduled NDX flow of the year.")

# ============================================================
cal("rebalance-russell", "Russell Reconstitution", "#582C83",
    "FTSE Russell US Indexes - the first ever December semi-annual "
    "reconstitution.")

ev("rebalance-russell", "\U0001F4CB", "Russell Rank Day (December cycle)",
   (2026, 10, 30, 16, 0), 30,
   "Last business day of October - the cut-off on which index eligibility and "
   "market caps are assessed for the December reconstitution. Preliminary "
   "constituent lists follow in the weeks after.")
ev("rebalance-russell", "\u267B",
   "Russell Semi-Annual Reconstitution - effective",
   (2026, 12, 11, 16, 0), 30,
   "FIRST EVER December reconstitution of the Russell US Indexes. Effective "
   "after the close on the second Friday of December, with changes reflected "
   "from the open on Monday 14 December.\n\nRussell moved from annual to "
   "semi-annual from 2026 - June stays on the fourth Friday, and this is the "
   "new second date. Around $12 trillion is benchmarked to Russell US "
   "indexes, though flows here are expected to be smaller than June's. "
   "December style-index changes are limited to new additions and size-driven "
   "moves.")
ev("rebalance-russell", "\u267B", "Russell Reconstitution - reflected at open",
   (2026, 12, 14, 9, 30), 30,
   "New Russell index composition is live from this open.")


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
for key, c in CALS.items():
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0",
        f"PRODID:-//Claude//{c['name']}//EN", "CALSCALE:GREGORIAN",
        f"X-WR-CALNAME:{c['name']}",
        f"X-APPLE-CALENDAR-COLOR:{c['colour']}",
        fold("X-WR-CALDESC:" + esc(c["desc"])),
        "X-WR-TIMEZONE:America/New_York",
    ]
    seen = set()
    for emoji, title, t, mins, note in sorted(c["events"], key=lambda x: x[2]):
        start = datetime(*t, tzinfo=ET)
        end = start + timedelta(minutes=mins)
        desc = (f"{title}\n{start.strftime('%A %-d %B %Y')}\n\n"
                f"Time\n{start.strftime('%-I:%M %p')} ET  |  "
                f"{start.astimezone(UTC).strftime('%H:%M')} UTC\n\n"
                f"Notes\n{note}")
        uid = f"{key}-{start.strftime('%Y%m%d%H%M')}-{abs(hash(title)) % 99999}"
        while uid in seen:
            uid += "x"
        seen.add(uid)
        lines += [
            "BEGIN:VEVENT", f"UID:{uid}@claude-mkt", f"DTSTAMP:{stamp}",
            f"DTSTART:{z(start)}", f"DTEND:{z(end)}",
            fold("SUMMARY:" + esc(f"{emoji} {title}")),
            fold("DESCRIPTION:" + esc(desc)),
            fold("CATEGORIES:" + esc(c["name"])),
            "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    with open(f"../docs/{key}.ics", "w",
              encoding="utf-8", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")
    print(f"{c['name']:<28} {len(c['events']):>2} events  {c['colour']}")
