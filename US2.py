import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#redespass
from ubidots import ApiClient
import math

api = ApiClient(token="972FUfeyLTXqbUKXlaLNgJ9jEHeuKl")
variable = api.get_variable("593ec67876254251716133ab")


TRIG = 23  #PIN 16
ECHO = 24  #PIN 18

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)



while GPIO.input(ECHO)==0:
  pulse_start = time.time()

while GPIO.input(ECHO)==1:
  pulse_end = time.time()

pulse_duration = pulse_end - pulse_start

distance = pulse_duration * 17150

distance = round(distance, 2)

metros = 14.5 - distance 

print "Distance:",distance,"cm"

if ( distance > 5) : print "Nivel 1!"

if ( distance > 10) : print "Nivel 2!"

if ( distance > 15) : print "Nivel 3!"


if ( distance > 20) : print "Nivel 4!"

if ( distance > 26) : print "Nivel 5!"

GPIO.cleanup()

# Write the value to your variable in Ubidots
response = variable.save_value({"value": metros})
print response
time.sleep(1)

