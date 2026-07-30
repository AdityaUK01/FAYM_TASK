# Architecture — Returns Automation Agent

## Stack
- **Playwright** (Python) for browser control — better at persistent auth state and
  network-level control than Selenium.
- **openpyxl** for Excel read/write, in place, row-by-row.
- Standard library `logging` for the timestamp/error log column.

## Data model (per line item — matches spec's line-item write-back requirement)

| Column | Source |
|---|---|
| Platform | input |
| OrderID | input |
| SKU | input |
| ReturnWindow | input |
| ReturnID | agent |
| ReturnStatus | agent: `Placed` / `Failed` / `OutOfWindow` |
| RefundAmount | agent |
| TaskStatus | agent: `Done` / `NeedsReview` |
| Timestamp | agent |
| ErrorNote | agent |

## Processing loop
1. Read all rows where `TaskStatus` is `To Do` / `Pending`.
2. Group rows by `(Platform, OrderID)` — this is what lets the agent tell whether
   an order has one line item or several, and route to batch vs. sequential flow.
3. For each group: open (or reuse) a browser context for that platform, using a
   **persistent authenticated session** (`storage_state.json`), not credentials
   typed at runtime. Login/OTP happens once, manually, outside the agent loop —
   the agent never touches the login form.
4. Ask the platform adapter which flow model applies (`batch` or `sequential`) —
   this is a property of the platform, not something re-detected per order.
5. Process each line item **independently**, even inside a batch call:
   - Before submitting, check current order/item status on the platform page. If
     a return already exists for this SKU (crash-recovery case), record it and
     skip re-submitting.
   - If out of window or otherwise ineligible: log `OutOfWindow`, move on.
   - If the platform throws a CAPTCHA/verification challenge: stop that item,
     mark `NeedsReview`, log the reason. The agent does not attempt to solve or
     bypass verification challenges — that's a human handoff, not a retry case.
6. Write back to Excel immediately after each line item resolves (not batched at
   the end) — if the process dies mid-run, completed items are already saved.
7. Order-level `Done` is derived, never set directly: true only when every line
   item under that `(Platform, OrderID)` has a terminal `TaskStatus`.

## Reliability choices (not detection evasion)
These are standard practices for *any* production browser automation, not
techniques aimed at defeating a platform's anti-bot system:
- Headed (not headless) browser context — headless is a common false-positive
  trigger and isn't needed here since this runs unattended on a schedule, not at
  interactive scale.
- Randomized think-time between actions (1–3s) — avoids literally-instant
  form submission, which is more about not breaking the platform's own rate
  limits than "hiding."
- One browser session per platform, reused across the run, rather than a fresh
  session per line item — fewer logins, more like normal usage.
- Hard stop and human handoff on CAPTCHA/verification — the agent is not built
  to auto-solve these.

What this explicitly does **not** do: fingerprint spoofing, proxy rotation to
mask origin, or CAPTCHA-solving integrations. If the review target platforms
start blocking this session, that's a signal to slow down or get explicit
sign-off from the platform relationship owner — not to add evasion.

## Files
- `main.py` — orchestrator / loop
- `models.py` — `LineItem` dataclass + status enums
- `excel_io.py` — read pending rows, write results back in place
- `platforms/base.py` — abstract platform interface
- `platforms/amazon.py`, `platforms/flipkart.py` — platform adapters (selectors
  are placeholders — need to be filled in against the real site DOM, which
  requires a live logged-in session to inspect)
- `config.py` — retry counts, delay ranges, paths
