import pyautogui
import time
from .kindle import get_kindle_window_position, is_kindle_active
from .utils import capture, save, ScreenshotComparator, wait

# TODO: options
title = "boss"
move = "left"  # TODO: name
max_same_count = 2  # 終了条件として設定する閾値



def main() -> None:
    print("Please activate your Kindle. Waiting for activation...")
    wait(is_kindle_active, 10)

    print("Kindle is now active. Starting screenshot process...")
    time.sleep(3)

    position = get_kindle_window_position()
    if not position:
        print("Could not find the Kindle window. Please make sure it is open and visible.")
        return

    page_number = 1
    comparator = ScreenshotComparator(max_same_count)

    while True:
        if not is_kindle_active():
            print("The process has ended because Kindle is no longer active.")
            break

        filename = f"{page_number}.png"
        screenshot = capture(position)
        save(screenshot, f"out/{title}", filename)
        print(f"Screenshot saved as {filename}.")

        if comparator.compare(screenshot):
            print("Detected the same page multiple times. The process has completed successfully.")
            break

        pyautogui.press(move)
        time.sleep(0.1)

        page_number += 1

