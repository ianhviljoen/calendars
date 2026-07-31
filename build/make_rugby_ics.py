#!/usr/bin/env python3
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

UTC = ZoneInfo("UTC")
TV = ("US broadcaster not confirmed at time of writing - check local listings. "
      "Confirmed elsewhere: ITV (UK), Virgin Media (IRE), TF1 (FRA), "
      "Stan Sport (AUS), Sky Sport (NZ), SuperSport (RSA).")

V = {  # venue -> (name, street, lat, lon, tz)
    "aviva": ("Aviva Stadium", "Lansdowne Rd, Dublin 4, D04 K5F9, Ireland", 53.334288, -6.227943, "Europe/Dublin"),
    "turin": ("Allianz Stadium", "Corso Gaetano Scirea 50, 10151 Torino TO, Italy", 45.109552, 7.641278, "Europe/Rome"),
    "murray": ("Scottish Gas Murrayfield", "Roseburn St, Edinburgh EH12 5PJ, UK", 55.942276, -3.241040, "Europe/London"),
    "princ": ("Principality Stadium", "Westgate St, Cardiff CF10 1NS, UK", 51.478209, -3.182634, "Europe/London"),
    "lyon": ("Groupama Stadium", "10 Av. Simone Veil, 69150 Decines-Charpieu, France", 45.765217, 4.982030, "Europe/Paris"),
    "twick": ("Allianz Stadium, Twickenham", "200 Whitton Rd, Twickenham TW2 7BA, UK", 51.455956, -0.341505, "Europe/London"),
    "sdf": ("Stade de France", "93200 Saint-Denis, France", 48.924475, 2.360144, "Europe/Paris"),
    "genoa": ("Stadio Luigi Ferraris", "Via Giovanni de Pra 1, 16139 Genova GE, Italy", 44.416500, 8.952519, "Europe/Rome"),
    "udine": ("Bluenergy Stadium", "Piazzale Repubblica Argentina 3, 33100 Udine UD, Italy", 46.081531, 13.199917, "Europe/Rome"),
    "velez": ("Estadio Jose Amalfitani", "Av. Juan Bautista Justo 9200, Buenos Aires, Argentina", -34.635353, -58.520689, "America/Argentina/Buenos_Aires"),
    "hanazono": ("Hanazono Rugby Stadium", "1-1-1 Matsubaraminami, Higashiosaka, Osaka 578-0923, Japan", 34.668953, 135.626324, "Asia/Tokyo"),
    "townsville": ("Queensland Country Bank Stadium", "2 Pride Cl, Railway Estate QLD 4810, Australia", -19.266081, 146.816540, "Australia/Brisbane"),
    "ellis": ("Ellis Park", "S Park Ln, New Doornfontein, Johannesburg 2094, South Africa", -26.197490, 28.060784, "Africa/Johannesburg"),
    "jujuy": ("Estadio 23 de Agosto", "Santa Barbara S/N, San Salvador de Jujuy, Argentina", -24.198553, -65.290886, "America/Argentina/Jujuy"),
    "dhl": ("DHL Stadium", "Fritz Sonnenberg Rd, Green Point, Cape Town 8051, South Africa", -33.903444, 18.411155, "Africa/Johannesburg"),
    "fnb": ("FNB Stadium", "Soccer City Ave, Nasrec, Johannesburg 2147, South Africa", -26.234757, 27.982655, "Africa/Johannesburg"),
    "mendoza": ("Estadio Malvinas Argentinas", "Bajada del Cerro s/n, M5500 Mendoza, Argentina", -32.889664, -68.880096, "America/Argentina/Mendoza"),
    "baltimore": ("M&T Bank Stadium", "1101 Russell St, Baltimore, MD 21230, USA", 39.277970, -76.622704, "America/New_York"),
    "optus": ("Optus Stadium", "333 Victoria Park Dr, Burswood WA 6100, Australia", -31.950749, 115.888799, "Australia/Perth"),
    "eden": ("Eden Park", "42 Reimers Ave, Mount Eden, Auckland 1024, New Zealand", -36.874973, 174.744764, "Pacific/Auckland"),
    "kingspark": ("Hollywoodbets Kings Park", "Jacko Jackson Dr, Stamford Hill, Durban 4025, South Africa", -29.824851, 31.029634, "Africa/Johannesburg"),
    "loftus": ("Loftus Versfeld", "416 Kirkness St, Arcadia, Pretoria 0007, South Africa", -25.753259, 28.222946, "Africa/Johannesburg"),
    "accor": ("Accor Stadium", "Edwin Flack Ave, Sydney Olympic Park NSW 2127, Australia", -33.847116, 151.063414, "Australia/Sydney"),
}

NC = "Nations Championship"
GR = "Rugby's Greatest Rivalry"

def U(y, m, d, hh, mm):
    return datetime(y, m, d, hh, mm, tzinfo=UTC)

# (uid, home, away, utc-datetime OR date for TBC, venue-key, competition, note)
M = [
    # ---- All Blacks tour of South Africa: provincial (non-Test) matches ----
    ("tour-stormers", "Stormers", "New Zealand", U(2026, 8, 7, 17, 0), "dhl", GR,
     "TOUR MATCH (not a Test). Opening game of the All Blacks' tour - their "
     "first full tour of South Africa since 1996."),
    ("tour-sharks", "Sharks", "New Zealand", U(2026, 8, 11, 17, 0), "kingspark", GR,
     "TOUR MATCH (not a Test), played midweek under lights in Durban."),
    ("tour-bulls", "Bulls", "New Zealand", U(2026, 8, 15, 17, 0), "loftus", GR,
     "TOUR MATCH (not a Test), at altitude in Pretoria."),
    ("tour-lions", "Lions", "New Zealand", U(2026, 8, 25, 17, 0), "ellis", GR,
     "TOUR MATCH (not a Test), played midweek between the first and second "
     "Tests, at the same ground as the first Test."),

    # ---- August-October bilaterals ----
    ("arg-rsa", "Argentina", "South Africa", U(2026, 8, 8, 19, 0), "velez", "Test match",
     "Standalone Test in Buenos Aires with a 26-man Springbok squad; the rest "
     "stay home to prep for the All Blacks. SA Rugby quotes 21:00 SAST - worth "
     "reconfirming nearer the date."),
    ("jpn-aus-1", "Japan", "Australia", U(2026, 8, 8, 11, 15), "hanazono", "Test match",
     "Leg one of a home-and-away series. Les Kiss's first Test in charge of the Wallabies."),
    ("aus-jpn-2", "Australia", "Japan", U(2026, 8, 15, 5, 0), "townsville", "Flight Centre Series",
     "Leg two of the home-and-away series with Japan."),
    ("rsa-nzl-1", "South Africa", "New Zealand", U(2026, 8, 22, 15, 0), "ellis", GR,
     "FIRST TEST. New Zealand's first full tour of South Africa in 30 years. "
     "17:00 local."),
    ("arg-aus-1", "Argentina", "Australia", U(2026, 8, 29, 19, 0), "jujuy", "Puma Trophy",
     "First of two Tests in Argentina for the Puma Trophy."),
    ("rsa-nzl-2", "South Africa", "New Zealand", U(2026, 8, 29, 15, 0), "dhl", GR,
     "SECOND TEST. 17:00 local in Cape Town."),
    ("arg-aus-2", "Argentina", "Australia", U(2026, 9, 5, 19, 0), "mendoza", "Puma Trophy",
     "Second Test of the Puma Trophy series."),
    ("rsa-nzl-3", "South Africa", "New Zealand", U(2026, 9, 5, 15, 0), "fnb", GR,
     "THIRD TEST. 17:00 local; last match on South African soil."),
    ("rsa-nzl-4", "South Africa", "New Zealand", U(2026, 9, 12, 15, 5), "baltimore", GR,
     "FOURTH TEST, at a neutral venue in the United States - 11:05 local in "
     "Baltimore, timed for a South African evening audience."),
    ("aus-rsa", "Australia", "South Africa", U(2026, 9, 27, 9, 30), "optus", "Mandela Challenge Plate",
     "One-off Test for the Mandela Challenge Plate."),
    ("nzl-aus-bled1", "New Zealand", "Australia", U(2026, 10, 10, 5, 10), "eden", "Bledisloe Cup",
     "Bledisloe Cup first Test. Australia have not won at Eden Park since 1986. "
     "Kick-off quoted by Rugby Australia as 3:10pm AEST - confirm nearer the date."),
    ("aus-nzl-bled2", "Australia", "New Zealand", U(2026, 10, 17, 4, 45), "accor", "Bledisloe Cup",
     "Bledisloe Cup second Test and a potential decider. "
     "Kick-off quoted by Rugby Australia as 3:45pm AEST - confirm nearer the date."),

    # ---- Nations Championship, Northern Hemisphere Series ----
    ("nc-ire-arg", "Ireland", "Argentina", U(2026, 11, 6, 20, 10), "aviva", NC, "Round 4."),
    ("nc-ita-rsa", "Italy", "South Africa", U(2026, 11, 7, 11, 40), "turin", NC, "Round 4."),
    ("nc-sco-nzl", "Scotland", "New Zealand", U(2026, 11, 7, 14, 10), "murray", NC, "Round 4."),
    ("nc-wal-jpn", "Wales", "Japan", U(2026, 11, 7, 16, 40), "princ", NC, "Round 4."),
    ("nc-fra-fij", "France", "Fiji", U(2026, 11, 7, 20, 10), "lyon", NC, "Round 4."),
    ("nc-eng-aus", "England", "Australia", U(2026, 11, 8, 15, 10), "twick", NC, "Round 4."),
    ("nc-fra-rsa", "France", "South Africa", U(2026, 11, 13, 20, 10), "sdf", NC, "Round 5."),
    ("nc-ita-arg", "Italy", "Argentina", U(2026, 11, 14, 11, 40), "genoa", NC, "Round 5."),
    ("nc-wal-nzl", "Wales", "New Zealand", U(2026, 11, 14, 14, 10), "princ", NC, "Round 5."),
    ("nc-eng-jpn", "England", "Japan", U(2026, 11, 14, 16, 40), "twick", NC, "Round 5."),
    ("nc-ire-fij", "Ireland", "Fiji", U(2026, 11, 14, 20, 10), "aviva", NC, "Round 5."),
    ("nc-sco-aus", "Scotland", "Australia", U(2026, 11, 15, 15, 10), "murray", NC, "Round 5."),
    ("nc-eng-nzl", "England", "New Zealand", U(2026, 11, 21, 14, 10), "twick", NC, "Round 6."),
    ("nc-sco-jpn", "Scotland", "Japan", U(2026, 11, 21, 14, 10), "murray", NC, "Round 6."),
    ("nc-ire-rsa", "Ireland", "South Africa", U(2026, 11, 21, 16, 40), "aviva", NC, "Round 6."),
    ("nc-ita-fij", "Italy", "Fiji", U(2026, 11, 21, 16, 40), "udine", NC, "Round 6."),
    ("nc-fra-arg", "France", "Argentina", U(2026, 11, 21, 20, 10), "sdf", NC, "Round 6."),
    ("nc-wal-aus", "Wales", "Australia", U(2026, 11, 21, 20, 10), "princ", NC, "Round 6."),
]

FINALS = [
    ("f-11th", "11th place play-off", "6th North v 6th South", U(2026, 11, 27, 16, 40)),
    ("f-5th", "5th place play-off", "3rd North v 3rd South", U(2026, 11, 27, 20, 10)),
    ("f-9th", "9th place play-off", "5th North v 5th South", U(2026, 11, 28, 13, 10)),
    ("f-3rd", "3rd place play-off", "2nd North v 2nd South", U(2026, 11, 28, 16, 40)),
    ("f-7th", "7th place play-off", "4th North v 4th South", U(2026, 11, 29, 13, 10)),
    ("f-final", "CHAMPIONSHIP FINAL", "1st North v 1st South", U(2026, 11, 29, 16, 40)),
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


BALL = "\U0001F3C9"
lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0",
    "PRODID:-//Claude//Rugby Internationals 2026//EN",
    "CALSCALE:GREGORIAN",
    f"X-WR-CALNAME:{BALL} Rugby Internationals",
    fold("X-WR-CALDESC:" + esc(
        "All remaining 2026 men's Test matches for Argentina, Australia, "
        "England, Fiji, France, Ireland, Italy, Japan, New Zealand, Scotland, "
        "South Africa and Wales.")),
    "X-WR-TIMEZONE:UTC",
]
stamp = "20260728T090000Z"
n_timed = n_allday = 0


def emit(uid, summary, when, vkey, comp, note, extra=""):
    global n_timed, n_allday
    vname, street, lat, lon, vtz = V[vkey]
    timed = isinstance(when, datetime)
    if timed:
        local = when.astimezone(ZoneInfo(vtz))
        ko = (f"Kick-off: {local.strftime('%a %-d %b, %H:%M')} local  |  "
              f"{when.strftime('%H:%M')} UTC")
        dt = [f"DTSTART:{when.strftime('%Y%m%dT%H%M%SZ')}",
              f"DTEND:{(when + timedelta(hours=2)).strftime('%Y%m%dT%H%M%SZ')}"]
        n_timed += 1
    else:
        ko = "Kick-off: TO BE CONFIRMED (shown as an all-day entry)"
        dt = [f"DTSTART;VALUE=DATE:{when.strftime('%Y%m%d')}",
              f"DTEND;VALUE=DATE:{(when + timedelta(days=1)).strftime('%Y%m%d')}"]
        n_allday += 1
    desc = (f"{summary[2:]}\n\nCompetition: {comp}\n{ko}\n\nVenue: {vname}\n"
            f"Address: {street}\n\nNotes\n{note}{extra}")
    lines.extend([
        "BEGIN:VEVENT", f"UID:{uid}-2026@claude-rugby-cal",
        f"DTSTAMP:{stamp}", *dt,
        fold("SUMMARY:" + esc(summary)),
        fold("LOCATION:" + esc(f"{vname}, {street}")),
        f"GEO:{lat};{lon}",
        fold(f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-ADDRESS="{street}";'
             f'X-APPLE-RADIUS=150;X-TITLE="{vname}":geo:{lat},{lon}'),
        fold("DESCRIPTION:" + esc(desc)),
        fold("CATEGORIES:" + esc("Rugby Union") + "," + esc(comp)),
        "URL:https://nationschampionshiprugby.com/en",
        "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
    ])


for uid, home, away, when, vkey, comp, note in M:
    emit(uid, f"{BALL} {home} v {away}", when, vkey, comp, note)

for uid, label, matchup, day in FINALS:
    emit(uid, f"{BALL} Nations C'ship {label}", day, "twick",
         "Nations Championship Finals",
         f"Finals Weekend at Twickenham - three days of double-headers. "
         f"Fixture: {matchup}. Kick-off is fixed and ticketed, but WHICH TEAMS "
         f"play is decided by the final pool tables after Round 6 on 21 Nov.")

lines.append("END:VCALENDAR")
with open("../docs/rugby-internationals.ics", "w",
          encoding="utf-8", newline="") as f:
    f.write("\r\n".join(lines) + "\r\n")
print(f"Wrote {n_timed + n_allday} matches ({n_timed} timed, {n_allday} TBC).")
