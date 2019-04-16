import time

def addition(args):
    return int(args[0]) + int(args[1])

def substraction(args):
    return int(args[0]) - int(args[1])

calls = {
    "addition" : addition,
    "substraction" : substraction
}
