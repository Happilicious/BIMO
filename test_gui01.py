import PySimpleGUI as sg

layout = [
		  [sg.Text('window 1')],
		  [sg.Input(do_not_clear=True)],
		  [sg.Text('',key='_OUTPUT_')],
		  [sg.Button('Launch 2')]
		 ]

win1 = sg.Window('window 1', layout)
win2_active=False

while True:
	ev1, vals1 = win1.Read(timeout=100)
	if ev1 is None:
		break
	win1.Element('_OUTPUT_').Update(vals1[0])
	if ev1 == 'Launch 2' and not win2_active:
		win2_active = True
		win1.Hide()
		layout2 = [
				   [sg.Text('Window 2')],
				   [sg.Button('Exit')]
				  ]
		win2 = sg.Window('window 2', layout2)
		while True:
			ev2, vals2 = win2.Read()
			if ev2 is None or cv2 == 'Exit':
				win2.Close()
				win2.active = False
				win1.Unhide()
				break
