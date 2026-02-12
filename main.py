import mss
import numpy as np
import cv2
import pyautogui
import keyboard
import time
import re


# ---------------- CONFIG ---------------- #

def load_config(path="config.txt"):

    config = {}

    try:
        with open(path, "r") as f:

            for line in f:

                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)

                    key = key.strip()
                    value = value.strip()

                    config[key] = value

    except FileNotFoundError:
        print("config.txt not found.")
        exit()

    return config


def hex_to_hsv(hex_color):

    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    rgb = np.uint8([[[r, g, b]]])

    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[0][0]

    return hsv


# ---------------- SCREEN ---------------- #

def capture_screen():

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        img = sct.grab(monitor)

        frame = np.array(img)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        return frame


# ---------------- COLOR ---------------- #

def find_color_pixels(frame, lower, upper):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)

    coords = np.column_stack(np.where(mask > 0))

    return coords


# ---------------- MOUSE ---------------- #

def trace_pixels(coords, speed=0.001):

    if len(coords) == 0:
        print("No color found")
        return

    for y, x in coords:
        pyautogui.moveTo(x, y, duration=speed)


# ---------------- MAIN ---------------- #

def main():

    config = load_config()

    # Read config
    hex_color = config.get("@color-selected", "#ff0000")
    keybind = config.get("@keybind", "f")

    print("Loaded config:")
    print(" Color:", hex_color)
    print(" Keybind:", keybind)

    # Convert hex → HSV
    hsv = hex_to_hsv(hex_color)

    # Tolerance (adjust if needed)
    h, s, v = hsv

    tolerance = 10

    lower = np.array([
        max(0, h - tolerance),
        max(50, s - 50),
        max(50, v - 50)
    ])

    upper = np.array([
        min(179, h + tolerance),
        min(255, s + 50),
        min(255, v + 50)
    ])


    print("HSV Target:", hsv)
    print("HSV Range:", lower, upper)
    print(f"Press {keybind.upper()} to trace")
    print("Press ESC to quit")


    while True:

        if keyboard.is_pressed(keybind):

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
