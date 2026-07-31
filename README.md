# Calendar hosting and auto-update

## The core idea

An imported `.ics` is a dead copy. A **subscribed** `.ics` is a live link that
re-reads the file on a schedule. So:

1. Put the files somewhere with a stable public URL
2. Subscribe instead of importing
3. Update the file in one place; every device follows

## Repo layout

```
calendars/
├─ .github/workflows/refresh-calendars.yml
├─ build/                 <- generator scripts + downloaded source data
│   ├─ make_nfl_full.py
│   ├─ make_f1_sessions.py
│   └─ ... (the rest)
└─ docs/                  <- the published .ics files (GitHub Pages root)
    ├─ nfl.ics
    ├─ f1.ics
    └─ ...
```

Use `docs/` and turn on GitHub Pages (Settings → Pages → Deploy from branch →
`main` / `docs`). **This matters:** `raw.githubusercontent.com` serves `.ics`
as `text/plain`, which some clients refuse. Pages serves it as `text/calendar`.

Your URLs become:

```
https://<username>.github.io/calendars/nfl.ics
```

## Subscribing

- **Apple** — Calendar → File → New Calendar Subscription. Paste the URL, set
  auto-refresh to *Every day*. On iPhone: Settings → Apps → Calendar →
  Accounts → Add Account → Other → Add Subscribed Calendar.
- **Google** — Other calendars → **From URL**. Refresh is 12–24h and cannot be
  controlled.
- Swap `https://` for `webcal://` and phones open the subscribe dialog
  instead of downloading a copy.

## What actually auto-updates

**Genuinely live — the workflow does real work:**

| Calendar | Source | What changes |
|---|---|---|
| NFL | `nflverse/nfldata` | Flex scheduling moves Sunday kick-offs on ~12 days' notice from Week 5. This is the single most valuable auto-update you have. |
| F1 | `sportstimes/f1` | Session time adjustments, occasional calendar changes. |

**Static — hosting still helps, but the workflow skips them:**

Golf, tennis, rugby, darts, chess, UFC, NASCAR, economic data, 13F,
trading holidays, derivatives. These were researched and hardcoded. Re-running
their scripts rewrites identical bytes. Hosting them is still worth it, because
you push a correction once rather than re-importing on every device.

## Manual refresh points

- **Quarterly** — earnings, UFC cards (confirmed 8–12 weeks out), darts session
  times, chess Rapid & Blitz once FIDE announces
- **October** — the new OMB federal indicator schedule lands; rebuild the
  economic calendars for the next year
- **Ad hoc** — anything the news moves. LIV Golf is the live example: a season
  finale went from scheduled to expected-cancelled in a week, and no cron job
  would have caught that.

## Safety

The workflow validates every file before committing: it must parse, contain at
least one event, and respect the 75-octet line-folding limit. A malformed
`.ics` pushed to a subscribed calendar can empty it on the client, so the
validation gate is not optional.

Run it by hand any time from the Actions tab via **workflow_dispatch**.
