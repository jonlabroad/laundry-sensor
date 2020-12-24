from sys import platform
from powerClient import PowerClient
from waterClient import WaterClient
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from threading import Timer

import time

class Main:
    def __init__(self):
        self.pollIntervalSec = 0.5
        self.verifyIntervalSec = 0.1
    
        self.powerGpio = 21
        self.waterGpio = 20

        if platform == "win32" or platform == "win64":
            Device.pin_factory = MockFactory()           

        self.powerClient = PowerClient(self.powerGpio)
        self.waterClient = WaterClient(self.waterGpio)

        self.currentState = "on"

        if platform == "win32" or platform == "win64":
            self.powerPin = Device.pin_factory.pin(self.powerGpio)
            self.waterPin = Device.pin_factory.pin(self.waterGpio)
            self.waterPin.drive_high()
            time.sleep(1.5)
            t = Timer(5.0, self.setWaterPin, [0])
            t.start()

    def run(self):
        print("Running...")
        self.powerClient.turnOn()
        while (True):
            if self.currentState == "on" and not self.powerClient.isOn():
                print("TURNING ON")
                self.powerClient.turnOn()
            elif self.currentState == "cutoff" and self.powerClient.isOn():
                print("CUTTING POWER")
                self.powerClient.turnOff()

            if self.currentState == "on" and self.waterClient.isOn():
                print("WATER DETECTED. VERIFYING...")
                verified = True
                for i in range(5):
                    time.sleep(self.verifyIntervalSec)
                    verified = verified and self.waterClient.isOn()
                    print(verified)

                if verified:
                    print("SHUTTING OFF POWER")
                    self.powerClient.turnOff()
                    self.currentState = "cutoff"

                    # TODO alert via AWS

            time.sleep(self.pollIntervalSec)

    def setWaterPin(self, val):
        if val == 0:
            self.waterPin.drive_low()
        else:
            self.waterPin.drive_high()

Main().run()
