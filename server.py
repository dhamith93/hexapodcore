from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys

from radapp import RADApp

class Server(BaseHTTPRequestHandler):
    verbose = False

    def do_POST(self):
        hwControl = RADApp()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers() 

        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        
        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postVars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postVars = {}

        if bytes('auth', 'utf8') in postVars:
            try:
                key = postVars[bytes('auth', 'utf8')][0].decode('utf-8')
                opType = postVars[bytes('type', 'utf8')][0].decode('utf-8')
                operation = postVars[bytes('op', 'utf8')][0].decode('utf-8')
            except:
                message = '{ "status":"error_decoding_params" }'
                self.wfile.write(bytes(message, 'utf8'))
                return                
        else:
            message = '{ "status":"no_auth" }'
            self.wfile.write(bytes(message, 'utf8'))
            return

        if key == 'KEY_123': # TODO secure keys
            if opType == 'test':
                message = '{ "status":"sent_to_test()" }'
            else:
                hwControl.handleOperation(operation)
                message = '{ "status":"OK" }'
        else:
            message = '{ "status":"wrong_auth" }'

        self.wfile.write(bytes(message, 'utf8'))

        if self.verbose:
            print(postVars)

    def do_GET(self):
        # self.send_response(200)
        # self.send_header('Content-type', 'application/json')
        # self.end_headers() 

        # message = 'Hello, World!'
        # self.wfile.write(bytes(message, 'utf8')) 
        self.send_response(301)
        self.send_header('Location','https://www.youtube.com/watch?v=PGNiXGX2nLU')
        self.end_headers()
        return
    
    def log_message(self, format, *args):
        if self.verbose:
            sys.stderr.write("%s - - [%s] %s\n" %
                            (self.address_string(),
                            self.log_date_time_string(),
                            format%args))
    
    def start(self, ip, port, verbose):
        self.verbose = verbose
        print('Starting server...')
        server_address = (ip, port)
        httpd = HTTPServer(server_address, Server)
        print('Server started on: ' + ip + ':' + str(port))
        httpd.serve_forever()
