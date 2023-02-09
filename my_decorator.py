from functools import wraps

# example 1
def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")
    return wrapTheFunction

@a_new_decorator
def a_function_requiring_decoration():
     print("I am the function which needs some decoration to remove my foul smell")

a_function_requiring_decoration()

# example 2
def decorator_name(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)
    return decorated
 
@decorator_name
def func():
    return "Function is running"
 
can_run = True
print(func())
 
can_run = False
print(func())

# example 3
# returns a function that is a wrapping function
def logit(logfile='out1.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)

            with open(logfile, "w") as opened_file:
                opened_file.write(log_string + '\n')
            
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator

@logit()
def myfunc1():
    pass

@logit(logfile='out2.log')
def myfunc2():
    pass

myfunc1()
myfunc2()

# calculate runtime
import time

def time_me(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        print(f'Runtime of {fn.__name__}: {time.time() - start} second')
    return wrapper

@time_me
def func():
    num = 0
    for i in range(1000):
        num += i
        for j in range(1000):
            num -= j
            for k in range(1000):
                num += k

func()
