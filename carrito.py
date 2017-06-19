###########################################################################
#Proyecto de Redes de Computadoras					             Profesor: Ing. Rogelio Gonzales Quiros#					
###########################################################################
#Realizado por: 			Jose Rosales C.             	 Francisco Elizondo R.	         Daniel Quesada V.#
###########################################################################
#Estudiantes de la carrera de Ing. Electronica del TEC, sede San Carlos                                                             #
###########################################################################


import binascii
import socket
import time
import signal
import sys
import serial
import RPi.GPIO as GPIO
import Adafruit_PN532 as PN532	#libreria lector NFC
from subprocess import call
from ftplib import FTP				#libreria FTP
import dht11						#libreria Sensor humedad y temperatura
import SI1145.SI1145 as SI1145	#Sensor UV 
from ubidots import ApiClient		#Ubidots...
import math
import os


####################PINES_RASPBERRY###########################
GPIO.setmode(GPIO.BCM)
# PN532 configuration for a Raspberry Pi GPIO:
GPIO.setwarnings(False)  #desacttiva Warnings
GPIO.cleanup()
CS   = 18               			 #GPIO 18, pin 12
MOSI = 23               		 #GPIO 23, pin 16
MISO = 24                		 #GPIO 24, pin 18
SCLK = 25                		 #GPIO 25, pin 22
GPIO.setup(16, GPIO.OUT)   #verde pin 36
GPIO.setup(12, GPIO.OUT)   #azul  pin 32
GPIO.setup(26, GPIO.OUT)   #rojo
#################Sensor de humedad y temp#########################
instance = dht11.DHT11(pin=14)
result = instance.read()
#################Sensor UV#####################################
sensor = SI1145.SI1145()

####################VARIABLES_GLOBALES#########################
#VARIABLES PARA LAS ESTACIONES:
v = "verde"
r = "rojo"
a = "amarillo"


###############FUNCION_PARA_LEER_TAGS##########################
def func_nfc():
	global data, DELAY, leds
	perro=True
	while (perro):
		if(leds==0): 
			
			GPIO.output(16, GPIO.HIGH)
			GPIO.output(26, GPIO.HIGH)
			GPIO.output(12, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(16, GPIO.LOW)
			GPIO.output(26, GPIO.LOW)
			GPIO.output(12, GPIO.LOW)
		#time.sleep(0.5)
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
		#print('')
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
	leds=0
	func_nfc()	#leer tag
    
##verde#################PRUEBA_01###########################################
	if(data[1:6] == v): 
		print(data[1:6])
		leds=1
		GPIO.output(26, GPIO.LOW)
		GPIO.output(12, GPIO.LOW)
		GPIO.output(16, GPIO.HIGH)
		leer_ip=True
		while (leer_ip):
			print("leyendo_ip")
			print(data[2:16])
			func_nfc()
			#if (data[1:15]==ip): 
			print("adksda")
			#domain name or server ip:69
			#datosnfc=data[1:15]
			#pancho=datosnfc.split()
			
			try:
				os.system("python hora.py >> hora.txt")
				ftp = FTP(str(data[2:16]))
				ftp.login(user='redesie1', passwd = 'redesie2017')
				#Subir archivo
				filename = 'hora.txt'
				ftp.storbinary('STOR '+filename, open(filename, 'rb'))
				#ftp.quit()
				#Bajar Archivo
				filename = 'archivo.txt'
				localfile = open(filename, 'wb')
				ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
				print("archivo correctamente descargado")
				ftp.quit()
				localfile.close()
				os.remove("hora.txt")
				leer_ip=False										#para salirse del while
			except socket.error,e: 
					print ' No se pudo conectar!, %s'%e
					os.remove("hora.txt")
		

##amarillo##################PRUEBA_02###########################################

	elif(data[1:9] == a):
		try:
			print(data[1:9])
			GPIO.output(26, GPIO.LOW)
			GPIO.output(16, GPIO.LOW)
			GPIO.output(12, GPIO.HIGH)
			global Temperatura, Humedad
			###########TEMP_HUM#############
			if result.is_valid():
				Temperatura=result.temperature
				Humedad=result.humidity
				print("Temperatura: %d C" % Temperatura)			
				print("Humedad: %d %%" % Humedad)
			else:
				print("Error: %d" % result.error_code)

			#############UV:################
			vis = sensor.readVisible()
	       		IR = sensor.readIR()
	       		UV = sensor.readUV()
	       		uvIndex = UV / 100.0
			#print ('Vis:             ' + str(vis))
	      	  	#print ('IR:              ' + str(IR))
			#print ('UV Index:        ' + str(uvIndex))

			#################UBIDOTS#############################################
			api = ApiClient(token="972FUfeyLTXqbUKXlaLNgJ9jEHeuKl")	#Api Client
			#variables:
			var_temp = api.get_variable("59420f727625421a07edcc58")
			var_hum = api.get_variable("59420f847625421a133a5303")
			var_uv = api.get_variable("59421dad7625421a0f8d7381")
			var_ir = api.get_variable("59421d9e7625421a0f8d7276")
			var_vis = api.get_variable("59421d937625421a04983b40")

			# Escribe el valor a las variables de UBIDOTS:
	 		resp_temp = var_temp.save_value({"value": Temperatura})
	  		print resp_temp
			resp_hum = var_hum.save_value({"value": Humedad})
	  		print resp_hum
			resp_uv = var_uv.save_value({"value": str(uvIndex)})
	  		print resp_uv
			resp_ir = var_ir.save_value({"value": str(IR)})
	  		print resp_ir
			resp_vis = var_vis.save_value({"value": str(vis)})
	  		print resp_vis

		except socket.error,e: 
					print ' Algun error, %s'%e
			


##amarillo##################PRUEBA_03###########################################
	
	elif(data[1:5] == r):
		print(data[1:5])
		GPIO.output(12, GPIO.LOW)
		GPIO.output(16, GPIO.LOW)
		GPIO.output(26, GPIO.HIGH)
		
		pancho=True
		while (pancho):
			try:
				###########TEMP_HUM#############
				if result.is_valid():
					Temperatura=result.temperature
					Humedad=result.humidity
					print("Temperatura: %d C" % Temperatura)			
					print("Humedad: %d %%" % Humedad)
				else:
					print("Error: %d" % result.error_code)

			

				###################XBEE######################################
				ser = serial.Serial(
					      
					port='/dev/ttyUSB0',
					baudrate = 9600,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS,
					timeout=1
					   )
				counter=0

				########LEER/ESCRIBIR_SERIAL#########
				x=ser.readline()
				print (x)
				y=ser.write(str(Temperatura))
				y=ser.write('/')
				y=ser.write(str(Humedad))
				y=ser.write(';')
				if (x=='OK'):
					pancho=False
				else:
					pancho=True
			
			except socket.error,e: 	
				print ("C mamo")
		

##################ELSE_POR_ALGUN_ERROR######################################
	else:
		print("NADA...")
		print(data[1:9])
		time.sleep(DELAY)






        
    



