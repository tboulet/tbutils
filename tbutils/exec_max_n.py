from collections import defaultdict
from logging import INFO, WARNING, Logger
from typing import Any, Callable, Dict, Union


def obj_to_discr_obj(obj: Any, discr_obj: Any, discr_fn: Callable[[Any], Any]) -> Any:
    """Get the obj to discriminate on.

    Args:
        obj (Any): The obj to discriminate on.
        discr_obj (Any): The obj to discriminate on.
        discr_fn (Callable[[Any], Any]): The function to discriminate on.

    Returns:
        Any: The obj to discriminate on.
    """
    if discr_obj is None:
        discr_obj = obj
    if discr_fn is not None:
        discr_obj = discr_fn(discr_obj)
    return discr_obj


dict_printing_objs_counter: Dict[str, int] = defaultdict(int)


def print_max_n(
    obj: Any,
    n: int,
    discr_obj: str = None,
    discr_fn: Callable[[Any], Any] = None,
    show_counter: bool = False,
):
    """Print an obj only if it has been printed less than n times.
    If discr_obj is specified, the discrimation is based on that obj.
    If discr_fn is specified, the discrimation is based on discr_fn(obj) (or discr_fn(discr_obj) if specified).

    Args:
        obj (Any): The obj to print.
        n (int): The maximum number of times the obj can be printed.
        discr_obj (str, optional): The obj to discriminate on. Defaults to None (go back to using the obj itself).
        discr_fn (Union[Callable[[Any], Any], str], optional): The function to discriminate on. Defaults to None (go back to using the obj/discr_obj itself).
        show_counter (bool, optional): Whether to show the counter. If True, f"{obj} ({counter}/{n})" will be printed. Defaults to False.
    """
    discr_obj = obj_to_discr_obj(obj, discr_obj, discr_fn)
    if dict_printing_objs_counter[discr_obj] < n:
        if show_counter:
            print(f"{obj} ({dict_printing_objs_counter[discr_obj]+1}/{n})")
        else:
            print(obj)
        dict_printing_objs_counter[discr_obj] += 1


def print_once(
    obj: Any,
    discr_obj: str = None,
    discr_fn: Callable[[Any], Any] = None,
    show_counter: bool = False,
):
    """Print an obj only if it has never been printed.
    If discr_obj is specified, the discrimation is based on that obj.
    If discr_fn is specified, the discrimation is based on discr_fn(obj) (or discr_fn(discr_obj) if specified).

    Args:
        obj (Any): The obj to print.
        discr_obj (str, optional): The obj to discriminate on. Defaults to None (go back to using the obj itself).
        discr_fn (Union[Callable[[Any], Any], str], optional): The function to discriminate on. Defaults to None (go back to using the obj/discr_obj itself).
        show_counter (bool, optional): Whether to show the counter. If True, f"{obj} ({counter}/{n})" will be printed. Defaults to False.
    """
    return print_max_n(obj, 1, discr_obj, discr_fn, show_counter)


dict_log_objs_counter: Dict[str, int] = defaultdict(int)


def log_max_n(
    logger: Logger,
    obj: str,
    n: int,
    discr_obj: str = None,
    discr_fn: Callable[[Any], Any] = None,
    level: int = INFO,
    show_counter: bool = False,
    *args,
    **kwargs,
):
    """Log a <level> logging obj using a logging.Logger only if it has been logged less than n times.
    If discr_obj is specified, the discrimation is based on that obj.
    If discr_fn is specified, the discrimation is based on the output of that function, applied to the obj or discr_obj if specified.

    Args:
        logger (Logger): The logger to log the obj.
        obj (str): The obj to log.
        n (int): The maximum number of times the obj can be logged.
        discr_obj (str, optional): The obj to discriminate on. Defaults to None (go back to using the obj itself).
        discr_fn (Union[Callable[[Any], Any], str], optional): The function to discriminate on. Defaults to None (go back to using the obj/discr_obj itself).
        level: The level at which to log the obj.
        show_counter (bool, optional): Whether to show the counter. If True, f"{obj} ({counter}/{n})" will be logged. Defaults to False.
        args: The arguments to pass to the logger.
        kwargs: The keyword arguments to pass to the logger
    """
    discr_obj = obj_to_discr_obj(obj, discr_obj, discr_fn)
    if dict_log_objs_counter[discr_obj] < n:
        if show_counter:
            obj = f"{obj} ({dict_log_objs_counter[discr_obj]+1}/{n})"
        logger.log(level, obj, *args, **kwargs)
        dict_log_objs_counter[discr_obj] += 1


def log_once(
    logger: Logger,
    obj: str,
    discr_obj: str = None,
    discr_fn: Callable[[Any], Any] = None,
    level: int = INFO,
    show_counter: bool = False,
    *args,
    **kwargs,
):
    """Log a <level> logging obj using a logging.Logger only if it has never been logged.
    If discr_obj is specified, the discrimation is based on that obj.
    If discr_fn is specified, the discrimation is based on the output of that function, applied to the obj or discr_obj if specified.

    Args:
        logger (Logger): The logger to log the obj.
        obj (str): The obj to log.
        discr_obj (str, optional): The obj to discriminate on. Defaults to None (go back to using the obj itself).
        discr_fn (Union[Callable[[Any], Any], str], optional): The function to discriminate on. Defaults to None (go back to using the obj/discr_obj itself).
        level: The level at which to log the obj.
        show_counter (bool, optional): Whether to show the counter. If True, f"{obj} ({counter}/{n})" will be logged. Defaults to False.
        args: The arguments to pass to the logger.
        kwargs: The keyword arguments to pass to the logger
    """
    return log_max_n(
        logger, obj, 1, discr_obj, discr_fn, level, show_counter, *args, **kwargs
    )


def warn_max_n(
    logger: Logger,
    obj: str,
    n: int,
    discr_obj: str = None,
    discr_fn: Callable[[Any], Any] = None,
    show_counter: bool = False,
    *args,
    **kwargs,
):
    """Log a WARNING logging obj using a logging.Logger only if it has been logged less than n times.
    If discr_obj is specified, the discrimation is based on that obj.
    If discr_fn is specified, the discrimation is based on the output of that function, applied to the obj or discr_obj if specified.

    Args:
        logger (Logger): The logger to log the obj.
        obj (str): The obj to log.
        n (int): The maximum number of times the obj can be logged.
        discr_obj (str, optional): The obj to discriminate on. Defaults to None (go back to using the obj itself).
        discr_fn (Union[Callable[[Any], Any], str], optional): The function to discriminate on. Defaults to None (go back to using the obj/discr_obj itself).
        show_counter (bool, optional): Whether to show the counter. If True, f"{obj} ({counter}/{n})" will be logged. Defaults to False.
        args: The arguments to pass to the logger.
        kwargs: The keyword arguments to pass to the logger
    """
    return log_max_n(
        logger, obj, n, discr_obj, discr_fn, WARNING, show_counter, *args, **kwargs
    )


def warn_once(
    logger: Logger,
    obj: str,
    discr_obj: str = None,
    discr_fn: Callable[[Any], Any] = None,
    show_counter: bool = False,
    *args,
    **kwargs,
):
    """Log a WARNING logging obj using a logging.Logger only if it has been logged less than n times.
    If discr_obj is specified, the discrimation is based on that obj.
    If discr_fn is specified, the discrimation is based on the output of that function, applied to the obj or discr_obj if specified.

    Args:
        logger (Logger): The logger to log the obj.
        obj (str): The obj to log.
        discr_obj (str, optional): The obj to discriminate on. Defaults to None (go back to using the obj itself).
        discr_fn (Union[Callable[[Any], Any], str], optional): The function to discriminate on. Defaults to None (go back to using the obj/discr_obj itself).
        show_counter (bool, optional): Whether to show the counter. If True, f"{obj} ({counter}/{n})" will be logged. Defaults to False.
        args: The arguments to pass to the logger.
        kwargs: The keyword arguments to pass to the logger
    """
    return log_once(
        logger, obj, discr_obj, discr_fn, WARNING, show_counter, *args, **kwargs
    )


def exec_max_n(
    func: Callable,
    n: int,
    criteria_exec: Callable[[Any], bool] = None,
    show_counter: bool = False,
):
    """Decorator to make a function only execute at most n times.
    If criteria_exec is specified, the func(x) will only be executed if criteria_exec(x) is True.

    Args:
        func (Callable): The function to decorate.
        n (int): The maximum number of times the function can be executed.
        criteria_exec (Callable[[Any], bool], optional): The criteria to execute the function. Function func(x) will only be executed if criteria_exec(x) is True. Defaults to None (no criteria).
        show_counter (bool, optional): Whether to show the counter. If True, f"{func.__name__} was called ({n-counter+1}/{n})" will be printed. Defaults to False.
    """
    assert callable(func), f"Expected a callable, got {func}"

    def wrapper(*args, **kwargs):

        if criteria_exec is not None and not criteria_exec(*args, **kwargs):
            return
        if wrapper.counter > 0:
            if show_counter:
                print(f"{func.__name__} was called ({n-wrapper.counter+1}/{n})")
            wrapper.counter -= 1
            return func(*args, **kwargs)

    wrapper.counter = n
    return wrapper


def exec_once(
    func: Callable,
    criteria_exec: Callable[[Any], bool] = None,
    show_counter: bool = False,
):
    """Decorator to make a function only execute once.
    If criteria_exec is specified, the func(x) will only be executed if criteria_exec(x) is True.
    
    Args:
        func (Callable): The function to decorate.
        criteria_exec (Callable[[Any], bool], optional): The criteria to execute the function. Function func(x) will only be executed if criteria_exec(x) is True. Defaults to None (no criteria).
        show_counter (bool, optional): Whether to show the counter. If True, f"{func.__name__} was called ({n-counter+1}/{n})" will be printed. Defaults to False.
    """
    return exec_max_n(func, 1, criteria_exec, show_counter)
