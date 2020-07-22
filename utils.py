from PIL import ImageGrab
import numpy as np
import cv2


# locations = ['g1 x150 y118 z-40', 'g1 x132 y138 z-40',	'g1 x118 y15 z-40',
# 			'g1 x128 y95 z-40',	  'g1 x105 y110 z-40',	'g1 x89 y125 z-40',
# 			'g1 x95 y66 z-40',	  'g1 x79 y80 z-40',	'g1 x59 y89 z-40',
# ]

locations = ['g1 x157 y126 z-20', 'g1 x132 y138 z-20', 'g1 x111 y160 z-20',
			'g1 x128 y95 z-20',   'g1 x105 y110 z-20', 'g1 x89 y125 z-20',
			'g1 x98 y68 z-20',    'g1 x79 y80 z-20',   'g1 x68 y98 z-20'
]

#last row -> 'g1 x95 y66 z-20 g1 x79 y80 z-20' 'g1 x59 y89 z-20'


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
