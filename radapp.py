import RPi.GPIO as gpio
import time
from camera_stream import CameraStream 


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

    def stop(self):
        self.cameraStream.stop()

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
        self.cameraStream = CameraStream()
        self.cameraStream.stream('127.0.0.1', 5000)

    def handleOperation(self, operation):
        if operation == 'start' and not self.started:
            self.start()
        elif operation == 'stop' and self.started:
            self.stop()
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
