import RPi.GPIO as GPIO
import time
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer


host_name = '127.0.1.1'    # Change this to your Raspberry Pi IP address
host_port = 8000

# Mode is a global variable which will help us switch between automatic and manual modes
mode = "Auto"


# Custom Server class built using the base http handler
class MyServer(BaseHTTPRequestHandler):

    # The automatic stoplight function is started in a thread
    # Exits only when the mode has changed
    def auto(self):
        global mode
        while mode == 'Auto':
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)

            time.sleep(5)
            if mode != 'Auto':
                return

            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)

            time.sleep(2)
            if mode != 'Auto':
                return

            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.HIGH)

            time.sleep(5)
            if mode != 'Auto':
                return

    # Defines the headers
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Defines what happens when the page loads
    def do_GET(self):
        # Simple html page with hyperlinks as buttons
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

        # Set mode to be global
        global mode

        # Setup the GPIO pins on the index page
        if self.path == '/':
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(17, GPIO.OUT)
            GPIO.setup(27, GPIO.OUT)
            GPIO.setup(22, GPIO.OUT)
        elif self.path == '/Green':
            mode = "Man"
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            print("hello")
        elif self.path == '/Yellow':
            mode = "Man"
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.HIGH)
            GPIO.output(22, GPIO.LOW)
        elif self.path == '/Red':
            mode = "Man"
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.HIGH)
        elif self.path == '/Off':
            mode = "Man"
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
        elif self.path == '/Auto':
            mode = "Auto"

            # Creates a thread so that you can exit the auto state
            auto = Thread(target=self.auto)
            auto.start()

        # After the GPIO action, rewrite the page
        self.wfile.write(html.format().encode("utf-8"))


# Run the server when the script starts
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
