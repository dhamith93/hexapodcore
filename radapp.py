import RPi.GPIO as gpio
import time
#from camera_stream import CameraStream 

LEFT_FORWARD = 4
LEFT_BACKWARD = 17
RIGHT_FORWARD = 27
RIGHT_BACKWARD = 22

class RADApp:
    started = False
    currentOp = 'stopped'
    sleepTime = 0.5

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
        gpio.setmode(gpio.BCM)
        gpio.cleanup()
        gpio.setup(LEFT_FORWARD, gpio.OUT)
        gpio.setup(LEFT_BACKWARD, gpio.OUT)
        gpio.setup(RIGHT_FORWARD, gpio.OUT)
        gpio.setup(RIGHT_BACKWARD, gpio.OUT)

    def start(self):
        self.setup()
        #self.broadcast()
        self.currentOp = 'idle'

    def stop(self):
        #self.cameraStream.stop()
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

    # def broadcast(self):
        # self.cameraStream = CameraStream()
        # self.cameraStream.stream('127.0.0.1', 5000)

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
