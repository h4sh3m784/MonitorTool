import time
import random

def addition(args):
    time.sleep(1)
    return int(args[0]) + int(args[1])

calls = {
    "addition" : addition
}
