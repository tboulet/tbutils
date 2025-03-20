# tbutils

```tbutils``` is a Python package that provides a set of utility functions. Main features are explained below and you can find information in the docstrings of the functions and examples in the folder ```examples/```.

# Installation

You can install the package using pip:

```bash
pip install tbutils
```

Or you can install it from the source code:

```bash
pip install git+https://github.com/tboulet/tbutils.git
```

## tbutils.config

This module provides functions to interact with configuration files, mostly under the Hydra framework.

The ```try_get(config, key, default)``` function act as the dictionary.get() method with two improvements :
- It can search recursively for value in nested dictionnary, such as ```try_get(config, "a.b.c", default)```
- ```default``` can also be a callable, called if the key is not found in the config, with arguments ```(config, key)``` depending on if ```default``` support them

```python
from tbutils.config import try_get

abc = try_get({"a": {"b": {"c": 1}}}, "a.b.c", 0)

double_a = try_get({"a": 1}, "double_a", lambda config: config["a"] * 2)
```

## tbutils.info

The function ```tbutils.info.check_version()``` will print the version of python, your machine, and numpy/torch/tensorflow/JAX versions and associated devices and compatibility.

```python
from tbutils.info import check_version
check_version()
```

Output example:

```bash
============= Checking Packages & System Info ============
OS: Windows (AMD64)
Python: 3.9.7
NumPy: 2.0.2
PyTorch: 2.5.1+cpu
        CUDA Available: False
        CUDA Version: N/A
        Available GPUs: 0
JAX: 0.4.30
        Available Devices: [CpuDevice(id=0)]
        Platform: cpu
==========================================================
```

### tbutils.exec_max_n

This module will provide functions and decorators to run something (either print, log from a logger, or execute a function) only once. This is useful to avoid printing the same message multiple times, or to avoid running the same function multiple times.

Printing and logging will use the str(message) as a key to check if the message has already been printed or logged.
```python
from tbutils.exec_max_n import print_once, print_max_n, log_once, log_max_n, exec_once, exec_max_n

for _ in range(10):
    # Printing
    print_once("This will be printed only once")
    print_max_n("This will be printed 3 times", 3)
    # Logging (using the logging module)
    logger = logging.getLogger(__name__)
    log_once(logger, "This will be logged only once")
    log_max_n(logger, "This will be logged 3 times", 3)
```

Function number-of-execution bounding works by using a decorator
```python
# Executing a function
@exec_once
def add(a, b):
    return a + b
for k in range(5):
    print(f"Addition result: {add(k, k+1)}")

# Executing a function with a maximum number of executions
def sub(a, b):
    return a - b
sub = exec_max_n(sub, 3)
for k in range(5):
    print(f"Subtraction result: {sub(k, k+1)}")
```

Rather than printing/logging `x` maximum `n` times depending on `x`, you can specify a discriminator object or function different than `x` to differentiate between what has to be printed/logged and what will be used as the key to check if the message has already been printed/logged.

```python	
for k in [5, 9, 13, 14, 15, 16, 25]:
    print_once(f"A number of a new ten was detected : {k}", discr_obj=k, discr_fn=lambda x: x // 10)
```

Output :

```bash
A number of a new ten was detected : 5
A number of a new ten was detected : 13
A number of a new ten was detected : 25
```


### tbutils.seed

The function ```tbutils.seed.try_get_seed(config)``` will try to get the seed from a config dict, or return a random seed if not found. 

```python	
from tbutils.seed import try_get_seed
config = {"seed": "unvalid seed"}
seed = try_get_seed(config)
print(seed)
```

The function ```tbutils.seed.set_seed(seed)``` will set the seed for native python, numpy, torch, and tensorflow. It does that only if these libraries are already installed and imported.

### tbutils.struct

This module allows you to flatten/unflatten a nested dictionary.

It also contains the function ```tbutils.struct.get_shape(obj)``` that will return the shape of a nested object (made of numpy arrays, list, tuple, dict, etc.).

### tbutils.tmeasure

This module provides a context manager to measure the time spent in blocks of code and make available data about the average/cumulative time spent in these blocks. Useful to profile your code if divided into blocks (loading, rendering, training, inference, etc.).

```python
import time
from tmeasure import RuntimeMeter

def foo():
    time.sleep(0.1)

def bar():
    time.sleep(0.2)

for _ in range(3):
    with RuntimeMeter("foo function"):
        foo()
    with RuntimeMeter("bar function"):
        bar()

print(RuntimeMeter.get_stage_runtime("foo function"))
print(RuntimeMeter.get_stage_runtime("bar function"))
print(RuntimeMeter.get_stage_runtime("total"))
```

Output :

```
0.3361208438873291
0.6190340518951416
0.9551548957824707
```