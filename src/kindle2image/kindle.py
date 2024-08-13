from typing import Optional
from AppKit import NSWorkspace
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID,
)

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
            menu_bar_height = 80
            adjusted_y = y + menu_bar_height
            adjusted_height = height - menu_bar_height
            return (int(x), int(adjusted_y), int(width), int(adjusted_height))
    return None


def is_kindle_active() -> bool:
    active_app = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    return active_app == "Kindle"