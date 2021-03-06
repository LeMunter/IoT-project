import time
import config
from network import WLAN
import machine
import sleeper
import pycom


def connectToWifi():
    pycom.rgbled(0x7f0000) # Yellow
    wlan = WLAN(mode=WLAN.STA)
    for cycles in range(10):
        print("Searching for network")
        nets = wlan.scan()

        for net in nets:
            if net.ssid == config.WIFI_SSID:
                print('Network found!')
                wlan.connect(net.ssid, auth=(net.sec, config.WIFI_PASSWORD), timeout=5000)
                while not wlan.isconnected():
                    machine.idle() # save power while waiting
                print(wlan.ifconfig())
                break

        if wlan.isconnected():
            return wlan

        print("Could not find network")
        time.sleep(20)
    # Go to deepsleep after failing a set amount of connections.
    sleeper.goToSleep(config.SLEEPTIME_WIFI_MS)
