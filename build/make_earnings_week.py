#!/usr/bin/env python3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ET, UTC = ZoneInfo("America/New_York"), ZoneInfo("UTC")
MONEY = "\U0001F4B0"

N = {  # ticker -> company
 "AZN": "AstraZeneca", "APLD": "Applied Digital", "NVTS": "Navitas Semiconductor",
 "CLS": "Celestica", "CDNS": "Cadence Design", "AMKR": "Amkor Technology",
 "NUE": "Nucor", "RMBS": "Rambus", "BRO": "Brown & Brown", "WELL": "Welltower",
 "FFIV": "F5", "PYPL": "PayPal", "KO": "Coca-Cola", "BA": "Boeing",
 "UPS": "UPS", "GLW": "Corning", "SPGI": "S&P Global",
 "RCL": "Royal Caribbean", "UL": "Unilever", "AMT": "American Tower",
 "CORZ": "Core Scientific", "HLT": "Hilton", "SHW": "Sherwin-Williams",
 "GSK": "GSK", "CNC": "Centene", "JBLU": "JetBlue", "V": "Visa",
 "BE": "Bloom Energy", "STX": "Seagate", "WM": "Waste Management",
 "KLAC": "KLA Corp", "F": "Ford", "TER": "Teradyne", "ENPH": "Enphase Energy",
 "NXPI": "NXP Semiconductors", "CAKE": "Cheesecake Factory",
 "MDLZ": "Mondelez", "TLRY": "Tilray", "SWKS": "Skyworks",
 "CSGP": "CoStar Group", "SOFI": "SoFi Technologies", "VRT": "Vertiv",
 "PG": "Procter & Gamble", "LMND": "Lemonade", "APH": "Amphenol",
 "ADP": "ADP", "BSX": "Boston Scientific", "GEHC": "GE HealthCare",
 "GD": "General Dynamics", "GRMN": "Garmin", "FVRR": "Fiverr",
 "HUM": "Humana", "WING": "Wingstop", "UBS": "UBS", "RIO": "Rio Tinto",
 "MSFT": "Microsoft", "META": "Meta Platforms", "HOOD": "Robinhood",
 "ARM": "Arm Holdings", "QCOM": "Qualcomm", "SBUX": "Starbucks",
 "CMG": "Chipotle", "LRCX": "Lam Research", "FTNT": "Fortinet",
 "CVNA": "Carvana", "VICI": "VICI Properties", "FICO": "Fair Isaac",
 "VKTX": "Viking Therapeutics", "EA": "Electronic Arts",
 "SFM": "Sprouts Farmers Market", "MA": "Mastercard", "RACE": "Ferrari",
 "MO": "Altria", "SHEL": "Shell", "BMY": "Bristol Myers Squibb",
 "PGY": "Pagaya", "CROX": "Crocs", "HSY": "Hershey", "PWR": "Quanta Services",
 "KKR": "KKR", "CI": "Cigna", "BTI": "British American Tobacco",
 "EPD": "Enterprise Products", "SO": "Southern Company", "SIRI": "SiriusXM",
 "AAPL": "Apple", "AMZN": "Amazon", "COIN": "Coinbase", "MSTR": "Strategy",
 "RDDT": "Reddit", "RIVN": "Rivian", "TEM": "Tempus AI", "BBAI": "BigBear.ai",
 "RBLX": "Roblox", "FSLR": "First Solar", "NXT": "Nextracker",
 "AXTI": "AXT Inc", "MPWR": "Monolithic Power", "SYK": "Stryker",
 "DXCM": "Dexcom", "CVX": "Chevron", "XOM": "ExxonMobil", "ABBV": "AbbVie",
 "CCJ": "Cameco", "MRNA": "Moderna", "ETN": "Eaton", "MDT": "Medtronic",
 "LIN": "Linde", "CL": "Colgate-Palmolive", "ENB": "Enbridge",
 "TROW": "T. Rowe Price", "SATS": "EchoStar", "D": "Dominion Energy",
 "NVT": "nVent Electric", "LYB": "LyondellBasell",
}

WEEK = {
 (2026, 7, 27): {"BMO": ["AZN"],
   "AMC": ["APLD", "NVTS", "CLS", "CDNS", "AMKR", "NUE", "RMBS", "BRO",
           "WELL", "FFIV"]},
 (2026, 7, 28): {"BMO": ["PYPL", "KO", "BA", "UPS", "GLW", "SPGI", "RCL",
                         "UL", "AMT", "CORZ", "HLT", "SHW", "GSK", "CNC",
                         "JBLU"],
   "AMC": ["V", "BE", "STX", "WM", "KLAC", "F", "TER", "ENPH", "NXPI",
           "CAKE", "MDLZ", "TLRY", "SWKS", "CSGP"]},
 (2026, 7, 29): {"BMO": ["SOFI", "VRT", "PG", "LMND", "APH", "ADP", "BSX",
                         "GEHC", "GD", "GRMN", "FVRR", "HUM", "WING", "UBS",
                         "RIO"],
   "AMC": ["MSFT", "META", "HOOD", "ARM", "QCOM", "SBUX", "CMG", "LRCX",
           "FTNT", "CVNA", "VICI", "FICO", "VKTX", "EA", "SFM"]},
 (2026, 7, 30): {"BMO": ["MA", "RACE", "MO", "SHEL", "BMY", "PGY", "CROX",
                         "HSY", "PWR", "KKR", "CI", "BTI", "EPD", "SO",
                         "SIRI"],
   "AMC": ["AAPL", "AMZN", "COIN", "MSTR", "RDDT", "RIVN", "TEM", "BBAI",
           "RBLX", "FSLR", "NXT", "AXTI", "MPWR", "SYK", "DXCM"]},
 (2026, 7, 31): {"BMO": ["CVX", "XOM", "ABBV", "CCJ", "MRNA", "ETN", "MDT",
                         "LIN", "CL", "ENB", "TROW", "SATS", "D", "NVT",
                         "LYB"], "AMC": []},
}

# verified consensus, sourced 28 Jul 2026
CONS = {
 "MSFT": ("Q4 FY2026", "EPS $4.22-4.24  |  Revenue $87.5-87.7bn",
          "Call 5:30pm ET. Azure growth is the swing factor - it ran ~40% "
          "last quarter. Stock is ~31% below its record, so the bar is low "
          "but capex commentary matters more than the print."),
 "META": ("Q2 2026", "EPS $7.18-7.23  |  Revenue ~$60.2bn (+27% YoY)",
          "Call 5:00pm ET. Guidance was $58-61bn. Note the split: revenue "
          "+27% but underlying EPS growth only ~1%. Meta beat on both lines "
          "last quarter and still fell 6-7% purely on capex - full-year "
          "capex guidance is $125-145bn."),
 "AAPL": ("Fiscal Q3 2026", "EPS $1.88-1.89  |  Revenue $108.8-108.9bn",
          "Call 5:00pm ET. iPhone demand, Services momentum, China, and "
          "margin pressure from rising memory costs."),
 "AMZN": ("Q2 2026", "EPS ~$1.81-1.85  |  Revenue ~$196.0bn",
          "Call 5:00pm ET. AWS growth is the swing factor; North America "
          "segment revenue seen near $113.8bn. Watch full-year capex "
          "guidance."),
}

BIG = {"MSFT", "META", "AAPL", "AMZN", "V", "MA", "XOM", "CVX", "PG", "KO",
       "QCOM", "ARM", "SPGI", "LIN", "ABBV", "BA", "UPS", "SBUX", "MDLZ"}


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
    "PRODID:-//Claude//Earnings Week 27 Jul 2026//EN", "CALSCALE:GREGORIAN",
    "X-WR-CALNAME:Earnings - Week of 27 Jul 2026",
    "X-APPLE-CALENDAR-COLOR:#00897B",
    fold("X-WR-CALDESC:" + esc(
        "US earnings for the week of 27 July 2026. BMO = before open, "
        "AMC = after close. Times Eastern, stored in UTC.")),
    "X-WR-TIMEZONE:America/New_York",
]
stamp, seen, n = "20260728T090000Z", set(), 0

for (y, m, d), sessions in WEEK.items():
    for sess, tickers in sessions.items():
        for tk in tickers:
            name = N.get(tk, tk)
            if sess == "BMO":
                hh, mm = 7, 0
                when = ("BEFORE THE OPEN\nRelease usually 6:00-8:00am ET; "
                        "earnings call typically 8:30am ET.")
                tag = "BMO"
            else:
                hh, mm = 16, 5
                when = ("AFTER THE CLOSE\nRelease usually 4:05-4:30pm ET; "
                        "earnings call typically 5:00pm ET.")
                tag = "AMC"
            if tk in CONS:
                q, figs, note = CONS[tk]
                cons = (f"\n\nConsensus ({q})\n{figs}\n\n{note}")
                if tk == "MSFT":
                    hh, mm = 16, 5
            else:
                cons = ("\n\nConsensus\nNot looked up for this name. Check "
                        "the link below for current estimates.")
            start = datetime(y, m, d, hh, mm, tzinfo=ET)
            end = start + timedelta(minutes=30)
            star = " *" if tk in BIG else ""
            desc = (f"{tk} - {name}\n{start.strftime('%A %-d %B %Y')}\n\n"
                    f"Session\n{when}\n\n"
                    f"Scheduled time\n{start.strftime('%-I:%M %p')} ET  |  "
                    f"{start.astimezone(UTC).strftime('%H:%M')} UTC"
                    f"{cons}\n\n"
                    f"Link\nhttps://finance.yahoo.com/quote/{tk}\n\n"
                    f"Source: Earnings Hub week of 27 Jul 2026. Companies "
                    f"move dates at short notice - reconfirm on the day.")
            uid = f"earn-{tk}-{y}{m:02d}{d:02d}"
            while uid in seen:
                uid += "x"
            seen.add(uid)
            lines += [
                "BEGIN:VEVENT", f"UID:{uid}@claude-earnings",
                f"DTSTAMP:{stamp}", f"DTSTART:{z(start)}", f"DTEND:{z(end)}",
                fold("SUMMARY:" + esc(f"{MONEY} {tk}{star} - {name} ({tag})")),
                fold("DESCRIPTION:" + esc(desc)),
                fold("CATEGORIES:" + esc("Earnings") + "," + esc(tag)),
                f"URL:https://finance.yahoo.com/quote/{tk}",
                "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
            ]
            n += 1

# the week's IPO
start = datetime(2026, 7, 30, 9, 30, tzinfo=ET)
lines += [
    "BEGIN:VEVENT", "UID:ipo-jmke-20260730@claude-earnings",
    f"DTSTAMP:{stamp}", f"DTSTART:{z(start)}",
    f"DTEND:{z(start + timedelta(minutes=30))}",
    fold("SUMMARY:" + esc("\U0001F514 IPO: JMKE - Jersey Mike's Subs")),
    fold("DESCRIPTION:" + esc(
        "Jersey Mike's Subs Inc (JMKE)\nThursday 30 July 2026\n\n"
        "IPO expected to price and begin trading this day. Opening time is "
        "set by the exchange on the morning and is often well after 9:30am.\n\n"
        "Source: Earnings Hub week of 27 Jul 2026.")),
    fold("CATEGORIES:" + esc("Earnings") + "," + esc("IPO")),
    "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
]
n += 1
lines.append("END:VCALENDAR")

with open("../docs/earnings-week-27jul2026.ics", "w",
          encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print(f"Wrote {n} events ({len(CONS)} with verified consensus).")
