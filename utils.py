from PIL import ImageGrab
import numpy as np
import cv2
from time import sleep


locations = ['g1 x157 y126 z-20', 'g1 x135 y145 z-20', 'g1 x116 y167 z-20',
			'g1 x126 y99 z-20',   'g1 x102 y110 z-20', 'g1 x87 y131 z-20',
			'g1 x97 y70 z-20',    'g1 x78 y84 z-20',   'g1 x62 y98 z-20'
]

def stateOfBoard():
	states = [' ']*9

	pil_img = ImageGrab.grab(bbox=(275,292,683,730))
	pil_img = pil_img.resize((408,408)).convert('L')

	image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

	img_lst = [
				image[0:120, 0:120],   image[0:120, 146:270],   image[0:120,293:400],
				image[140:270, 0:120], image[140:268, 145:270], image[140:270,292:400],
				image[287:400, 0:120], image[287:400,145:270],  image[287:400,292:403]
			  ]

	for i in range(len(img_lst)):
		template_o = cv2.imread('./template/o.jpg')
		template_x = cv2.imread('./template/x.jpg')

		result_o = cv2.matchTemplate(
									cv2.resize(img_lst[i],(120,120)), 
									template_o, cv2.TM_CCOEFF_NORMED)
		result_x = cv2.matchTemplate(
									cv2.resize(img_lst[i],(120,120)), 
									template_x, cv2.TM_CCOEFF_NORMED)

		if np.amax(result_o) >= 0.8: states[i] = 'O'
		elif np.amax(result_x) >= 0.8: states[i] = 'X'
		else: states[i] = ' '

	return states

def whosTurn():
	sleep(1)
	pil_img = ImageGrab.grab(bbox=(457,233,483,265)).convert('L') #bbox(x,y,w,h)

	turn_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)



	turn_o = cv2.imread('./template/turn_O.jpg')
	turn_x = cv2.imread('./template/turn_X.jpg')

	result_o = cv2.matchTemplate(
								turn_img, 
								turn_o, cv2.TM_CCOEFF_NORMED)
	result_x = cv2.matchTemplate(
								turn_img,
								turn_x, cv2.TM_CCOEFF_NORMED) 

	if np.amax(result_o) >= 0.8: return 'O'
	elif np.amax(result_x) >= 0.8: return 'X'
	else: return '-'
