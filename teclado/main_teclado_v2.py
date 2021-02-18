from pynput.keyboard import Key, Controller, Listener
import pynput
import keyboard
import time

class MyKeyboard:

    controller = Controller()
    geral = []

    def on_press(self, key):
        print('{0} pressed'.format(
            key))
        self.geral.append({"pressed": key})

    def on_release(self, key):

        self.geral.append({"released": key})

        if key == Key.esc:
            return False

        print('{0} release'.format(
            key))

    def listen(self):
        with Listener(self.on_press, self.on_release) as listener:
            listener.join()
        try:
            listener.wait()
        finally:
            listener.stop()

    def playit(self):
        print('*REPLAYING*')
        for dict_key in self.geral:
            tipo, tecla = list(dict_key.items())[0]

            if tipo == 'released':
                self.controller.release(tecla)
            elif tipo == 'pressed':
                self.controller.press(tecla)

dale = MyKeyboard()
dale.listen()
dale.playit()
