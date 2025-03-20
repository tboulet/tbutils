import sys
from typing import Any, Dict, Tuple, Union
import importlib
import numpy as np


from tbutils.struct import get_dict_flattened, unflatten_dict, get_shape

if __name__ == "__main__":
    # Test get_dict_flattened and unflatten_dict
    d = {
        "key1": 1,
        "key2": {"key3": 3, "key4": {"key5": 5}},
        "key6": {"key7": 7},
    }
    print(f"Testing get_dict_flattened with {d}")
    flattened = get_dict_flattened(d)
    print(f"Flattened: {flattened}")
    unflattened = unflatten_dict(flattened)
    print(f"Unflattened: {unflattened}")

    # Test get_shape
    print(f"{get_shape([[1, 2], [3, 4]])=}")
    print(f"{get_shape(np.array([[1, 2], [3, 4]]))=}")
    print(f"{get_shape({1: [1, 2], 2: (1, 2), 3: {1, 2}})=}")
    # Test get_shape with assert_same_shape=True
    print(f"{get_shape([[[None, None, None, None, None, None, None], [4]], [None, [7, 8]]])=}")
    try:
        print(f"{get_shape([[[None, None, None, None, None, None, None], [4]], [None, [7, 8]]], assert_same_shape=True)=}")
    except AssertionError as e:
        print(f"AssertionError was raised: {e}")
    