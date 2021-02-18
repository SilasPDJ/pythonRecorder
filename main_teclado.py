from pynput.keyboard import Key, Controller, Listener
import pynput
import time
from time import sleep


def on_press(key):
    print('{0} pressed'.format(
        key))


def on_release(key):

    eventos.append(key)
    if key == Key.esc:

        return False

    print('{0} release'.format(
        key))


controller = pynput.keyboard.Controller()

eventos = []

# Collect events until released
with Listener(on_press, on_release) as listener:
    listener.join()
try:
    listener.wait()
finally:
    listener.stop()


print('*REPLAYING*')
for key in eventos:
    print(key)
    controller.press(key)
    controller.release(key)

