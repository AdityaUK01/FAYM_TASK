import logging
from collections import defaultdict
from typing import Dict, List, Tuple

from playwright.sync_api import sync_playwright

import config
import excel_io
from models import LineItem
from platforms.amazon import AmazonPlatform
from platforms.flipkart import FlipkartPlatform

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("returns_agent")

PLATFORMS = {
    "Amazon": AmazonPlatform(),
    "Flipkart": FlipkartPlatform(),
}


def group_by_platform_and_order(tasks: List[LineItem]) -> Dict[Tuple[str, str], List[LineItem]]:
    groups: Dict[Tuple[str, str], List[LineItem]] = defaultdict(list)
    for t in tasks:
        groups[(t.platform, t.order_id)].append(t)
    return groups


def run():
    tasks = excel_io.read_pending_tasks()
    log.info("Loaded %d pending line items", len(tasks))

    unknown_platform_tasks = [t for t in tasks if t.platform not in PLATFORMS]
    for t in unknown_platform_tasks:
        t.task_status = config.STATUS_NEEDS_REVIEW
        t.error_note = f"Unrecognized platform: {t.platform}"
        excel_io.write_result(t)

    groups = group_by_platform_and_order(
        [t for t in tasks if t.platform in PLATFORMS]
    )

    with sync_playwright() as p:
        # one browser context per platform, reused across all its orders in this run
        contexts = {}
        try:
            for platform_name in set(k[0] for k in groups):
                platform = PLATFORMS[platform_name]
                browser = p.chromium.launch(headless=False)
                context = browser.new_context(storage_state=platform.storage_state_path())
                contexts[platform_name] = context

            for (platform_name, order_id), items in groups.items():
                platform = PLATFORMS[platform_name]
                context = contexts[platform_name]
                page = context.new_page()

                log.info("Processing order %s on %s (%d line items)",
                         order_id, platform_name, len(items))
                try:
                    platform.process_order(page, order_id, items)
                except Exception as exc:
                    # order-level failure: still resolve every item individually,
                    # never leave a whole order silently unrecorded
                    log.exception("Order %s on %s failed at order level", order_id, platform_name)
                    for item in items:
                        if not item.is_terminal():
                            item.task_status = config.STATUS_NEEDS_REVIEW
                            item.error_note = f"Order-level failure: {exc}"
                finally:
                    for item in items:
                        if not item.is_terminal():
                            item.task_status = config.STATUS_NEEDS_REVIEW
                            item.error_note = item.error_note or "Left unresolved after processing"
                        excel_io.write_result(item)
                    page.close()
        finally:
            for context in contexts.values():
                context.close()

    log.info("Run complete")


if __name__ == "__main__":
    run()
