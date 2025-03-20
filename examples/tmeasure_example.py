import time
from tbutils.tmeasure import RuntimeMeter

def foo():
    time.sleep(0.1)

def bar():
    time.sleep(0.2)

if __name__ == "__main__":
    for _ in range(3):
        with RuntimeMeter("foo function"):
            foo()
        with RuntimeMeter("bar function"):
            bar()

    print(RuntimeMeter.get_stage_runtime("foo function"))
    print(RuntimeMeter.get_stage_runtime("bar function"))
    print(RuntimeMeter.get_stage_runtime("total"))