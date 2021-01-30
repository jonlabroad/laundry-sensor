import asyncio
import requests

host = "https://watersensor.thejonlab.net"

class ServerClient:
    def __init__(self, testMode):
        self.testMode = testMode

    async def triggerLaundryOnEvent(self):
        payload = {'type': 'LAUNDRY_START', 'test': self.testMode}
        r = requests.post(host + "/detect", json=payload)
        print(r.status_code)
        print(r.text)
    
    async def triggerLaundryOffEvent(self):
        payload = {'type': 'LAUNDRY_END', 'test': self.testMode}
        r = requests.post(host + "/detect", json=payload)
        print(r.status_code)
        print(r.text)

    async def triggerWaterDetectEvent(self):
        payload = {'type': 'WATER_DETECTED', 'test': self.testMode}
        r = requests.post(host + "/detect", json=payload)
        print(r.status_code)
        print(r.text)

    async def triggerWaterNotDetectEvent(self):
        payload = {'type': 'WATER_NOT_DETECTED', 'test': self.testMode}
        r = requests.post(host + "/detect", json=payload)
        print(r.status_code)
        print(r.text)