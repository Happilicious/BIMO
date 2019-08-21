#gui
import PySimpleGUI as sg
#opencv
import cv2 as cv
import math
import time
import argparse
#serial
import serial
#time
import time

#All of this is a pile of vomit, bad practice,
#and hard coding due to time constraints

#Prerequisites:
#Python3, OpenCV, PySimpleGUI, TkInter, PySerial

#global variable please have mercy
data = []	#stores all data
name = []	#stores name

#---------------------------------------
#get input from file
with open('data/data.txt', 'r') as file:
	data = file.readlines()
	file.close()

#---------------------------------------
#opencv prerequisite and functions
def getFaceBox(net, frame, conf_threshold=0.7):
	selected_bbox=[]
	frameOpencvDnn = frame.copy()
	frameHeight = frameOpencvDnn.shape[0]
	frameWidth = frameOpencvDnn.shape[1]
	blob = cv.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

	net.setInput(blob)
	detections = net.forward()
	bboxes = []
	middle=[]
	for i in range(detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		if confidence > conf_threshold:
			x1 = int(detections[0, 0, i, 3] * frameWidth)
			y1 = int(detections[0, 0, i, 4] * frameHeight)
			x2 = int(detections[0, 0, i, 5] * frameWidth)
			y2 = int(detections[0, 0, i, 6] * frameHeight)
			bboxes.append([x1, y1, x2, y2])
			middle.append((x1+x2)/2)
			cv.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
	if bboxes:
		#print(bboxes)
		#print(middle)
		height, width = frame.shape[:2]
		#print(middle.index(min(middle, key=lambda x:abs(x-(width/2)))))
		selected_bbox = bboxes[middle.index(min(middle, key=lambda x:abs(x-(width/2))))]
		cv.rectangle(frameOpencvDnn, (selected_bbox[0], selected_bbox[1]), (selected_bbox[2], selected_bbox[3]), (255, 0, 0), int(round(frameHeight/150)), 8)
	return frameOpencvDnn, bboxes, selected_bbox

parser = argparse.ArgumentParser(description='Use this script to run age and gender recognition using OpenCV.')
parser.add_argument('--input', help='Path to input image or video file. Skip this argument to capture frames from a camera.')

args = parser.parse_args()

faceProto = "opencv/opencv_face_detector.pbtxt"
faceModel = "opencv/opencv_face_detector_uint8.pb"

ageProto = "opencv/deploy_age.prototxt"
ageModel = "opencv/age_net.caffemodel"

genderProto = "opencv/deploy_gender.prototxt"
genderModel = "opencv/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# Load network
ageNet = cv.dnn.readNet(ageModel, ageProto)
genderNet = cv.dnn.readNet(genderModel, genderProto)
faceNet = cv.dnn.readNet(faceModel, faceProto)

def datacollect(index):
	# Open a video file or an image file or a camera stream
	cap = cv.VideoCapture(args.input if args.input else 0)
	#cap = cv.VideoCapture('data/video.mp4')
	#cap = cv.VideoCapture('http://192.168.43.242:8080/?action=stream')
	padding = 20
	o_padding = 20	#output padding
	ser_token=[]
	flag=-1
	ser_num = []
	ser.flushInput()
	while True:
		if cv.waitKey(1) >= 0:
			break
		# Read frame
		t = time.time()
		hasFrame, frame = cap.read()
		if not hasFrame:
			print('no frame')
			cv.waitKey()
			break
		
		frameFace, bboxes, selected_bbox = getFaceBox(faceNet, frame)
		if not bboxes:
		    #print("No face Detected, Checking next frame")
		    continue

		for bbox in bboxes:
			# print(bbox)
			face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]
			'''
			blob = cv.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
			genderNet.setInput(blob)
			genderPreds = genderNet.forward()
			gender = genderList[genderPreds[0].argmax()]
			# print("Gender Output : {}".format(genderPreds))
			#print("Gender : {}, conf = {:.3f}".format(gender, genderPreds[0].max()))

			ageNet.setInput(blob)
			agePreds = ageNet.forward()
			age = ageList[agePreds[0].argmax()]
			#print("Age Output : {}".format(agePreds))
			#print("Age : {}, conf = {:.3f}".format(age, agePreds[0].max()))

			label = "{},{}".format(gender, age)
			cv.putText(frameFace, label, (bbox[0], bbox[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv.LINE_AA)
			'''
			cv.imshow("BIMO: Taking Pictures", frameFace)
			# cv.imwrite("age-gender-out-{}".format(args.input),frameFace)
		#print("time : {:.3f}".format(time.time() - t))
		
		#wait for serial, then capture image
		if(ser.in_waiting != 0):
			ser_input=ser.readline()
			ser_decoded = ser_input.decode('utf-8')
			ser_token = ser_decoded.split()
			
			crop_height_scale_to_width=(((selected_bbox[3]+o_padding)-(selected_bbox[1]-o_padding))/9*7)/2
			crop_width_middle=(selected_bbox[0]+selected_bbox[2])/2
			crop_image = frame[  selected_bbox[1]-o_padding:selected_bbox[3]+o_padding, 
								int(crop_width_middle-crop_height_scale_to_width):int(crop_width_middle+crop_height_scale_to_width)]#x
			scaled_image = cv.resize(crop_image, (175, 225))
			cv.imwrite('data/'+str(index)+'.png', scaled_image)
			flag=1
			break
	cap.release()
	cv.destroyAllWindows()
	return flag, ser_token

#---------------------------------------
#functions and layouts

#update after back from window2, or delete from window1
def updatename():
	name.clear()
	for line in data:
		name.append(line.split(None, 1)[0])
	return

#pass flags and selected user data if condition met
def openwindow1():
	updatename()
	
	window1 = sg.Window('BIMO', layout1)
	flag=-1
	index=-1
	while True:
		event1, values1 = window1.Read()
		if event1 is None:
			flag=0
			break
		if event1 == 'New':
			flag=1
			break
		if event1 == 'View':
			try:
				index=name.index(next(iter(values1.values()))[0])
			except:
				print('Please select user')
			else:
				flag=2
				break
		if event1 == 'Delete':
			try:
				print('deleting', next(iter(values1.values()))[0])
			except:
				print('Please select user')
			else:
				del data[name.index(next(iter(values1.values()))[0])]
				updatename()
				window1.Element('LISTBOX1').Update(values=name)
	window1.Close()
	return flag, index

def openwindow2():
	window2 = sg.Window('BIMO: New user', layout2)
	flag=-1
	new_data=[]
	while True:
		event2, values2 = window2.Read()
		if event2 is None:
			flag=0
			break
		if event2 == 'Back':
			flag=1
			break
		if event2 == 'Next':
			try:
				list(values2.keys())[list(values2.values()).index('')]
			except:
				new_data=list(values2.values())
				flag=2
				if ' ' in new_data[0] or ' ' in new_data[1]:
					print('Please make sure no space in name section')
				else:
					break
			else:
				print('Please all fill all field')
	window2.Close()
	return flag, new_data
	
def openwindow3(index):
	window3 = sg.Window('BIMO: View', layout3)
	window3.Read(timeout=10)#force update image
	window3.Element('IMAGE').Update(filename='data/'+str(index)+'.png')
	data_token = (data[index]).split()
	window3.Element('FIRSTNAME').Update(data_token[0])
	window3.Element('LASTNAME').Update(data_token[1])
	window3.Element('AGE'	).Update(data_token[2])
	window3.Element('GENDER').Update(data_token[3])
	window3.Element('HEIGHT').Update(data_token[4])
	window3.Element('WEIGHT').Update(data_token[5])
	window3.Element('LBM'	).Update(data_token[6])
	window3.Element('LBM_P'	).Update(data_token[7])
	window3.Element('DLM'	).Update(data_token[8])
	window3.Element('TBW'	).Update(data_token[9])
	window3.Element('EWATER').Update(data_token[10])
	window3.Element('IWATER').Update(data_token[11])
	window3.Element('SMM'	).Update(data_token[12])
	window3.Element('BFM'	).Update(data_token[13])
	window3.Element('BMI'	).Update(data_token[14])
	window3.Element('BFM_P'	).Update(data_token[15])
	window3.Element('ECW_TBW').Update(data_token[16])
	window3.Element('BMR'	).Update(data_token[17])
	window3.Element('R_BMR'	).Update(data_token[18])
	window3.Element('TIME').Update(data_token[19])
	window3.Element('DATE').Update(data_token[20])
	new_data=[]
	while True:
		event3, values3 = window3.Read()
		if event3 is None:
			flag=0
			break
		try:
			list(values3.keys())[list(values3.values()).index('')]
		except:
			new_data=list(values3.values())
			all_new_data=' '.join(new_data)
			print(all_new_data+'\n')
			if ' ' in new_data[0] or ' ' in new_data[1]:
				print('Please make sure no space in name section')
			else:
				if event3 == 'Back':
					flag=1
					data[index]=all_new_data+'\n'
					break
				if event3 == 'Test Again':
					data[index]=all_new_data+'\n'
					flag=2
					break
		else:
			print('Please all fill all field')
	window3.Close()
	return flag
	

#layouts
text_size=(25,1)
input_size=(20,1)
text_size2=(11,1)
input_size2=(11,1)
desription_size=(60,1)
myfont = 'Calibri 12'

layout1=[
		[sg.Text('Hello user! What can I help you?',font = 'Calibri 20')], #Read old file or create new file
		[sg.Listbox(values=name, key='LISTBOX1', size=(50,7))],
		[sg.Button('New'), sg.Button('View'), sg.Button('Delete')]
	 	]

layout2=[
		[sg.Text('First Name',	size=text_size),	sg.Input('', size=input_size)],
		[sg.Text('Last Name',	size=text_size),	sg.Input('', size=input_size)],
		[sg.Text('Age', 	size=text_size), 	sg.Input('', size=input_size)],
		[sg.Text('Gender',	size=text_size),	sg.Input('', size=input_size)],
		[sg.Text('Height',	size=text_size),	sg.Input('', size=input_size)],
		[sg.Text('Weight',	size=text_size),	sg.Input('', size=input_size)],
		[sg.Button('Back'), sg.Button('Next')]
	 	]

column1=[
		[sg.Image(filename='data/blank.png', key='IMAGE')],
		[sg.Text('First Name',size=text_size2, font = myfont),	sg.Input('', key='FIRSTNAME',size=input_size2, font = myfont)],
		[sg.Text('Last Name',size=text_size2, font = myfont),	sg.Input('', key='LASTNAME',size=input_size2, font = myfont)],
		[sg.Text('Age', 	size=text_size2, font = myfont), 	sg.Input('', key='AGE',		size=input_size2, font = myfont)],
		[sg.Text('Gender',	size=text_size2, font = myfont),	sg.Input('', key='GENDER',	size=input_size2, font = myfont)],
		[sg.Text('Height',	size=text_size2, font = myfont),	sg.Input('', key='HEIGHT',	size=input_size2, font = myfont)],
		[sg.Text('Weight',	size=text_size2, font = myfont),	sg.Input('', key='WEIGHT',	size=input_size2, font = myfont)],
	 	]

#if (data_token[15] >= 18.5 and data_token[15] < 25):
#EF5350 - RED
#90EE98 - GREEN
#FFED83 - YELLOW
column2=[
	[sg.Text('Lean Body Mass (kg)',				size=text_size, font = myfont),	sg.Input('', key='LBM',		size=input_size, font = myfont), sg.Text('<< Body weight without fat>>', size=desription_size)],
	[sg.Text('Lean Body Mass (%)',				size=text_size, font = myfont),	sg.Input('', key='LBM_P',	size=input_size, font = myfont), sg.Text('Mean = 81.9% << Weight of protein (muscle) and fat in the body >>', size=desription_size)],
	[sg.Text('Dry Lean Mass (kg)',				size=text_size, font = myfont),	sg.Input('', key='DLM',		size=input_size, font = myfont), sg.Text('<< Weight of protein (muscle) and fat in the body>>', size=desription_size)],
	[sg.Text('Total Body Water (kg)',			size=text_size, font = myfont),	sg.Input('', key='TBW',		size=input_size, font = myfont), sg.Text('<< Total amount of body water >>', size=desription_size)],
	[sg.Text('Extracellular Water (kg)',		size=text_size, font = myfont),	sg.Input('', key='EWATER',	size=input_size, font = myfont), sg.Text('<< Amount of body water held within the body\'s cell >>', size=desription_size)],
	[sg.Text('Intracellular Water (kg)',		size=text_size, font = myfont),	sg.Input('', key='IWATER',	size=input_size, font = myfont), sg.Text('<< Amount of body water held outside the body\'s cell >>', size=desription_size)],
	[sg.Text('Skeletal Muscle Percent (%)',		size=text_size, font = myfont),	sg.Input('', key='SMM',		size=input_size, font = myfont, background_color = '#FFED83'), sg.Text('Mean = 39.77% (data collected from Curtin)', size=desription_size)],
	[sg.Text('Body Fat Mass (kg)',				size=text_size, font = myfont),	sg.Input('', key='BFM',		size=input_size, font = myfont), sg.Text('Mean = 13.94 kg (data collected from Curtin)', size=desription_size)],
	
	[sg.Text('Body Fat Mass (%)',				size=text_size, font = myfont),	sg.Input('', key='BFM_P',	size=input_size, font = myfont, background_color = '#EF5350'), sg.Text('Mean = 20.23%', size=desription_size)],
	[sg.Text('BMI',								size=text_size, font = myfont),	sg.Input('', key='BMI',		size=input_size, font = myfont, background_color = '#EF5350'), sg.Text('Mean = 23.17 << 18.5 or more and less than 25 is consider normal >>', size=desription_size)],
	[sg.Text('ECW/TBW Ratio',					size=text_size, font = myfont),	sg.Input('', key='ECW_TBW',	size=input_size, font = myfont, background_color = '#FFED83'), sg.Text('Best value at 0.36 - 0.39', size=desription_size)],
	[sg.Text('BMR',								size=text_size, font = myfont),	sg.Input('', key='BMR',		size=input_size, font = myfont), sg.Text('Basal metabolic rate (BMR) is the minimum \namount of calorie needed per day', size=(70,2))],
	[sg.Text('Recommended BMR ',				size=text_size, font = myfont),	sg.Input('', key='R_BMR',	size=input_size, font = myfont), sg.Text('It is recommended for you to intake this amount of calorie per day', size=desription_size)],


	[sg.Text('Suggestion: ',				size=text_size, font = myfont),	sg.Text('Eat more fruit and vege, do regular excersice, sleep before 11pm, consume less carbonate drink and drink more mineral water', size=(60,2), font = myfont)],
			]

layout3=[
		[sg.Column(column1), sg.Column(column2)],
		[sg.Button('Back'), sg.Button('Test Again'),
		 sg.Text('Test Time',size=(9,1)),sg.Input('', key='TIME',size=(9,1)),
		 sg.Text('Test Date',size=(9,1)),sg.Input('', key='DATE',size=(11,1))]
	 	]

sg.Popup('		Welcome to BIMO','Your best personal healthcare advisor', font = 'Calibri 22')

#---------------------------------------
#window3-datacollect loop
def openwindow3loop(index):
	flag=-1
	while True:
		flag1 = openwindow3(index)
		if flag1 is 0:
			flag=0
			break
		if flag1 is -1:
			print('Handler Error in openwindow3')
			break
		if flag1 is 1:
			print('window3 Back')
			flag=1
			break
		if flag1 is 2:
			print('window3 Test Again')
			data_token = data[index].split()
			flag2, new_data2 = datacollect(index)
			current_time = time.asctime(time.localtime(time.time()))
			new_data3 = current_time.split()
			if flag2 is 0:
				flag=0
				break;
			if flag2 is -1:
				print('Handler Error in datacollect')
				break
			if flag2 is 1:
				print('All data required get')
				data[index]=' '.join(data_token[:6]+new_data2+[new_data3[3]]+[new_data3[1]+','+new_data3[2]+','+new_data3[4]])
				data[index]=data[index]+'\n'
				print(data[index])
	return 0

#main function
try:
	#ser = serial.Serial('/dev/ttyUSB0')
	ser = serial.Serial('/dev/ttyACM0')
	ser.flushInput()
except:
	print('serial init failed')
else:
	while True:
		flag1, index1 = openwindow1()
		if flag1 is 0:
			break
		if flag1 is -1:
			print('Handler Error in openwindow1')
			break
		if flag1 is 1:#NEW
			print('window1 New')
			flag2, new_data1 = openwindow2()
			if flag2 is 0:
				break
			if flag2 is -1:
				print('Handler Error in openwindow2')
				break
			if flag2 is 1:
				print('window2 Back')
			if flag2 is 2:
				print('window2 Next')
				flag3, new_data2 = datacollect(len(data))
				current_time = time.asctime(time.localtime(time.time()))
				new_data3 = current_time.split()
				if flag3 is 0:
					break
				if flag3 is -1:
					print('Handler Error in datacollect')
					break
				if flag3 is 1:
					print('All data required get')
					all_new_data=' '.join(new_data1+new_data2+[new_data3[3]]+[new_data3[1]+','+new_data3[2]+','+new_data3[4]])
					data.append(all_new_data+'\n')
					openwindow3loop(len(data)-1)
		if flag1 is 2:
			print('window1 View')
			openwindow3loop(index1)
	ser.close()
#---------------------------------------
#save input to file
#print('Saving data:',data)
if len(data)>=0:
	with open('data/data.txt', 'w') as file:
		data = file.writelines(data)
		file.close()
		print('data saved')
