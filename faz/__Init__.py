import pickle
import time
import pyautogui
from pynput import keyboard, mouse

# Load the events and timestamps from the pickle file
with open('events.pickle', 'rb') as f:
    events, timestamps = pickle.load(f)

# Import the Controller class from Pynput
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController

# Create instances of the Pynput Controllers
keyboard_controller = KeyboardController()
mouse_controller = MouseController()

# Iterate through the events and execute them
for i, (event, timestamp) in enumerate(zip(events, timestamps)):
    event_type, *args = event
    if event_type == 'keyboard':
        print(event_type)
        key, pressed = args
        if pressed:
            keyboard_controller.press(key)
        else:
            keyboard_controller.release(key)
    elif event_type == 'mouse':
        button, pressed = args
        if pressed:
            mouse_controller.press(button)
        else:
            mouse_controller.release(button)
    # Wait for the time difference between events
    if i < len(events) - 1:
        next_timestamp = timestamps[i+1]
        time.sleep(max(0, next_timestamp - timestamp))
