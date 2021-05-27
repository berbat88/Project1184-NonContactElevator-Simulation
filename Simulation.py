import time
import threading
import can

can_interface = 'can0'
bus = can.interface.Bus(can_interface, bustype='socketcan', bitrate=500000)

TargetFloor = set()
CurrentFloor = 0


class CanCheck(threading.Thread):
    def __init__(self, stopper):
        threading.Thread.__init__(self)
        self.stopper = stopper

    def run(self):
        while not self.stopper.is_set():
            while 1:
                message = bus.recv()
                msg = str(message)
                msg2 = int(msg)

                TargetFloor.add(msg2)
                print("New target floor :", msg2)


stop = threading.Event()
worker = CanCheck(stop)
worker.start()


def elevatormoveasc(x):
    maxfl = list(TargetFloor)[-1]

    print("Elevator starts ascending... ↑")

    while x < maxfl + 1:
        delayt()
        print("Current Floor:", x, "↑")

        if x in TargetFloor:
            TargetFloor.discard(x)
            arrivedelayt(x)

            if x == maxfl:
                break
            else:
                print("Elevator starts ascending... ↑")

        x += 1

    return x


def elevatormovedesc(x):
    minfl = list(TargetFloor)[0]

    print("Elevator starts descending... ↓")

    while x > minfl - 1:
        delayt()
        print("Current Floor:", x, " ↓")

        if x in TargetFloor:
            TargetFloor.discard(x)
            arrivedelayt(x)

            if x == minfl:
                break
            else:
                print("Elevator starts descending... ↓")

        x -= 1

    return x


def delayt():
    time.sleep(1)


def arrivedelayt(x):
    time.sleep(1)
    print("Elevator doors opened...")
    time.sleep(1)
    if ((len(TargetFloor)) > 0):
        print("Elevator Stopped at: Floor number ", x)
        print("Targets left to go: ", TargetFloor)
    else:
        print("No more target to go.")
        time.sleep(0.5)
        print("Waiting for input")
    time.sleep(1)
    print("Elevator doors closed.")
    time.sleep(1)


print("Initial Targets: ", TargetFloor)

print("Starting Floor: ", CurrentFloor)

print("-----------------------------")

while 1:
    time.sleep(0.25)
    if len(TargetFloor) > 0:
        if list(TargetFloor)[0] >= CurrentFloor:
            CurrentFloor = elevatormoveasc(CurrentFloor)

        else:
            CurrentFloor = elevatormovedesc(CurrentFloor)
