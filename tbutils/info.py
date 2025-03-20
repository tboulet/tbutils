import sys
import platform
import importlib.util


def is_installed(package_name):
    return importlib.util.find_spec(package_name) is not None


def check_versions():
    python_version = sys.version.split(" ")[0]
    system_name = platform.system()
    machine = platform.machine()

    print("\n============== Checking Packages & System Info ================")
    print(f"OS: {system_name} ({machine})")
    print(f"Python: {python_version}")

    # NumPy
    if is_installed("numpy"):
        import numpy as np

        print(f"NumPy: {np.__version__}")

    # PyTorch
    if is_installed("torch"):
        import torch

        print(f"PyTorch: {torch.__version__}")
        print(f"\tCUDA Available: {torch.cuda.is_available()}")
        print(
            f"\tCUDA Version: {torch.version.cuda if torch.cuda.is_available() else 'N/A'}"
        )
        print(f"\tAvailable GPUs: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"\t  - GPU {i}: {torch.cuda.get_device_name(i)}")

    # TensorFlow
    if is_installed("tensorflow"):
        import tensorflow as tf

        print(f"TensorFlow: {tf.__version__}")
        print(f"\tCUDA Available: {tf.test.is_built_with_cuda()}")
        print(f"\tAvailable GPUs: {len(tf.config.list_physical_devices('GPU'))}")
        for gpu in tf.config.list_physical_devices("GPU"):
            print(f"\t  - {gpu}")

    # JAX
    if is_installed("jax"):
        import jax
        from jax.lib import xla_bridge

        print(f"JAX: {jax.__version__}")
        print(f"\tAvailable Devices: {jax.devices()}")
        print(f"\tPlatform: {xla_bridge.get_backend().platform}")

    print("===============================================================")
