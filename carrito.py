# Requires Adafruit_Python_PN532

import binascii
import socket
import time
import signal
import sys
import RPi.GPIO as GPIO
import Adafruit_PN532 as PN532
from subprocess import call


####################PINES_RASPBERRY###########################
GPIO.setmode(GPIO.BCM)
# PN532 configuration for a Raspberry Pi GPIO:
GPIO.setwarnings(False)  #desacttiva Warnings
CS   = 18               			 #GPIO 18, pin 12
MOSI = 23               		 #GPIO 23, pin 16
MISO = 24                		 #GPIO 24, pin 18
SCLK = 25                		 #GPIO 25, pin 22
GPIO.setup(16, GPIO.OUT)   #verde pin 36
GPIO.setup(12, GPIO.OUT)   #azul  pin 32
GPIO.setup(26, GPIO.OUT)   #rojo
###############################################################




####################VARIABLES_GLOBALES#########################

#VARIABLES PARA LAS ESTACIONES:
v = "verde"
r = "rojo"
a = "azul"
ip= "54.237.192.107"





###############FUNCION_PARA_LEER_TAGS###########################
def func_nfc():
	global data, DELAY
	perro=True
	while (perro):
	    	# Configure the key to use for writing to the MiFare card.  You probably don't
		# need to change this from the default below unless you know your card has a
		# different key associated with it.
		CARD_KEY = [0xD3, 0xF7, 0xD3, 0xF7, 0xD3, 0xF7]
		# Number of seconds to delay after reading data.
		DELAY = 0.5
		# Prefix, aka header from the card
		HEADER = b'BG'
		def close(signal, frame):
			sys.exit(0)
		signal.signal(signal.SIGINT, close)
		# Create and initialize an instance of the PN532 class
		pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
		pn532.begin()
		pn532.SAM_configuration()
		# Wait for a card to be available
		uid = pn532.read_passive_target()
		# Try again if no card found
		if uid is None:
			continue
		# Found a card, now try to read block 4 to detect the block type
		print('')
		print('Card UID 0x{0}'.format(binascii.hexlify(uid)))
		#Authenticate and read block 4
		#if not pn532.mifare_classic_authenticate_block(uid, 1, PN532.MIFARE_CMD_AUTH_A,
				                #CARD_KEY):
		#print('Failed to authenticate with card!')
		#continue
		data = pn532.mifare_classic_read_block(6)
		if data is None:
			print('Failed to read data from card!')
			continue
		perro=False
##########################################################################



while True:
    
	func_nfc()
    
##verde#################PRUEBA_01###########################################
	if(data[1:6] == v): 
		print(data[1:6])
		GPIO.output(16, GPIO.HIGH)
		leer_ip=True
		while (leer_ip):
			print("leyendo_ip")
			print(data[1:15])
			func_nfc()
			if (data[1:15]==ip): 
				print("adksda")
	
		
            







##rojo##################PRUEBA_02###########################################
	elif(data[1:5] == r):
		print(data[1:5])
		GPIO.output(26, GPIO.HIGH)
		








##azul##################PRUEBA_02###########################################
	elif(data[1:5] == a):
		print(data[1:5])
		GPIO.output(12, GPIO.HIGH)
		







##################ELSE_POR_ALGUN_ERROR######################################
	else:
		print("NADADADA")
		time.sleep(DELAY)






        
    



