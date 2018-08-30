import RPi.GPIO as gpio
import time
from camera_stream import CameraStream 

class RADApp:
    started = False
    currentOp = 'stopped'
    sleepTime = 0.5

    def rightMotor(self, op):
        if op == 'forward':
            gpio.output(7, True)
            gpio.output(11, True)
            gpio.output(13, True)
            gpio.output(15, False)
        elif op == 'stop':
            gpio.output(7, False)
            gpio.output(11, False)
            gpio.output(13, False)
        elif op == 'backward':
            gpio.output(7, True)
            gpio.output(11, True)
            gpio.output(13, True)
            gpio.output(15, False)
    
    def leftMotor(self, op):
        if op == 'forward':
            gpio.output(7, True)
            gpio.output(11, True)
            gpio.output(13, True)
            gpio.output(15, False)
        elif op == 'stop':
            gpio.output(7, False)
            gpio.output(11, False)
            gpio.output(13, False)
        elif op == 'backward':
            gpio.output(7, True)
            gpio.output(11, True)
            gpio.output(13, True)
            gpio.output(15, False)

    def setup(self):
        gpio.setup(7, gpio.OUT)
        gpio.setup(11, gpio.OUT)
        gpio.setup(13, gpio.OUT)
        gpio.setup(15, gpio.OUT)

    def start(self):
        self.setup()
        self.broadcast()
        self.currentOp = 'idle'

    def stop(self):
        self.cameraStream.stop()
        self.leftMotor('stop')
        self.rightMotor('stop')
        gpio.cleanup()
        self.currentOp = 'stopped'

    def goForward(self):
        self.leftMotor('forward')
        self.rightMotor('forward')
        self.currentOp = 'forward'

    def goBackward(self):
        self.leftMotor('backward')
        self.rightMotor('backward')
        self.currentOp = 'backward'

    def goLeft(self):
        self.leftMotor('stop')
        time.sleep(self.sleepTime)
        if self.currentOp == 'forward':
            self.leftMotor('forward')
        elif self.currentOp == 'backward':
            self.leftMotor('backward')

    def goRight(self):
        self.rightMotor('stop')
        time.sleep(self.sleepTime)
        if self.currentOp == 'forward':
            self.rightMotor('forward')
        elif self.currentOp == 'backward':
            self.rightMotor('backward')

    def broadcast(self):
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
