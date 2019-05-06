import threading

def test():
    e = threading.Event()
    return  e

t = test()

print(type(t))

if isinstance(t, threading._Event):
    print("kek")
else:
    print("np")
