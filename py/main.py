from sys import platform
import asyncio
from powerClient import PowerClient
from waterClient import WaterClient
from kasaClient import KasaClient
from serverClient import ServerClient
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from threading import Timer
from datetime import datetime

import time

class Main:
    def __init__(self):
        self.testMode = platform == "win32" or platform == "win64"
        self.pollIntervalSec = 0.5
        self.verifyIntervalSec = 0.1
        self.currentPollIntervalSec = 10
    
        self.powerGpio = 24
        self.waterGpio = 23

        if platform == "win32" or platform == "win64":
            Device.pin_factory = MockFactory()

        self.powerClient = PowerClient(self.powerGpio)
        self.waterClient = WaterClient(self.waterGpio)
        self.kasaClient = KasaClient("Laundry Machine")
        self.serverClient = ServerClient(self.testMode)

        self.currentState = "on"
        self.machineIsRunning = False
        self.connected = False
        self.currentLastPollTime = 0
        self.numConsecutiveChanges = 0

        if platform == "win32" or platform == "win64":
            self.powerPin = Device.pin_factory.pin(self.powerGpio)
            self.waterPin = Device.pin_factory.pin(self.waterGpio)
            self.waterPin.drive_high()
            time.sleep(1.5)
            t = Timer(5.0, self.setWaterPin, [0])
            t.start()

    async def run(self):
        print("Initializing...")
        self.powerClient.turnOn()
        while(not self.connected):
            time.sleep(5)
            self.connected = await self.kasaClient.discover()
        await self.kasaClient.turnOn()

        print("Running...")
        while (True):
            await self.pollPlug()

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
                    await self.serverClient.triggerWaterDetectEvent()

            time.sleep(self.pollIntervalSec)

    async def pollPlug(self):
        currTime = datetime.now().timestamp()
        if currTime - self.currentLastPollTime > self.currentPollIntervalSec:
            self.currentLastPollTime = currTime
            isRunning = await self.kasaClient.isRunning()
            print(isRunning)
            if self.machineIsRunning != isRunning:
                self.numConsecutiveChanges = self.numConsecutiveChanges + 1
                if self.numConsecutiveChanges == 5:
                    self.machineIsRunning = isRunning
                    if self.machineIsRunning:
                        await self.serverClient.triggerLaundryOnEvent()
                    else:
                        await self.serverClient.triggerLaundryOffEvent()
            else:
                self.numConsecutiveChanges = 0

    def setWaterPin(self, val):
        if val == 0:
            self.waterPin.drive_low()
        else:
            self.waterPin.drive_high()

asyncio.run(Main().run())
