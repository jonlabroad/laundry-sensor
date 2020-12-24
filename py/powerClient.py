from gpiozero import OutputDevice

class PowerClient:
    def __init__(self, pin):
        self.gpio = OutputDevice(pin)

    def turnOn(self):
        self.gpio.on()

    def turnOff(self):
        self.gpio.off()

    def read(self):
        return self.gpio.value

    def isOn(self):
        return self.read() == 1
