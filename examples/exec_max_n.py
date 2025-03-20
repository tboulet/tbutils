from logging import Logger
import logging
from time import sleep

from tbutils.exec_max_n import (
    print_max_n,
    print_once,
    log_max_n,
    log_once,
    warn_max_n,
    warn_once,
    exec_max_n,
    exec_once,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
if __name__ == "__main__":
    show_counter = input("Do you want to see the counter? (y/n): ").lower() == "y"
    # Test printing functions
    print(f"Testing printing functions:")
    print_once("Will be printed only once")
    print_once("Will be printed only once")
    print()
    for _ in range(5):
        print_max_n("Will be printed only 3 times", 3, show_counter=show_counter)
    print()
    
    # Test logging functions
    print(f"Testing logging functions:")
    logger = logging.getLogger(__name__)
    log_once(logger, "Will be logged only once")
    log_once(logger, "Will be logged only once")
    print()
    for _ in range(5):
        log_max_n(logger, "Will be logged only 3 times", 3, show_counter=show_counter)
    print()

    # Test one_time_exec
    print(f"Testing one_time_exec:")

    @exec_once
    def test_func():
        print("Will be printed only once")

    test_func()
    test_func()

    def test_func2():
        print("Will be printed only 3 times")

    test_func2 = exec_max_n(test_func2, 3, show_counter=show_counter)
    for _ in range(5):
        test_func2()
    print()
       
    # Test discr_obj and discr_fn
    print(f"Testing discr_obj and discr_fn:")
    for k in [5, 9, 13, 14, 15, 16, 25]:
        print_once(f"A number of a new ten was detected : {k}", discr_obj=k, discr_fn=lambda x: x // 10)
