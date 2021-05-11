
import threading
from Adafruit import livemqtt as lm
import app

# creating thread
t1 = threading.Thread(target=lm.threadone)
t2 = threading.Thread(target=app.call)

# import math as m
# t2 = threading.Thread(target=m.pi)

# starting thread 1
t1.start()
# starting thread 2
t2.start()

# wait until thread 1 is completely executed
t1.join()
# wait until thread 2 is completely executed
t2.join()

# both threads completely executed
print("Done!")
