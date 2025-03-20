import sys
from typing import Any, Dict, Tuple, Union
import importlib
import numpy as np


def get_dict_flattened(d: Dict, parent_key="", sep="."):
    """Get a flattened version of a nested dictionary, where keys correspond to the path to the value.

    Args:
        d (Dict): The dictionary to be flattened.
        parent_key (str): The base key string (used in recursive calls).
        sep (str): Separator to use between keys.

    Returns:
        Dict: The flattened dictionary.
    """
    items = []
    for k, v in d.items():
        assert not sep in k, f"Separator {sep} is not allowed in keys"
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(get_dict_flattened(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def unflatten_dict(d: Dict, sep="."):
    """Unflatten a dictionary that was flattened using get_dict_flattened.

    Args:
        d (Dict): The dictionary to be unflattened.
        sep (str): Separator used between keys.

    Returns:
        Dict: The unflattened dictionary.
    """
    res = {}
    for key, value in d.items():
        keys = key.split(sep)
        current = res
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
    return res

def get_shape(
    obj: Any,
    authorized_types: Tuple[type] = (np.ndarray, list, tuple, set, dict),
    assert_same_shape: bool = False,
) -> Tuple[int]:
    """Returns the shape of the object.
    If the object is a list, tuple, set or np.ndarray, it will return the shape of the object.
    If the object is not of the authorized types, it will return an empty tuple.

    This function makes the assumption that the object is a nested structure where sub-objects have the same shape.
    If assert_same_shape is True, it will assert that all sub-objects have the same shape.

    Args:
        object (Any): the object
        authorized_types (Tuple[type], optional): the authorized types for the object. Defaults to (np.ndarray, list, tuple, set).

    Returns:
        Tuple[int]: the shape of the object
    """
    if isinstance(obj, authorized_types):
        if len(obj) == 0:
            return (0,)
        if isinstance(obj, dict):
            obj = obj.values()
            shape = get_shape(list(obj), authorized_types, assert_same_shape)
            return f"Dict({len(obj)} keys to {shape})"
        first_shape = get_shape(next(iter(obj)), authorized_types, assert_same_shape)
        
        if assert_same_shape:
            sub_shapes = [get_shape(el, authorized_types, assert_same_shape) for el in obj]
            if any(shape != first_shape for shape in sub_shapes):
                raise AssertionError("All sub-objects must have the same shape, but got: ", sub_shapes)

        return (len(obj), *first_shape)
    
    return ()
