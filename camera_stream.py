import socket
import time
import picamera

class CameraStream:
    def stream(self, ip, port):
        self.camera = picamera.PiCamera()
        # self.camera.resolution = (640, 480)
        self.camera.resolution = (200, 200) # use lower resolution to reduce the stream delay
        self.camera.framerate = 24

        self.serverSocket = socket.socket()
        self.serverSocket.bind((ip, port))
        self.serverSocket.listen(0)

        self.connection = self.serverSocket.accept()[0].makefile('wb')
        try:
            self.camera.start_recording(self.connection, format='h264')
        except:
            pass

    def stop(self):
        try:
            self.camera.stop_recording()
            self.connection.close()
            self.serverSocket.close()
        except:
            pass
