import time
import argparse
from .kindle import (
    get_kindle_window_position,
    is_kindle_active,
    find_kindle_pid,
    send_down_to_pid,
)
from .utils import capture, save, ScreenshotComparator, wait

def main() -> None:
    parser = argparse.ArgumentParser(description="Capture Kindle pages as images.")
    parser.add_argument("--title", type=str, required=True, help="Title for the output directory.")
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

    pid = find_kindle_pid()
    if pid is None:
        print("Could not find the Kindle process.")
        return
    print(f"Kindle PID: {pid}. You can switch focus to other apps now.")

    page_number = 1
    comparator = ScreenshotComparator(args.max_same_count)

    while True:
        if find_kindle_pid() is None:
            print("The process has ended because Kindle is no longer running.")
            break

        filename = f"{page_number}.png"
        screenshot = capture(position)
        save(screenshot, f"out/{args.title}", filename)
        print(f"Screenshot saved as {filename}.")

        if comparator.compare(screenshot):
            print("Detected the same page multiple times. The process has completed successfully.")
            break

        send_down_to_pid(pid)
        time.sleep(0.1)

        page_number += 1

if __name__ == "__main__":
    main()
