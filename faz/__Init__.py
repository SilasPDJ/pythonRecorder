from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import pickle
import time
import pyautogui
from pynput import keyboard, mouse
import pandas as pd


class RecorderUtils:
    def __init__(self, filename='events.pickle'):
        self.filename = filename

    def record_pickle(self):
        # Initialize the lists to store the events
        events = []
        timestamps = []

        # Define a shared variable to control the listeners
        stop_listening = False

        # Define the on_press function for the keyboard listener

        def on_press(key):
            nonlocal stop_listening
            events.append(('keyboard', key, True))
            timestamps.append(time.time())

            # Stop the listeners when F8 is pressed
            if key == keyboard.Key.f8:
                print('Stopping listeners...')
                stop_listening = True
                return False

        # Define the on_release function for the keyboard listener

        def on_release(key):
            events.append(('keyboard', key, False))
            timestamps.append(time.time())

        # Define the on_click function for the mouse listener

        def on_click(x, y, button, pressed):
            events.append(('mouse', button, pressed))
            timestamps.append(time.time())

        # Start the keyboard listener
        keyboard_listener = keyboard.Listener(
            on_press=on_press, on_release=on_release)
        keyboard_listener.start()

        # Start the mouse listener
        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.start()

        # Wait for the listeners to finish or stop if F8 is pressed
        while not stop_listening:
            time.sleep(0.1)

        # Stop the listeners
        keyboard_listener.stop()
        mouse_listener.stop()

        # Save the events to a CSV file

        # Save the events and timestamps to a pickle file
        with open(self.filename, 'wb') as f:
            pickle.dump((events, timestamps), f)

    def execute_pickle(self):
        # Load the events and timestamps from the pickle file
        with open(self.filename, 'rb') as f:
            events, timestamps = pickle.load(f)
        # df = pd.DataFrame(events)

        # Import the Controller class from Pynput

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


if __name__ == "__main__":
    pass
    new = RecorderUtils()
    new.record_pickle()
    new.execute_pickle()
