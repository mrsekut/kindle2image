import os
import pyautogui
from typing import Callable
import time
from PIL import Image, ImageChops
from typing import Optional

def wait(condition: Callable[[], bool], timeout: int) -> bool:
    start_time = time.time()

    while not condition():
        if time.time() - start_time > timeout:
            print("Time out.")
            return False
        time.sleep(1)

    return True


def capture(region: tuple[int, int, int, int]) -> Image.Image:
    return pyautogui.screenshot(region=region)


def save(image: Image.Image, dir: str, filename: str) -> None:
    if not os.path.exists(dir):
        os.makedirs(dir)

    image.save(os.path.join(dir, filename))



class ScreenshotComparator:
    def __init__(self, max_same_count: int, resize_to: tuple[int, int] = (64, 64)):
        self.max_same_count = max_same_count
        self.same_count = 0
        self.prev_screenshot: Optional[Image.Image] = None
        self.resize_to = resize_to

    def compare(self, cur_screenshot: Image.Image) -> bool:
        cur_resized = cur_screenshot.resize(self.resize_to).convert("L")

        if self.prev_screenshot:
            prev_resized = self.prev_screenshot.resize(self.resize_to).convert("L")
            # 画像の差分を計算し、差分がほとんどない場合は同じと判断
            diff = ImageChops.difference(cur_resized, prev_resized)
            if diff.getbbox() is None:
                self.same_count += 1
                if self.same_count >= self.max_same_count:
                    return True
            else:
                self.same_count = 0

        self.prev_screenshot = cur_screenshot
        return False