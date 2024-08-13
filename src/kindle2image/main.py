import pyautogui
import time
import argparse
from .kindle import get_kindle_window_position, is_kindle_active
from .utils import capture, save, ScreenshotComparator, wait

def main() -> None:
    parser = argparse.ArgumentParser(description="Capture Kindle pages as images.")
    parser.add_argument("--title", type=str, default="title", help="Title for the output directory.")
    parser.add_argument("--dirction", type=str, default="left", help="Direction key to move to the next page (e.g., 'left', 'right').")
    parser.add_argument("--max-same-count", type=int, default=2, help="Threshold for the number of consecutive identical screenshots before stopping.")
    args = parser.parse_args()

    print("Please activate your Kindle. Waiting for activation...")
    wait(is_kindle_active, 10)

    print("Kindle is now active. Starting screenshot process...")
    time.sleep(3)

    position = get_kindle_window_position()
    if not position:
        print("Could not find the Kindle window. Please make sure it is open and visible.")
        return

    page_number = 1
    comparator = ScreenshotComparator(args.max_same_count)

    while True:
        if not is_kindle_active():
            print("The process has ended because Kindle is no longer active.")
            break

        filename = f"{page_number}.png"
        screenshot = capture(position)
        save(screenshot, f"out/{args.title}", filename)
        print(f"Screenshot saved as {filename}.")

        if comparator.compare(screenshot):
            print("Detected the same page multiple times. The process has completed successfully.")
            break

        pyautogui.press(args.dirction)
        time.sleep(0.1)

        page_number += 1

if __name__ == "__main__":
    main()
