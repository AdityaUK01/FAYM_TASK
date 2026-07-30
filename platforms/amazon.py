import random
import time
from typing import List

import config
from models import LineItem
from platforms.base import Platform


def _think_pause():
    time.sleep(random.uniform(*config.ACTION_DELAY_RANGE_SECONDS))


def _looks_like_verification_challenge(page) -> bool:
    """Best-effort check for a CAPTCHA / OTP / 'verify it's you' interstitial.
    Selectors are placeholders — fill in against the real page.
    On a hit, the item is handed to a human, not auto-solved."""
    return page.locator("text=Enter the characters you see").count() > 0


class AmazonPlatform(Platform):
    name = "Amazon"
    flow_type = "sequential"  # confirmed with whoever wrote the spec — see FEEDBACK.md item 1

    def storage_state_path(self) -> str:
        return str(config.STORAGE_STATE_DIR / "amazon.json")

    def process_order(self, page, order_id: str, items: List[LineItem]) -> None:
        for item in items:
            try:
                self._return_single_item(page, order_id, item)
            except Exception as exc:
                item.task_status = config.STATUS_NEEDS_REVIEW
                item.error_note = f"Unhandled error: {exc}"
            # one item's outcome, good or bad, never blocks the next item

    def _return_single_item(self, page, order_id: str, item: LineItem) -> None:
        # TODO: replace with real selectors from Amazon's Your Orders page.
        page.goto(f"https://www.amazon.in/gp/css/order-history?orderID={order_id}")
        _think_pause()

        if _looks_like_verification_challenge(page):
            item.task_status = config.STATUS_NEEDS_REVIEW
            item.error_note = "Verification challenge shown — needs manual handling"
            return

        # TODO: locate the specific SKU row within the order, click "Return items"
        sku_row = page.locator(f"[data-sku='{item.sku}']")
        if sku_row.count() == 0:
            item.task_status = config.STATUS_NEEDS_REVIEW
            item.error_note = "SKU not found on order page"
            return

        # TODO: check return-eligibility text on the page before submitting
        if False:  # placeholder for real "out of window" detection
            item.return_status = config.RETURN_STATUS_OUT_OF_WINDOW
            item.task_status = config.STATUS_DONE
            return

        # TODO: click through reason selection, refund/pickup option, confirm
        _think_pause()

        # TODO: scrape confirmation screen for real return ID / refund amount
        item.return_id = "PLACEHOLDER-RETURN-ID"
        item.refund_amount = "PLACEHOLDER-AMOUNT"
        item.return_status = config.RETURN_STATUS_PLACED
        item.task_status = config.STATUS_DONE
