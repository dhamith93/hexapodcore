import RPi.GPIO as gpio
import time
import subprocess

LEFT_FORWARD = 18
LEFT_BACKWARD = 17
RIGHT_FORWARD = 23
RIGHT_BACKWARD = 22

WHITE_LED_1 = 5
WHITE_LED_2 = 6
RED_LED = 13

class RADApp:
    started = False
    currentOp = 'stopped'
    sleepTime = 1.5

    def setup(self):
        gpio.cleanup()
        gpio.setmode(gpio.BCM)
        gpio.setup(LEFT_FORWARD, gpio.OUT)
        gpio.setup(LEFT_BACKWARD, gpio.OUT)
        gpio.setup(RIGHT_FORWARD, gpio.OUT)
        gpio.setup(RIGHT_BACKWARD, gpio.OUT)
        gpio.setup(WHITE_LED_1, gpio.OUT)
        gpio.setup(WHITE_LED_2, gpio.OUT)
        gpio.setup(RED_LED, gpio.OUT)
        self.halt()

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

    def led(self, led, operation):
        if led == 'white':
            if operation == 'on':
                gpio.output(WHITE_LED_1, True)
                gpio.output(WHITE_LED_2, True)
            else:
                gpio.output(WHITE_LED_1, False)
                gpio.output(WHITE_LED_2, False)
        
        if led == 'red':
            if operation == 'on':
                gpio.output(RED_LED, True)
            else:
                gpio.output(RED_LED, False)

    def start(self):
        self.started = True
        self.setup()
        subprocess.call('/home/pi/git/hexapodcore/start_stream.sh')
        self.led('white', 'on')
        self.currentOp = 'idle'

    def stop(self):
        self.started = False
        subprocess.call('/home/pi/git/hexapodcore/stop_stream.sh')
        self.leftMotor('stop')
        self.rightMotor('stop')
        self.led('white', 'off')
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
        elif operation == 'emergency_on':
            self.led('red', 'on')
        elif operation == 'emergency_off':
            self.led('red', 'off')
        else:
            print('Err... invalid op')
