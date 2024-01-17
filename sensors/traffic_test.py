import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set the pin 21 as output
GPIO.setup(21, GPIO.OUT)

# Set the pin 21 to high
GPIO.output(21, GPIO.HIGH)

# Wait for a while
time.sleep(5)  # You can adjust the sleep time as needed
GPIO.cleanup()
