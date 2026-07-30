# Returns Automation Agent

## Setup
```
pip install -r requirements.txt
playwright install chromium
```

## 1. Capture an authenticated session (once per platform)
```
python capture_login_session.py amazon
python capture_login_session.py flipkart
```
This opens a real browser, you log in manually (OTP included), and the
session is saved to `auth_state/<platform>.json`. Re-run whenever a session
expires or gets logged out. No credential is ever stored in code or in Excel.

## 2. Prepare `returns_tasks.xlsx`
Sheet name: `Tasks`. Header row, one line item per row:

`Platform | OrderID | SKU | ReturnWindow | ReturnID | ReturnStatus | RefundAmount | TaskStatus | Timestamp | ErrorNote`

Leave `ReturnID`, `ReturnStatus`, `RefundAmount`, `Timestamp`, `ErrorNote` blank.
Set `TaskStatus` to `To Do` for rows the agent should process.

## 3. Run
```
python main.py
```
Processes every pending line item, writes results back to the same Excel file
row by row, groups line items by order so partial-order failures don't block
unrelated items.

## Before this touches real orders
- Fill in the real selectors in `platforms/amazon.py` / `platforms/flipkart.py`
  — the current ones are placeholders (marked `TODO`), built without access to
  a live logged-in session on either site.
- Confirm Amazon's actual flow type (see `FEEDBACK.md` item 1) — currently set
  to `sequential`, unverified against the real UI.
- Get sign-off that automated return submission is allowed under both
  platforms' terms of service for this account. This is a business/legal
  question, not something the code resolves.
- Test against a handful of real orders manually before pointing it at a full
  queue — especially the "out of window" and duplicate-submission detection
  logic, which is stubbed (`if False:`) pending real page content to check
  against.
