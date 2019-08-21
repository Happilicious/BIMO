import serial

#ser = serial.Serial('/dev/ttyUSB0')
ser = serial.Serial('/dev/ttyACM0')
ser.flushInput()

quit=0
while not quit:
	if(ser.in_waiting != 0):
		ser_input=ser.readline()
		quit=1

ser_decoded = ser_input.decode('utf-8')
ser_token = ser_decoded.split()

ser_num = []
i=0
while i<len(ser_token):
	ser_num.append(float(ser_token[i]))
	i+=1

j=0
while j<i:
	print(ser_num[j])
	j+=1

ser.close()
