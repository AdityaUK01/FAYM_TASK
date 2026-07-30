from pathlib import Path

EXCEL_PATH = Path("returns_tasks.xlsx")
SHEET_NAME = "Tasks"

STORAGE_STATE_DIR = Path("auth_state")  # one storage_state.json per platform

MAX_RETRIES_PER_ITEM = 2
ACTION_DELAY_RANGE_SECONDS = (1.0, 3.0)  # think-time between UI actions

STATUS_TODO = "To Do"
STATUS_PENDING = "Pending"
STATUS_DONE = "Done"
STATUS_NEEDS_REVIEW = "Needs human review"

RETURN_STATUS_PLACED = "Placed"
RETURN_STATUS_FAILED = "Failed"
RETURN_STATUS_OUT_OF_WINDOW = "Out of window"
