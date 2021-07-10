import pyfirmata
import time

board = pyfirmata.Arduino('COM4')

while True:
    print(1)
    board.digital[13].write(1)
    time.sleep(2)
    print(0)
    board.digital[13].write(0)
    time.sleep(1)
