import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#redespass
from ubidots import ApiClient
import math

api = ApiClient(token="972FUfeyLTXqbUKXlaLNgJ9jEHeuKl")
<<<<<<< HEAD
#variable = api.get_variable("59274e40762542294766e523")
variable1 = api.get_variable("593ec67876254251716133ab")
=======
variable = api.get_variable("593ec67876254251716133ab")

>>>>>>> b4da794d99f4738376ecd76dc118397ff3f02dee

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

metros = 14.89-distance

print "Hay",metros,"m3"

print "------------------------------------------------------"
print "------------------------------------------------------"
print "------------------------------------------------------"

if ( metros < 3) : print "Tanque vacio!"


#if ( metros >= 6  and metros <9 ) : print "Tanque a un cuarto!"


#if ( metros >= 9) : print "Tanque a tres cuartos!"

if ( metros >= 12) : print "Tanque lleno!"

GPIO.cleanup()

# Write the value to your variable in Ubidots
<<<<<<< HEAD
#response = variable.save_value({"value": distance})
#print response
#time.sleep(1)

response = variable1.save_value({"value": metros})
=======
response = variable.save_value({"value": metros})
>>>>>>> b4da794d99f4738376ecd76dc118397ff3f02dee
print response
time.sleep(1)
