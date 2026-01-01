import pyperclip
import pyautogui
import time
from pynput import keyboard

en_to_ar = {
    '`': 'ذ',
    '1': '١',
    '2': '٢',
    '3': '٣',
    '4': '٤',
    '5': '٥',
    '6': '٦',
    '7': '٧',
    '8': '٨',
    '9': '٩',
    '0': '٠',
    '-': '-',
    '=': '=',
    'q': 'ض',
    'w': 'ص',
    'e': 'ث',
    'r': 'ق',
    't': 'ف',
    'y': 'غ',
    'u': 'ع',
    'i': 'ه',
    'o': 'خ',
    'p': 'ح',
    '[': 'ج',
    ']': 'د',
    'a': 'ش',
    's': 'س',
    'd': 'ي',
    'f': 'ب',
    'g': 'ل',
    'h': 'ا',
    'j': 'ت',
    'k': 'ن',
    'l': 'م',
    ';': 'ك',
    "'": 'ط',
    'z': 'ئ',
    'x': 'ء',
    'c': 'ؤ',
    'v': 'ر',
    'b': 'لا',
    'n': 'ى',
    'm': 'ة',
    ',': 'و',
    '.': 'ز',
    '/': 'ظ',
    ' ': ' ',
}
ar_to_en = {v: k for k, v in en_to_ar.items()}

def mapper(input_text: str) -> str:
    """Converts English keyboard input to Arabic characters."""
    output = ''
    if input_text[0] in en_to_ar.keys():
        for char in input_text.lower():
            output += en_to_ar.get(char, char)
        return output
    else:
        for char in input_text.lower():
            output += ar_to_en.get(char, char)
        return output


kbd_controller = keyboard.Controller()
def convert_selected_text():
    """
    Main function that handles the conversion process.
    """

    kbd_controller.release(keyboard.Key.shift)
    kbd_controller.release(keyboard.Key.shift_l)
    kbd_controller.release(keyboard.Key.shift_r)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl','c')

    original_text = pyperclip.paste()
    converted_text = mapper(original_text)
    pyperclip.copy(converted_text)
    pyautogui.hotkey('ctrl', 'v')

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