from flask import Flask
import time

app = Flask(__name__)

# decorator function is a function that wraps another function and extends its behavior
def delay_decorator(func):
    def wrapper():
        time.sleep(2)
        # Do something before
        func()
        func()
        print(func.__name__)
        # Do something after
    return wrapper

@delay_decorator
def say_hello():
    print("Hello")
    
def say_goodbye():
    print("Goodbye")

@delay_decorator
def say_greeting():
    print("How are you?")
    
decorated_say_goodbye = delay_decorator(say_goodbye)
decorated_say_goodbye()