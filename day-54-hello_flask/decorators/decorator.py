import functools
import time

## Python decorator function
## wraps a function within another function
## allows things to run before the function is called

def delay_decorator(function):
    def wrapper_function():
        # do something before
        time.sleep(2)
        function()

        # do something after
    return wrapper_function

def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_function():
            time.sleep(2)
            for _ in range(num_times):
                func()

        return wrapper_function

    return decorator_repeat

@delay_decorator
def say_hello():
    print("Hello")

@delay_decorator
def say_goodbye():
    print("Goodbye")

@repeat(2)
def say_greeting():
    print("Greetings")

say_hello()
say_goodbye()
say_greeting()

# decorated_function = delay_decorator(say_greeting)
# decorated_function()