import subprocess
from pynput.keyboard import Controller, Key
import time

keyboard = Controller()

def execute_action(action):
    if action.startswith("type:"):
        text = action.replace("type:", "", 1)
        type_text(text)
        return f"Typed '{text}'"

    elif action.startswith("launch:"):
        program = action.replace("launch:", "", 1)
        subprocess.Popen(program, shell=True)
        return f"Launched '{program}'"

    else:
        raise ValueError("Unknown action format")

def type_text(text):
    time.sleep(0.3)  # slight delay
    for char in text:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.02)
