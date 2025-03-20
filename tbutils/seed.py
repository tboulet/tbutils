import os
from typing import Dict, Type, Any, Tuple, Union
import random
import sys

from tbutils.exec_max_n import print_once
from tbutils.config import try_get


def try_get_seed(
    config: Dict,
    seed_max: int = 1000,
    key_seed: str = "seed",
    warn_if_unvalid: bool = True,
) -> int:
    """Will try to extract the seed from the config, or return a random one if not found

    Args:
        config (Dict): the run config
        seed_max (int, optional): the maximum value for the random seed. Defaults to 1000.
        key_seed (str, optional): the key to look for in the config. Defaults to "seed".
        warn_if_unvalid (bool, optional): whether to warn if the seed is not an integer. Defaults to True.

    Returns:
        int: the seed
    """
    # Extract the seed from the config. If not found, a random seed will be used
    seed = try_get(
        config=config,
        key=key_seed,
        default=random.randint(0, seed_max - 1),
        warn_if_unvalid=False, # dont warn if seed is not found
    )
    # If seed is found but not an integer, use a random seed instead and raise a warning if warn_if_unvalid
    if not isinstance(seed, int):
        seed = random.randint(0, seed_max - 1)
        if warn_if_unvalid:
            print_once(
                f"[WARNING] The seed is not an integer, using a random seed instead: {seed}"
            )
    return seed



def set_seed(seed: int):
    """Set the seed for reproducibility.
    This function will set the seed for Python, Numpy, PyTorch and TensorFlow, but only if the corresponding library is already imported.

    Args:
        seed (int): the seed to set
    """
    # Python
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    # Numpy
    if "numpy" in sys.modules:
        import numpy as np

        np.random.seed(0)

    # PyTorch
    if "torch" in sys.modules:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

        # This flag only allows cudnn algorithms that are determinestic unlike .benchmark
        torch.backends.cudnn.deterministic = True

        # this flag enables cudnn for some operations such as conv layers and RNNs,
        # which can yield a significant speedup.
        torch.backends.cudnn.enabled = False

        # This flag enables the cudnn auto-tuner that finds the best algorithm to use
        # for a particular configuration. (this mode is good whenever input sizes do not vary)
        torch.backends.cudnn.benchmark = False

    # TensorFlow
    if "tensorflow" in sys.modules:
        import tensorflow as tf

        tf.random.set_seed(seed)
