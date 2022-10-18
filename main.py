# Traffic light for Kraktakara
# 120mA / light = 360mA

from time import perf_counter as timer, sleep
import pigpio

from cie1931 import cie
import functions

pi = pigpio.pi()

RedPin = 17
YellowPin = 22
GreenPin = 24

steps = functions.long_fade_from_black

bpm = 120
bps = bpm / 60


def setled(pin, brightness):
    linearised = cie[round(brightness * 255)]  # Linearise led intensity (In 0<255 Out 0<1023)
    pi.set_PWM_dutycycle(pin, linearised / 4)  # Set GPIO output PWM (0<255)


def lerp(decimal_beat: float, prev_step_idx: int, next_step_idx: int):
    prev_step = steps[prev_step_idx]
    if next_step_idx < len(steps):
        next_step = steps[next_step_idx]
        prev_beat = prev_step[0]
        next_beat = next_step[0]
    else:
        next_step = steps[0]
        prev_beat = prev_step[0]
        next_beat = len(steps)+1

    prev_step = prev_step[1]
    next_step = next_step[1]

    assert prev_beat <= decimal_beat <= next_beat, f"{prev_beat}, {decimal_beat}, {next_beat}"
    progress = (decimal_beat - prev_beat) / (next_beat - prev_beat)

    return tuple(
        prev + (next - prev) * progress
        for prev, next in zip(prev_step, next_step)
    )


start_time = timer()
while True:
    rel_time = timer() - start_time
    length = steps[len(steps)-1][0]
    decimal_beat = (rel_time * bps)%length

    # Find the previous and the current step
    next_step_idx = 0
    while next_step_idx < len(steps) and steps[next_step_idx][0] < decimal_beat:
        next_step_idx += 1
    prev_step_idx = max(0, next_step_idx - 1)

    if next_step_idx >= len(steps):
        prev_step_idx = 0
        next_step_idx = 0
    pos = lerp(decimal_beat, prev_step_idx, next_step_idx)

    print("At time {:.03f}, beat {:.03f}".format(rel_time, decimal_beat), end="")
    print(", pos: {:.02f}, {:.02f}, {:.02f}".format(*pos))

    setled(RedPin, pos[0])
    setled(YellowPin, pos[1])
    setled(GreenPin, pos[2])

    sleep(0.01)
