import { Gpio } from 'onoff';

export default class WaterClient {
    gpio: Gpio;

    constructor(pin: number) {
        this.gpio = new Gpio(pin, 'in');
    }

    read() {
        return this.gpio.readSync();
    }

    isOn() {
        return this.read() === 0;
    }
}