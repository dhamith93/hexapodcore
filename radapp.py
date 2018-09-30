import RPi.GPIO as gpio
import time
import subprocess

LEFT_FORWARD = 18
LEFT_BACKWARD = 17
RIGHT_FORWARD = 23
RIGHT_BACKWARD = 22

class RADApp:
    started = False
    currentOp = 'stopped'
    sleepTime = 1.5

    def rightMotor(self, op):
        if op == 'forward':
            gpio.output(RIGHT_FORWARD, True)
            gpio.output(RIGHT_BACKWARD, False)
        elif op == 'stop':
            gpio.output(RIGHT_FORWARD, False)
            gpio.output(RIGHT_BACKWARD, False)
        elif op == 'backward':
            gpio.output(RIGHT_FORWARD, False)
            gpio.output(RIGHT_BACKWARD, True)
    
    def leftMotor(self, op):
        if op == 'forward':
            gpio.output(LEFT_FORWARD, True)
            gpio.output(LEFT_BACKWARD, False)
        elif op == 'stop':
            gpio.output(LEFT_FORWARD, False)
            gpio.output(LEFT_BACKWARD, False)
        elif op == 'backward':
            gpio.output(LEFT_FORWARD, False)
            gpio.output(LEFT_BACKWARD, True)

    def setup(self):
        gpio.cleanup()
        gpio.setmode(gpio.BCM)
        gpio.setup(LEFT_FORWARD, gpio.OUT)
        gpio.setup(LEFT_BACKWARD, gpio.OUT)
        gpio.setup(RIGHT_FORWARD, gpio.OUT)
        gpio.setup(RIGHT_BACKWARD, gpio.OUT)
        self.leftMotor('stop')
        self.rightMotor('stop')

    def start(self):
        self.started = True
        self.setup()
        subprocess.call('/home/pi/git/hexapodcore/start_stream.sh')
        self.currentOp = 'idle'

    def stop(self):
        self.started = False
        subprocess.call('/home/pi/git/hexapodcore/stop_stream.sh')
        self.leftMotor('stop')
        self.rightMotor('stop')
        gpio.cleanup()
        self.currentOp = 'stopped'

    def halt(self):
        self.leftMotor('stop')
        self.rightMotor('stop')
        self.currentOp = 'halted'

    def goForward(self):
        self.leftMotor('forward')
        self.rightMotor('forward')
        self.currentOp = 'forward'

    def goBackward(self):
        self.leftMotor('backward')
        self.rightMotor('backward')
        self.currentOp = 'backward'

    def goLeft(self):
        if self.currentOp == 'forward' or self.currentOp == 'halted':
            self.leftMotor('backward')
            self.rightMotor('forward')
        elif self.currentOp == 'backward':
            self.leftMotor('forward')
            self.rightMotor('backward')

    def goRight(self):
        if self.currentOp == 'forward' or self.currentOp == 'halted':
            self.rightMotor('backward')
            self.leftMotor('forward')
        elif self.currentOp == 'backward':
            self.rightMotor('forward')
            self.leftMotor('backward')

    def handleOperation(self, operation):
        if operation == 'start':
            self.start()
        elif operation == 'stop':
            self.stop()
        elif operation == 'forward':
            self.goForward()
        elif operation == 'backward':
            self.goBackward()
        elif operation == 'left':
            self.goLeft()
        elif operation == 'right':
            self.goRight()
        elif operation == 'halt':
            self.halt()
        else:
            print('Err... invalid op')
