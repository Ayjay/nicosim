import sys

tick_rate = 30
ticks_per_min = tick_rate * 60

input_rate = 390
input_belt = 480
input_buffer = 0

debug = False
if debug:
    debugprint = print
else:
    def debugprint(x): pass

class OutputBelt:
    name = ""
    sink_rate = 280
    belt_rate = 480
    entry = 0
    buffer = 0
    buffer_limit = 0
    total = 0

    def __init__(self,name,sink_rate,belt_rate,buffer_limit):
        self.name = name
        self.sink_rate = sink_rate
        self.belt_rate = belt_rate
        self.buffer_limit = buffer_limit
    
    def item_enter(self):
        if self.entry == 0:
            debugprint(f'{self.name}: item enters')
            self.entry = 1
            return True
        return False
    
    def belt_move(self):
        if self.entry == 1 and self.buffer < self.buffer_limit:
            debugprint(f'{self.name}: moves item to buffer')
            self.buffer += 1
            self.entry = 0
    
    def sink(self):
        if self.buffer > 0:
            debugprint(f'{self.name}: item taken from buffer')
            self.buffer -= 1
            self.total += 1

left = OutputBelt('left', 280, 480, 200)
right = OutputBelt('right', 110, 120, 200000)

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
    debugprint(f'input generated')

def splitter():
    global input_buffer
    if input_buffer > 0 and \
       (left.item_enter() or right.item_enter()):
            input_buffer -= 1

actions = [
    timed_eventer(input_rate, generate_input),
    timed_eventer(0, splitter),
    timed_eventer(left.belt_rate, left.belt_move),
    timed_eventer(left.sink_rate, left.sink),
    timed_eventer(right.belt_rate, right.belt_move),
    timed_eventer(right.sink_rate, right.sink),
]
if debug:
    ticks = 10*tick_rate
else:
    ticks = 30*60*tick_rate
for _ in range(ticks):
    for action in actions:
        next(action)

print(f'input_buffer: {input_buffer}')
print(f'left.buffer: {left.buffer} left.total {left.total}')
print(f'right.buffer: {right.buffer} right.total {right.total}')
