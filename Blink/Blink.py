import pyfirmata
import time

board = pyfirmata.Arduino('COM4')

while True:
    print("High")
    board.digital[13].write(1)
    time.sleep(2)
    print("Low")
    board.digital[13].write(0)
    time.sleep(1)
