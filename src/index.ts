import PowerClient from "./powerClient";
import Util from "./util";
import WaterClient from "./waterClient";

export type PowerState = "on" | "cutoff";

export const run = async () => {
    const pollIntervalMs = 500;
    const verifyInterval = 100;
    
    const powerGpio = 21;
    const waterGpio = 20;

    const powerClient = new PowerClient(powerGpio);
    const waterClient = new WaterClient(waterGpio);

    let currentState = "on";

    console.log("Running...");
    powerClient.turnOn();
    while (true) {
        if (currentState === "on" && !powerClient.isOn()) {
            console.log("TURNING ON");
            powerClient.turnOn();
        } else if (currentState === "cutoff" && powerClient.isOn()) {
            console.log("CUTTING POWER");
            powerClient.turnOff();
        }

        if (currentState === "on" && waterClient.isOn()) {
            console.log("WATER DETECTED. VERIFYING...");
            let verified = true;
            for (let i = 0; i < 5; i++) {
                await Util.sleep(verifyInterval);
                verified = verified && waterClient.isOn();
                console.log(verified);
            }

            if (verified) {
                console.log("SHUTTING OFF POWER");
                powerClient.turnOff();
                currentState = "cutoff";

                // TODO alert via AWS
            }            
        }

        await Util.sleep(pollIntervalMs);
    }
}

run();
