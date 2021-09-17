# How to create a Raspberry Pi Stoplight
### Created by Jordan Ricks

The goal of this project is to create a Raspberry Pi "stoplight" that can be controlled through a web interface. 

## Materials
* Raspberry Pi (I will be using a Pi 4b)
* 3 LED lights (Green, Yellow, and Red)
* A breadboard
* 4 wires
* 3 resistors

## Design
Our stoplight should be able to work in both Manual and Automatic modes. In Manual mode, a user is able to select any light for the stoplight to switch to including an "off" state. In Automatic mode a timer starts in the Green state and moves between Green, Yellow, and Red states automatically. The user should be able to switch between these two modes at will using the web interface.

### State Diagram
![](/images/StoplightDiagram.png)

## Creating Our Website
There are many ways to create a webserver in Python, but for the sake of this project we will be using http.python.

Create a new folder to work out and create a new python file. I named mine webserver.py, but feel free to name it anything you like.

First we need to import http.python

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
```

Define your host name and host port. Your host name is the ip address of your Pi, and the port is 8000.

```python
host_name = '127.0.1.1'    # Change this to your Raspberry Pi IP address
host_port = 8000
```

Next we need to define a custom server class using the BaseHTTPRequestHandler we imported. Inside the class we must define 2 functions for the server to work: do_HEAD and do_GET

```python
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
```
## Wiring the Pi

Ground -> Board Pin 9

Green  -> GPIO Pin 17

Yellow -> GPIO Pin 27

Red    -> GPIO Pin 22

Be sure to add a resistor before the current exits to prevent LED burnout.

![](/images/wiring.jpeg)
## Programming the Stoplight

## Sources
Build a Python Webserver with Flask - https://projects.raspberrypi.org/en/projects/python-web-server-with-flask
