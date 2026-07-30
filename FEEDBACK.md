# Spec Review — Returns Automation Agent

Issues found before starting the build. These need answers or the build will make
assumptions that could be wrong.

## 1. Amazon is listed under both flow types
Section 3 lists Amazon as an example of "Batch flow" AND "Sequential flow" in the
same document. These are contradictory. Which is correct? (Real answer: Amazon's
return flow is per-item / sequential — you select items to return one at a time,
even within one order. If someone wrote "batch" for Amazon, that's a spec error.)

## 2. Bot-detection avoidance is listed as a "bonus" — it's actually the hardest part
Everything else in the spec (Excel loop, write-back, partial success) is standard
RPA. Reliably driving Amazon/Flipkart without tripping bot detection is the real
engineering risk, and it's the one part with zero detail. Before building:
- What detection signals are we expected to defeat? (headless fingerprinting,
  CAPTCHA, session/IP consistency, request pacing)
- Is there a fallback when a CAPTCHA or verification challenge blocks the flow —
  or does the whole task go to "needs human review"?
- Has this been checked against Amazon/Flipkart's terms of service for automated
  account access? This isn't a build question, it's a legal/business one, and it
  should be answered before this ships, not after.

## 3. No idempotency / crash-recovery behavior specified
If the agent dies mid-run after submitting a return but before writing back to
Excel, what happens on restart? Without a way to check "did this return already
go through," a naive retry could submit a duplicate return request. Needs a
defined answer — the build below assumes duplicate-submission checking via
before/after order-status lookup.

## 4. No volume or timing expectations
No stated order volume, run frequency, or SLA. This affects whether the agent runs
as a scheduled batch job or a longer-running daemon, and how much parallelism is
safe. The build below defaults to sequential processing (safer, slower) — flag if
volume requires parallel sessions.

## 5. Credentials shared in plaintext in the spec doc
The Flipkart phone number / OTP login flow is written directly into this document.
That's a document that gets emailed, uploaded, and copy-pasted. Credentials
shouldn't live in a spec — they belong in a secrets manager or `.env` file that's
gitignored, referenced by name only. Flagging this so it doesn't get treated as
normal practice on the next spec.
