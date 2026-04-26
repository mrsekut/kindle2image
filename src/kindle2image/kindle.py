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

def get_kindle_window_position() -> Optional[tuple[int, int, int, int]]:
    window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)

    for window in window_list:
        if "Kindle" in window.get("kCGWindowOwnerName", ""):
            bounds = window.get("kCGWindowBounds")

            x = bounds.get("X")
            y = bounds.get("Y")
            width = bounds.get("Width")
            height = bounds.get("Height")

            # Adjust y coordinate and height to exclude the menu bar
            menu_bar_height = 40
            adjusted_y = y + menu_bar_height
            adjusted_height = height - menu_bar_height
            return (int(x), int(adjusted_y), int(width), int(adjusted_height))
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