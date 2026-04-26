from typing import Optional
from AppKit import NSWorkspace
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID,
    CGEventCreateKeyboardEvent,
    CGEventPostToPid,
)

DOWN_KEY_CODE = 125

def find_kindle_window_id() -> Optional[int]:
    window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
    for window in window_list:
        if "Kindle" in window.get("kCGWindowOwnerName", ""):
            return int(window.get("kCGWindowNumber"))
    return None


def is_kindle_active() -> bool:
    active_app = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    return active_app == "Kindle"


def find_kindle_pid() -> Optional[int]:
    for app in NSWorkspace.sharedWorkspace().runningApplications():
        name = app.localizedName()
        if name and "Kindle" in name:
            return int(app.processIdentifier())
    return None


def send_down_to_pid(pid: int) -> None:
    ev_down = CGEventCreateKeyboardEvent(None, DOWN_KEY_CODE, True)
    ev_up = CGEventCreateKeyboardEvent(None, DOWN_KEY_CODE, False)
    CGEventPostToPid(pid, ev_down)
    CGEventPostToPid(pid, ev_up)