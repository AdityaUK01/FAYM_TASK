# Returns Automation Agent

## What this is
A script (RPA — not an AI agent, no LLM, no API key) that reads pending
return requests from an Excel file, is meant to place those returns on
Amazon/Flipkart, and writes the result back into the same Excel row.

## Why this exists
Doing e-commerce returns by hand — click into each order, pick a reason,
confirm, note the result — is repetitive and slow when there are many
orders. This script automates the repetitive part: reading the task list,
driving the browser, and logging what happened, so a human doesn't have
to do each step manually.


## What you need installed
```
pip install -r requirements.txt
playwright install chromium
```

## One-time setup: log in
```
python capture_login_session.py amazon
python capture_login_session.py flipkart
```
Opens a real browser, you log in manually (OTP included), it saves the
session to `auth_state/`. The script itself never touches a login form or
stores a password — re-run this only when a session expires.

## What to put in Excel before running
File: `returns_tasks.xlsx`, in the same folder as `main.py`.

Header row, any of these column names work (spacing/casing flexible):

| Column | What goes in it | Who fills it |
|---|---|---|
| Platform | `Amazon` or `Flipkart` | you |
| OrderID | the order number | you |
| SKU | product/SKU name | you |
| ReturnWindow | e.g. `15 days` | you |
| TaskStatus | `To Do` | you |
| ReturnID | leave blank | script |
| ReturnStatus | leave blank | script |
| RefundAmount | leave blank | script |
| Timestamp | leave blank | script |
| ErrorNote | leave blank (optional column) | script |

One row per line item — if an order has 3 products, that's 3 rows, same
OrderID, different SKU. Set `TaskStatus` to `To Do` on every row you want
processed. The script skips rows already marked `Done` or anything other
than `To Do` / `Pending`.

## How to run
1. Close `returns_tasks.xlsx` in Excel first — Windows locks the file
   while it's open, and the script can't save results into a locked file.
2. Run:
   ```
   python main.py
   ```
3. Reopen the Excel file to see results per row.

## What happens when it runs
- Reads every row marked `To Do`.
- Groups rows by order, so multi-item orders are handled together.
- For each row: opens the platform, attempts the return, writes back
  `ReturnID` / `ReturnStatus` / `RefundAmount` / `TaskStatus` / `Timestamp`.
- If one item in an order fails, the others still get processed — one bad
  item doesn't block the rest of the order.
- If a platform shows a CAPTCHA or verification challenge, that row is
  marked `Needs human review` instead of the script trying to solve it.

## Before pointing this at real orders
- Fill in the real selectors (see "Current state" above).
- Confirm Amazon's actual return flow (batch vs. per-item) — the spec
  document this was built from contradicted itself on this point.
- Get confirmation that automating returns this way doesn't violate
  Amazon/Flipkart's terms of service for the account being used — that's
  a business decision, not something this script resolves.

## Repo contents
This repo also contains the SQL assignment answers and charts for the
FAYM task, in addition to the returns automation agent above.

