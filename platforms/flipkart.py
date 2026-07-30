import random
import time
from typing import List

import config
from models import LineItem
from platforms.base import Platform


def _think_pause():
    time.sleep(random.uniform(*config.ACTION_DELAY_RANGE_SECONDS))


def _looks_like_verification_challenge(page) -> bool:
    return page.locator("text=Verify OTP").count() > 0


class FlipkartPlatform(Platform):
    name = "Flipkart"
    flow_type = "sequential"

    def storage_state_path(self) -> str:
        return str(config.STORAGE_STATE_DIR / "flipkart.json")

    def process_order(self, page, order_id: str, items: List[LineItem]) -> None:
        for item in items:
            try:
                self._return_single_item(page, order_id, item)
            except Exception as exc:
                item.task_status = config.STATUS_NEEDS_REVIEW
                item.error_note = f"Unhandled error: {exc}"

    def _return_single_item(self, page, order_id: str, item: LineItem) -> None:
        # TODO: replace with real selectors from Flipkart's order detail page.
        page.goto(f"https://www.flipkart.com/orders/{order_id}")
        _think_pause()

        if _looks_like_verification_challenge(page):
            item.task_status = config.STATUS_NEEDS_REVIEW
            item.error_note = "OTP/verification prompt shown — needs manual login refresh"
            return

        sku_row = page.locator(f"[data-sku='{item.sku}']")
        if sku_row.count() == 0:
            item.task_status = config.STATUS_NEEDS_REVIEW
            item.error_note = "SKU not found on order page"
            return

        if False:  # TODO: real eligibility check
            item.return_status = config.RETURN_STATUS_OUT_OF_WINDOW
            item.task_status = config.STATUS_DONE
            return

        _think_pause()

        item.return_id = "PLACEHOLDER-RETURN-ID"
        item.refund_amount = "PLACEHOLDER-AMOUNT"
        item.return_status = config.RETURN_STATUS_PLACED
        item.task_status = config.STATUS_DONE
