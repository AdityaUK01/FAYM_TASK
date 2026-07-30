from abc import ABC, abstractmethod
from typing import List
from models import LineItem


class Platform(ABC):
    name: str
    flow_type: str  # "batch" or "sequential" — fixed per platform, not re-detected per order

    @abstractmethod
    def storage_state_path(self) -> str:
        """Path to the saved Playwright auth session for this platform.
        Login/OTP happens once, manually, outside the agent — the agent
        only ever loads an already-authenticated session."""

    @abstractmethod
    def process_order(self, page, order_id: str, items: List[LineItem]) -> None:
        """Process every line item for one order on this platform.
        Must mutate each LineItem in place (return_id, return_status,
        refund_amount, task_status, error_note) and must not let one
        item's failure stop the others in the same order."""
