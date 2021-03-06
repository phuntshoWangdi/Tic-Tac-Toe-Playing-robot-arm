from utils import stateOfBoard, locations, whosTurn
import TicTacToeMaster as ttt
import serial
from time import sleep
import cv2


sleep(1)
#open port for communication with arduino
try:
	portToArduino = serial.Serial('COM9', 9600)
except:
	print('Couldnot open the port')
	exit()

input("Please press enter to start...")

while 1:
	turn = whosTurn()
	if turn == '-': pass

	elif turn == 'X':

		print("X's turn!!")
		cur_state_of_board = stateOfBoard()
		if ' ' in cur_state_of_board:
		
			board, nextMove = ttt.getRandomBoard(cur_state_of_board)
			ttt.printBoard(board)
			
			bestMove = ttt.getAIMove(board, nextMove, nextMove)

			if bestMove != (-1,10) and bestMove != (-1,-10) and bestMove != (-1,0):
				#send command to arduino
				print(f'Move: {bestMove[0]}')
				if bestMove[0] == 0:
					position_to_send = locations[0]
				elif bestMove[0] == 1:
					position_to_send = locations[1]
				elif bestMove[0] == 2:
					position_to_send = locations[2]
				elif bestMove[0] == 3:
					position_to_send = locations[3]
				elif bestMove[0] == 4:
					position_to_send = locations[4]
				elif bestMove[0] == 5:
					position_to_send = locations[5]
				elif bestMove[0] == 6:
					position_to_send = locations[6]
				elif bestMove[0] == 7:
					position_to_send = locations[7]
				elif bestMove[0] == 8:
					position_to_send = locations[8]

				cmd = position_to_send+'\n'
				cmd_real = cmd

				print(f'cmd: {cmd}')

				cmd_temp = cmd[:]
				cmd = cmd.encode('utf-8')
				portToArduino.write(cmd)
				sleep(1)
				prev_cmd = cmd[:]

				new_cmd = ''
				for char in cmd_temp:
					if char == 'z':
						break
					new_cmd = new_cmd + char
				
				#drop down endstop
				new_cmd = new_cmd+'z-55\n'

				print(f'new_cmd: {new_cmd}')

				new_cmd = new_cmd.encode('utf-8')
				portToArduino.write(new_cmd)
				
				#pull back endstop
				new_cmd = prev_cmd[:]
				portToArduino.write(new_cmd)
				sleep(1)

				#return back to home position
				new_cmd = 'endstop\n'
				new_cmd =  new_cmd.encode('utf-8')
				portToArduino.write(new_cmd)

				turn = whosTurn()

				while turn == 'X':
					turn = whosTurn()
					if turn == 'O': break
		else: pass

	elif turn == 'O':
		print("O2's turn!!")
		while turn == 'O':
			turn = whosTurn()
			if turn == 'X': break

	else: pass

		



	
