import RPi.GPIO as gpio
import time

class RADApp:
    started = False

    def setup(self):
        gpio.setup(7, gpio.OUT)
        gpio.setup(11, gpio.OUT)
        gpio.setup(13, gpio.OUT)
        gpio.setup(15, gpio.OUT)

    def start(self):
        print('Starting hexapod...')
        self.setup()
        self.broadcast()
    
    def goForward(self):
        print('going forward...')
        gpio.output(7, True)
        gpio.output(11, True)
        gpio.output(13, True)
        gpio.output(15, False)

    def goBackward(self):
        print('going backward...')

    def goLeft(self):
        print('going left...')

    def goRight(self):
        print('going right...')

    def broadcast(self):
        print('broadcasting...')

    def handleOperation(self, operation, isContinuous):
        if operation == 'start' and not self.start:
            self.start()
        elif operation == 'forward':
            self.goForward()
        elif operation == 'backward':
            self.goBackward()
        elif operation == 'left':
            self.goLeft()
        elif operation == 'right':
            self.goRight()
        else:
            print('Err... invalid op')
