# Traffic light for Kraktakara
# 120mA / light = 360mA

import time
import pigpio

from cie1931 import cie
import functions

pi = pigpio.pi()

RedPin = 17
YellowPin = 22
GreenPin = 24


def setled(pin, brightness):
    linearised = cie[round(brightness * 255)]  # Linearise led intensity (In 0<255 Out 0<1023)
    pi.set_PWM_dutycycle(pin, linearised / 4)  # Set GPIO output PWM (0<255)


def loop():
    beat_length = 0.5  # 120BPM Equivalent
    start_time = time.time()
    time_since_start = .0
    last_beat_time = .0
    time_since_beat = .0
    beats_since_start = 0
    position_in_beat = .0

    func = functions.test  # Fonction test
    func_steps = func["steps"]
    func_length = func["length"]

    while True:
        current_time = time.time()
        time_since_start = current_time - start_time
        time_since_beat = time_since_start - last_beat_time
        position_in_beat = time_since_beat / beat_length
        if time_since_beat > beat_length:
            last_beat_time = time_since_start
            time_since_beat = .0
            beats_since_start += 1
            position_in_beat = .0
        # print(time_since_start, beats_since_start+position_in_beat)

        beat = beats_since_start % func_length

        # Implémenter l'interpolation linéaire ici

        setled(RedPin, 0)
        setled(YellowPin, 0)
        setled(GreenPin, 0)


if __name__ == '__main__':
    loop()
