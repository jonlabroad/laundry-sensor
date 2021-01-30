import asyncio
from kasa import Discover
from kasa import SmartPlug

class KasaClient:   
    def __init__(self, deviceAlias):
        self.deviceAlias = deviceAlias
        self.currentThreshold = 20

    async def discover(self):
        devices = await Discover.discover()
        for ipAddr, device in devices.items():
            if device.alias == self.deviceAlias:
                print("Found device at " + ipAddr + ": " + device.alias)
                self.device = SmartPlug(ipAddr)
        print(devices)

    async def turnOn(self):
        await self.device.turn_on()

    async def turnOff(self):
        await self.device.turn_off()

    async def getEmeter(self):
        await self.device.update()
        return self.device.emeter_realtime

    async def isRunning(self):
        powerData = await self.getEmeter()
        current = powerData['current_ma']
        return current > self.currentThreshold
    
