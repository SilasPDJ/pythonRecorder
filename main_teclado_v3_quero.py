from pynput.keyboard import Key, Controller, Listener
import pynput
import keyboard
import time
from datetime import datetime as dt


class MyKeyboard:

    controller = Controller()
    geral = []
    live_time_program = time.time()

    start = time.time()
    ss_count = False

    def on_press(self, key):
        if not self.ss_count:
            self.start = time.time()
            self.ss_count = True
        self.geral.append({"pressed": key})

    def on_release(self, key):
        if key == Key.f8:
            return False

        appended = {"released": key, 'time_taken': self.get_time_taken()}
        self.geral.append(appended)
        print(appended['time_taken'])

    def get_time_taken(self):
        end = time.time()
        self.ss_count = False

        return round(end - self.start, 2)

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
                # tempo = list(dict_key.items())[1][1]
                tempo = dict_key['time_taken']
                time.sleep(tempo)
                self.controller.release(tecla)
            elif tipo == 'pressed':
                self.controller.press(tecla)

dale = MyKeyboard()
dale.listen()
dale.playit()
