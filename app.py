from flask import Flask, render_template
import RPi.GPIO as GPIO
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def setup_gpio():
    GPIO.setmode(GPIO.BOARD)

    # Green
    GPIO.setup(11, GPIO.OUT)

    # Yellow
    GPIO.setup(12, GPIO.OUT)

    # Red
    GPIO.setup(13, GPIO.OUT)


def change_lights(light):
    if light == "Green":
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
    elif light == "Yellow":
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
    elif light == "Red":
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
    elif light == "Off":
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
    return


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
