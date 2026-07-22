import logging

# one time setup
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))


def logger_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        pos_parameters = list(args) if args else "none"
        kw_parameters = kwargs if kwargs else "none"

        log_message = (
            f"function: {func.__name__}\n"
            f"positional parameters: {pos_parameters}\n"
            f"keyword parameters: {kw_parameters}\n"
            f"return: {result}\n"
        )
        logger.log(logging.INFO, log_message)

        return result
    return wrapper

@logger_decorator
def say_hello():
    print("Hello, World!")

@logger_decorator
def positional_function(*args):
    return True

@logger_decorator
def keyword_function(**kwargs):
    return logger_decorator

if __name__ == "__main__":
    say_hello()
    positional_function(1, 2, 3)
    keyword_function(a=1, b=2)