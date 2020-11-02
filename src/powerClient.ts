import { Gpio } from 'onoff';

export default class PowerClient {
    gpio: Gpio;

    constructor(pin: number) {
        this.gpio = new Gpio(pin, 'out');
    }

    turnOn() {
        this.gpio.writeSync(1);
    }

    turnOff() {
        this.gpio.writeSync(0);
    }

    read() {
        return this.gpio.readSync();
    }

    isOn() {
        return this.read() === 1;
    }
}