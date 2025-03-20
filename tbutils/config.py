import importlib
from typing import Any, Callable, Dict, List, Union
from abc import ABC, abstractmethod
from functools import partial

import os
import hydra
from omegaconf import OmegaConf

from tbutils.exec_max_n import print_once


def try_get(
    config: Dict,
    key: str,
    default: Union[Any, Callable] = None,
    warn_if_unvalid: bool = False,
    sep: str = ".",
) -> Any:
    """
    Will try to extract the (splitted) key from the config, or return 'default' of 'default(kwargs)' if not found.

    If the key is of the form 'key1.key2.key3' (or with other 'sep'), it will search for the equivalent of 'config['key1']['key2']['key3']'

    In case default is a function, this function will be called with kwargs config=config and key=key depending on what it supports

    Args:
        config (Dict): the run config
        key (str): the key to look for in the config, as a string or a dot-separated string representing a path in the config
        default (Union[Any, Callable], optional): the default value to return/function to call if the key is not found. Defaults to None.
        warn_if_unvalid (bool, optional): whether to warn if the key is not found. Defaults to False.
        sep (str, optional): the separator to split the key. Defaults to ".".
        
    Returns:
        int: the seed
    """
    key_split = key.split(sep)
    value = config
    for subkey in key_split:
        if subkey in value:
            value = value[subkey]
        else:
            if callable(default):
                kwargs_default = {}
                if "config" in default.__code__.co_varnames:
                    kwargs_default["config"] = config
                if "key" in default.__code__.co_varnames:
                    kwargs_default["key"] = key
                default_value = default(**kwargs_default)
            else:
                default_value = default
            if warn_if_unvalid:
                print_once(
                    f"[tbutils.config WARNING] The key {key} is not found ({subkey} not in config/subconfig), using a default value: {default_value}",
                    discr_obj=key,
                )
            return default_value
    return value


def merge_container(*containers):
    """Merge containers of the same type (list, dict, tuple) into one container."""
    containers = [OmegaConf.to_container(container) for container in containers]
    if all(isinstance(container, list) for container in containers):
        return [item for container in containers for item in container]
    elif all(isinstance(container, dict) for container in containers):
        return {
            key: value for container in containers for key, value in container.items()
        }
    elif all(isinstance(container, tuple) for container in containers):
        return tuple(item for container in containers for item in container)
    else:
        raise ValueError(
            f"All containers should be of the same type, but got {[type(container) for container in containers]}"
        )


def get_env_variable(name: str):
    """Get the value of an environment variable."""
    return os.environ.get(name)


def register_hydra_resolvers():
    """Register the custom Hydra resolvers.

    Example usage :
    ```yaml
    # configs/default.yaml
    key1: value1
    key2: ${eval:'${key1} /2'}
    ```
    """
    OmegaConf.register_new_resolver("merge", merge_container)
    OmegaConf.register_new_resolver("eval", eval)
    OmegaConf.register_new_resolver("env_variable", get_env_variable)


def instantiate_class(**kwargs) -> Any:
    """Instantiate a class from a dictionnary that contains a key "class_string" with the format "path.to.module:ClassName"
    and that contains other keys that will be passed as arguments to the class constructor

    Args:
        config (dict): the configuration dictionnary
        **kwargs: additional arguments to pass to the class constructor

    Returns:
        Any: the instantiated class
    """
    assert (
        "class_string" in kwargs
    ), "The class_string should be specified in the config"
    class_string: str = kwargs["class_string"]
    module_name, class_name = class_string.split(":")
    module = importlib.import_module(module_name)
    Class = getattr(module, class_name)
    object_config = kwargs.copy()
    object_config.pop("class_string")
    return Class(**object_config)
