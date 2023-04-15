import pickle
import csv
from pynput import keyboard, mouse
import time
import threading

# Initialize the lists to store the events
events = []
timestamps = []

# Define a shared variable to control the listeners
stop_listening = False

# Define the on_press function for the keyboard listener


def on_press(key):
    global stop_listening

    events.append(('keyboard', key, True))
    timestamps.append(time.time())

    # Stop the listeners when F8 is pressed
    if key == keyboard.Key.f8:
        print('Stopping listeners...')
        stop_listening = True

# Define the on_release function for the keyboard listener


def on_release(key):
    events.append(('keyboard', key, False))
    timestamps.append(time.time())

# Define the on_click function for the mouse listener


def on_click(x, y, button, pressed):
    events.append(('mouse', button, pressed))
    timestamps.append(time.time())


# Start the keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
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
with open('events.pickle', 'wb') as f:
    pickle.dump((events, timestamps), f)
