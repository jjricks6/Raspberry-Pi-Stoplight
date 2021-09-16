import RPi.GPIO as GPIO
import os
import time
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer


host_name = '127.0.1.1'    # Change this to your Raspberry Pi IP address
host_port = 8000

mode = "Auto"
class MyServer(BaseHTTPRequestHandler):
    
    def auto(self):
        global mode
        while mode == 'Auto':
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            status='Green LED is On'

            time.sleep(5)
            if mode !='Auto':
                return
            
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)
            status='Yellow LED is On'
            
            time.sleep(2)
            if mode !='Auto':
                return
            
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.HIGH)
            status='Red LED is On'
            
            time.sleep(5)
            if mode !='Auto':
                return
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <h1>Raspberry Pi Stoplight</h1>
            <p>Turn LED:
                <a href="/Green">Green</a>
                <a href="/Yellow">Yellow</a>
                <a href="/Red">Red</a>
                <a href="/Off">Off</a>
                <a href="/Auto">Automatic</a>
            </p>
            </body>
            </html>
        '''
        self.do_HEAD()
        global mode
        if self.path=='/':
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(17, GPIO.OUT)
            GPIO.setup(27, GPIO.OUT)
            GPIO.setup(22, GPIO.OUT)
        elif self.path=='/Green':
            mode = "Man"
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            print("hello")
        elif self.path=='/Yellow':
            mode = "Man"
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)
            GPIO.output(22, GPIO.LOW)
        elif self.path=='/Red':
            mode = "Man"
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.HIGH)
        elif self.path=='/Off':
            mode = "Man"
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
        elif self.path=='/Auto':
            mode = "Auto"
            auto = Thread(target=self.auto)
            auto.start()
            print("testy")
        self.wfile.write(html.format().encode("utf-8"))
        
    
        
        
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))
    
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()