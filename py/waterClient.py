from gpiozero import InputDevice

class WaterClient:
    def __init__(self, pin):
        self.gpio = InputDevice(pin)

    def read(self):
        return self.gpio.value

    def isOn(self):
        return self.read() == 0
