import threading

e = threading.Event()
d = {"event" : e}


t = test()

print(type(t))

if isinstance(t, threading._Event):
    print("kek")
else:
    print("np")
