
from tbutils.seed import try_get_seed, set_seed

if __name__ == "__main__":
    print(f"Try get seed on a config with seed: {try_get_seed({'seed': 42})}")
    print(f"Try get seed on a config without seed: {try_get_seed({})}")
    print(f"Try get seed on a config with non-integer seed: {try_get_seed({'seed': '42'})}")

    set_seed(42)
