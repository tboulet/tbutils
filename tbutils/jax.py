import importlib
from typing import Any, Dict, List, Union
from abc import ABC, abstractmethod
from functools import partial

if importlib.util.find_spec("jax") is not None:
    import jax
    from jax import random
    import jax.numpy as jnp
    import numpy as np
    from jax.lib import xla_bridge


def check_jax_device():
    try:
        print("Checking device used by JAX:")
        print(f"\tAvailable devices: {jax.devices()}")
        print(f"\tPlatform: {xla_bridge.get_backend().platform}")
    except Exception as e:
        print(f"Error while checking JAX device: {e}")


def nest_for_array(func):
    """Decorator to allow a function to be applied to nested arrays.

    Args:
        func (function): the function to decorate

    Returns:
        function: the decorated function
    """

    def wrapper(arr, *args, **kwargs):
        if isinstance(arr, jnp.ndarray):
            return func(arr, *args, **kwargs)
        elif isinstance(arr, dict):
            if "key_random" in kwargs:
                key_random = kwargs["key_random"]
                del kwargs["key_random"]
                for key, value in arr.items():
                    key_random, subkey = random.split(key_random)
                    arr[key] = wrapper(value, *args, key_random=subkey, **kwargs)
            else:
                for key, value in arr.items():
                    arr[key] = wrapper(value, *args, **kwargs)
            return arr
        elif isinstance(arr, list):
            if "key_random" in kwargs:
                key_random = kwargs["key_random"]
                del kwargs["key_random"]
                for idx, value in enumerate(arr):
                    key_random, subkey = random.split(key_random)
                    arr[idx] = wrapper(value, *args, key_random=subkey, **kwargs)
            else:
                for idx, value in enumerate(arr):
                    arr[idx] = wrapper(value, *args, **kwargs)
            return arr
        else:
            raise ValueError(f"Unknown type for array: {type(arr)}")

    return wrapper
