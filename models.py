from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LineItem:
    row_index: int          # excel row number, for write-back
    platform: str
    order_id: str
    sku: str
    return_window: str

    return_id: Optional[str] = None
    return_status: Optional[str] = None   # Placed / Failed / Out of window
    refund_amount: Optional[str] = None
    task_status: Optional[str] = None     # Done / Needs human review
    error_note: str = ""

    def is_terminal(self) -> bool:
        return self.task_status in ("Done", "Needs human review")
