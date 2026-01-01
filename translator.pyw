import pyperclip
import pyautogui
import time
import threading
import sys
from pynput import keyboard
from pystray import Icon, MenuItem as item, Menu
from PIL import Image
import os
# --- 1. MAPPING LOGIC (Your Original Logic) ---
en_to_ar = {
    '`': 'ذ', '1': '١', '2': '٢', '3': '٣', '4': '٤', '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩', '0': '٠',
    '-': '-', '=': '=', 'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف', 'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ',
    'p': 'ح', '[': 'ج', ']': 'د', 'a': 'ش', 's': 'س', 'd': 'ي', 'f': 'ب', 'g': 'ل', 'h': 'ا', 'j': 'ت', 'k': 'ن',
    'l': 'م', ';': 'ك', "'": 'ط', 'z': 'ئ', 'x': 'ء', 'c': 'ؤ', 'v': 'ر', 'b': 'لا', 'n': 'ى', 'm': 'ة', ',': 'و',
    '.': 'ز', '/': 'ظ', ' ': ' ',
}
ar_to_en = {v: k for k, v in en_to_ar.items()}
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    # We use os.path.join to avoid slash errors
    return os.path.join(base_path, relative_path)

def mapper(input_text: str) -> str:
    if not input_text: return ""
    output = ''
    if input_text[0] in ar_to_en:
        for char in input_text:
            output += ar_to_en.get(char, char)
    else:
        for char in input_text.lower():
            output += en_to_ar.get(char, char)
    return output


# --- 2. KEYBOARD HANDLING ---
kbd_controller = keyboard.Controller()


def convert_selected_text():
    try:
        # Release modifiers logic
        kbd_controller.release(keyboard.Key.shift)
        kbd_controller.release(keyboard.Key.shift_l)
        kbd_controller.release(keyboard.Key.shift_r)
        time.sleep(0.1)

        # Select All and Copy
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.05)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.05)

        original_text = pyperclip.paste()
        if not original_text: return

        converted_text = mapper(original_text)

        pyperclip.copy(converted_text)
        pyautogui.hotkey('ctrl', 'v')

    except Exception as e:
        print(f"Error: {e}")


def start_keyboard_listener():
    """Runs the pynput listener in a separate thread."""

    def on_activate():
        convert_selected_text()

    def for_canonical(f):
        return lambda k: f(listener.canonical(k))

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<shift>+<caps_lock>'),
        on_activate)

    with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)
    ) as listener:
        listener.join()


# --- 3. SYSTEM TRAY ICON SETUP ---

def create_image():
    """Generates a simple icon image dynamically so you don't need a .ico file."""
    image = resource_path("app_icon.ico")
    return Image.open(image)


def on_quit(icon, item):
    """Callback to exit the program."""
    icon.stop()
    sys.exit()


def main():
    # 1. Start the keyboard listener in a background thread
    # We use daemon=True so it dies automatically when the main program quits
    listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
    listener_thread.start()

    # 2. Create the system tray icon
    image = create_image()
    menu = Menu(item('Exit', on_quit))

    icon = Icon("LanguageFixer", image, "En/Ar Fixer", menu)

    # 3. Run the icon (this blocks the main thread until you click Exit)
    icon.run()


if __name__ == "__main__":
    main()