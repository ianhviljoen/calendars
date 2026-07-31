#!/usr/bin/env bash
# update.sh - rebuild every calendar, validate, publish.
#
#   ./update.sh            rebuild + validate + commit + push
#   ./update.sh --dry      rebuild + validate only, no git
#   ./update.sh --live     only the two calendars with live upstream feeds
#
set -euo pipefail
cd "$(dirname "$0")"

DRY=0; LIVE_ONLY=0
for a in "$@"; do
  [[ "$a" == "--dry"  ]] && DRY=1
  [[ "$a" == "--live" ]] && LIVE_ONLY=1
done

echo "==> Checking dependency"
if python3 -c "import icalendar" 2>/dev/null; then
  echo "    icalendar already present"
else
  echo "    installing icalendar"
  PIP="python3 -m pip install --quiet --disable-pip-version-check"
  $PIP icalendar 2>/dev/null \
    || $PIP --user icalendar 2>/dev/null \
    || $PIP --break-system-packages icalendar 2>/dev/null \
    || { echo "    could not install - try: pip3 install icalendar"; exit 1; }
fi

echo "==> Downloading live source data"
curl -sSfL --retry 3 \
  https://raw.githubusercontent.com/nflverse/nfldata/master/data/games.csv \
  -o build/nfl.csv
curl -sSfL --retry 3 \
  https://raw.githubusercontent.com/sportstimes/f1/main/_db/f1/2026.json \
  -o build/f1.json
curl -sSfL --retry 3 \
  https://raw.githubusercontent.com/openfootball/england/master/2026-27/1-premierleague.txt \
  -o build/epl.txt
curl -sSfL --retry 3 \
  "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=100&ordering=net&lsp__name=SpaceX" \
  -o build/launches.json

echo "==> Rebuilding"
cd build
if [[ $LIVE_ONLY -eq 1 ]]; then
  SCRIPTS="make_nfl_full.py make_f1_sessions.py make_epl_ics.py make_launches_ics.py"
else
  SCRIPTS=$(ls make_*.py)
fi
for s in $SCRIPTS; do
  printf '    %-26s ' "$s"
  python3 "$s" >/dev/null 2>&1 && echo "ok" || { echo "FAILED"; exit 1; }
done
rm -f nfl.csv f1.json epl.txt launches.json
cd ..

echo "==> Validating"
python3 - <<'PY'
import glob, sys
from icalendar import Calendar
fail = False
files = sorted(glob.glob("docs/*.ics"))
if not files:
    print("    no .ics files found"); sys.exit(1)
for p in files:
    raw = open(p, "rb").read()
    try:
        n = len(list(Calendar.from_ical(raw).walk("VEVENT")))
    except Exception as e:
        print(f"    FAIL parse {p}: {e}"); fail = True; continue
    longs = [l for l in raw.decode().split("\r\n") if len(l.encode()) > 75]
    uids = [str(e["UID"]) for e in Calendar.from_ical(raw).walk("VEVENT")]
    if n == 0:
        print(f"    FAIL empty {p}"); fail = True
    elif longs:
        print(f"    FAIL fold  {p}: {len(longs)} long lines"); fail = True
    elif len(set(uids)) != len(uids):
        print(f"    FAIL dupes {p}: repeated UIDs"); fail = True
    else:
        print(f"    ok {p:<34} {n:>4} events")
sys.exit(1 if fail else 0)
PY

if [[ $DRY -eq 1 ]]; then
  echo "==> Dry run - nothing committed"
  exit 0
fi

echo "==> Publishing"
git add -A docs
if git diff --staged --quiet; then
  echo "    no changes"
else
  git commit -q -m "Refresh calendars $(date -u +%Y-%m-%d)"
  git push -q
  echo "    pushed"
fi
echo "==> Done"
