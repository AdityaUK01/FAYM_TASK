"""
Run this once per platform to create the persistent auth session the agent
uses later. This is the ONLY place a human logs in / enters an OTP —
main.py never touches a login form or holds a credential.

Usage:
    python capture_login_session.py amazon
    python capture_login_session.py flipkart
"""
import sys
from playwright.sync_api import sync_playwright

import config

URLS = {
    "amazon": "https://www.amazon.in/ap/signin",
    "flipkart": "https://www.flipkart.com/account/login",
}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in URLS:
        print("Usage: python capture_login_session.py [amazon|flipkart]")
        sys.exit(1)

    platform_key = sys.argv[1]
    config.STORAGE_STATE_DIR.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(URLS[platform_key])

        input(f"Log in to {platform_key} manually in the opened browser "
              f"(including OTP), then press Enter here once you're on the "
              f"account home page... ")

        out_path = config.STORAGE_STATE_DIR / f"{platform_key}.json"
        context.storage_state(path=str(out_path))
        print(f"Saved session to {out_path}")
        browser.close()


if __name__ == "__main__":
    main()
