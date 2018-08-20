import socket
import time
import picamera

class CameraStream:
    def stream(self, ip, port):
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 24

        serverSocket = socket.socket()
        serverSocket.bind((ip, port))
        serverSocket.listen(0)

        connection = serverSocket.accept()[0].makefile('wb')
        try:
            camera.start_recording(connection, format='h264')
            camera.wait_recording(60)
            camera.stop_recording()
        finally:
            connection.close()
            serverSocket.close()
