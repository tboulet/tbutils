from tbutils.config import instantiate_class, get_env_variable, try_get

class Class:
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
    def __repr__(self):
        return f"Class(arg1={self.arg1}, arg2={self.arg2})"
        
config_for_class = {
    "class_string": "examples.config:Class", # work if you run this script from the root of the project
    "arg1": 1,
    "arg2": 2,
}

if __name__ == "__main__":
    # Try get
    print(f"{try_get({'a': {'b': {'c': 1}}}, 'a.b.c')=}")
    print(f"{try_get({'a': 1}, 'double_a', lambda config, key: config['a'] * 2)=}")

    # Class instanciation
    print(f"Class instanciation from config: {config_for_class}")
    obj = instantiate_class(**config_for_class)
    print(f"Obj: {obj}")
    # Environment variable
    print(f"Environment variable: {get_env_variable('USERNAME')}")