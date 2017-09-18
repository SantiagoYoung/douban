import threading
import time


def task():
    while 1:
        time.sleep(1)
        print(1)


t1 = threading.Thread(target=task())
t1.start()
t1.join(5)
print(11111)
