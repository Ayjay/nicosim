import sys

tick_rate = 30
ticks_per_min = tick_rate * 60

input_rate = 390
input_belt = 480
input_buffer = 0

left_rate = 280
left_belt = 480
left_buffer = 0

right_rate = 110
right_belt = 120
right_buffer = 0

def timed_eventer(interval, action):
    time_interval = (ticks_per_min / interval) if interval > 0 else 0
    time_until_action = 0
    while True:
        time_until_action += time_interval
        while time_until_action > 0:
            time_until_action -= 1
            yield None
        yield action()

def generate_input():
    global input_buffer
    input_buffer += 1

def sink_left():
    global left_buffer
    if left_buffer > 0:
        left_buffer -= 1

def sink_right():
    global right_buffer
    if right_buffer > 0:
        right_buffer -= 1

def splitter():
    global input_buffer,left_buffer,right_buffer
    if input_buffer > 0:
        if left_buffer == 0:
            left_buffer += 1
        else:
            right_buffer += 1
        input_buffer -= 1

actions = [
    timed_eventer(input_rate, generate_input),
    timed_eventer(left_rate, sink_left),
    timed_eventer(right_rate, sink_right),
    timed_eventer(0, splitter),
]
for _ in range(30*60*tick_rate):
    for action in actions:
        next(action)

print(f'input_buffer: {input_buffer} left_buffer: {left_buffer} right:buffer: {right_buffer}')
