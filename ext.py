import pyperclip
import pyautogui
import time
from pynput import keyboard

# ============================================
# PART 1: CHARACTER MAPPING
# ============================================

# English to Arabic keyboard mapping
# Based on standard QWERTY to Arabic keyboard layout
en_to_ar = {
    # Top row (numbers and symbols)
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

    # First letter row
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

    # Second letter row
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

    # Third letter row
    'z': 'ئ',
    'x': 'ء',
    'c': 'ؤ',
    'v': 'ر',
    'b': 'لا',  # Special: LA ligature
    'n': 'ى',
    'm': 'ة',
    ',': 'و',
    '.': 'ز',
    '/': 'ظ',

    # Space and common characters
    ' ': ' ',
}


# ============================================
# PART 2: TEXT CONVERSION FUNCTION
# ============================================

def mapper(input_text: str) -> str:
    """Converts English keyboard input to Arabic characters."""
    output = ''
    for char in input_text:
        output += en_to_ar.get(char, char)
    return output


# ============================================
# PART 3: MAIN CONVERSION LOGIC
# ============================================

def convert_selected_text():
    """
    Main function that handles the conversion process.
    """
    try:
        print("Converting...")

        # Step 1: Copy the highlighted text
        pyautogui.hotkey('ctrl', 'c')

        # Step 2: Wait for clipboard to update
        time.sleep(0.1)

        # Step 3: Get the copied text
        original_text = pyperclip.paste()

        # Check if we actually got text
        if not original_text:
            print("No text selected!")
            return

        # Step 4: Convert it
        converted_text = mapper(original_text)

        # Step 5: Put converted text in clipboard
        pyperclip.copy(converted_text)

        # Step 6: Small delay before pasting
        time.sleep(0.05)

        # Step 7: Paste the converted text
        pyautogui.hotkey('ctrl', 'v')

        print(f"✓ Converted: '{original_text}' → '{converted_text}'")

    except Exception as e:
        print(f"✗ Error during conversion: {e}")


# ============================================
# PART 4: HOTKEY DETECTION (FIXED VERSION)
# ============================================

# Track modifier keys separately
ctrl_pressed = False
shift_pressed = False
caps_pressed  = False

def on_press(key):
    """
    Called whenever ANY key is pressed.

    NEW APPROACH:
    - Track Ctrl and Shift separately with boolean flags
    - When we detect 'A' being pressed, check if both modifiers are active
    - This is more reliable than using sets
    """
    global ctrl_pressed, shift_pressed, caps_pressed

    # Check for Ctrl key (both left and right)
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.ctrl):
        ctrl_pressed = True
        print("Ctrl pressed")

    # Check for Shift key (both left and right)
    elif key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
        shift_pressed = True
        print("Shift pressed")

    elif key == keyboard.Key.caps_lock:
        caps_pressed = True
        print("caps pressed")




def on_release(key):
    """
    Called whenever ANY key is released.
    Reset our modifier flags when keys are released.
    """
    global ctrl_pressed, shift_pressed,caps_pressed
    if ctrl_pressed and shift_pressed and caps_pressed:
        print("🔥 HOTKEY DETECTED! Starting conversion...")
        convert_selected_text()
    # Reset Ctrl flag
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.ctrl):
        ctrl_pressed = False
        print("Ctrl released")

    # Reset Shift flag
    elif key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
        shift_pressed = False
        print("Shift released")
    elif key == keyboard.Key.caps_lock:
        caps_pressed = False
        print("caps released")

    # Exit on ESC
    if key == keyboard.Key.esc:
        print("\n👋 Exiting program...")
        return False  # Stop listener


# ============================================
# PART 5: MAIN PROGRAM
# ============================================

def main():
    """Main function that starts the program."""
    print("=" * 60)
    print("🔤 English to Arabic Keyboard Converter")
    print("=" * 60)
    print("\n📋 Instructions:")
    print("  1. Highlight any English text")
    print("  2. Press Ctrl + Shift + A")
    print("  3. Text will be converted to Arabic")
    print("\n⚠️  Press ESC to exit the program")
    print("=" * 60)
    print("\n👂 Listening for hotkey (Ctrl + Shift + A)...\n")

    # Test the mapper function
    print("🧪 Testing mapper:")
    test_text = "hgsghlugd;l"
    print(f"   Input:  '{test_text}'")
    print(f"   Output: '{mapper(test_text)}'")
    print()

    # Create and start the listener
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release
    ) as listener:
        listener.join()

    print("\n✓ Program ended.")


# ============================================
# PART 6: RUN THE PROGRAM
# ============================================

if __name__ == "__main__":
    main()