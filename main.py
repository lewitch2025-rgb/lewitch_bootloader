import mss
import numpy as np
import cv2
import pyautogui
import keyboard
import time


def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = sct.grab(monitor)

        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        return frame


def find_color_pixels(frame, lower, upper):
    """
    lower / upper = HSV color range
    """

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)

    coords = np.column_stack(np.where(mask > 0))

    return coords


def trace_pixels(coords, speed=0.001):
    """
    Moves mouse through detected pixels
    """

    if len(coords) == 0:
        print("No color found")
        return

    h, w = pyautogui.size()

    for y, x in coords:
        pyautogui.moveTo(x, y, duration=speed)


def main():

    print("Press F to trace color")
    print("Press ESC to quit")

    # Example: RED color range in HSV
    lower = np.array([0, 120, 70])
    upper = np.array([10, 255, 255])

    while True:

        if keyboard.is_pressed("f"):

            print("Capturing...")

            frame = capture_screen()

            coords = find_color_pixels(frame, lower, upper)

            print(f"Found {len(coords)} pixels")

            trace_pixels(coords)

            time.sleep(0.5)

        if keyboard.is_pressed("esc"):
            break


if __name__ == "__main__":
    main()
