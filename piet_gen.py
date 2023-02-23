import numpy as np
from PIL import Image
import imageio

class Color(object):
	
	def __init__(self, color_table=None):
		if color_table is None:
			self.color_table = [1,0]
		else:
			self.color_table = color_table
			
	def RGB(self):
		if self.color_table[1] == 0:
			#Red
			if self.color_table[0] == 0:
				#Light
				return [255,192,192]
			elif self.color_table[0] == 1:
				#Normal
				return [255,0,0]
			elif self.color_table[0] == 2:
				#Dark
				return [192,0,0]
		elif self.color_table[1] == 1:
			#Yellow
			if self.color_table[0] == 0:
				#Light
				return [255,255,192]
			elif self.color_table[0] == 1:
				#Normal
				return [255,255,0]
			elif self.color_table[0] == 2:
				#Dark
				return [192,192,0]
		elif self.color_table[1] == 2:
			#Green
			if self.color_table[0] == 0:
				#Light
				return [192,255,192]
			elif self.color_table[0] == 1:
				#Normal
				return [0,255,0]
			elif self.color_table[0] == 2:
				#Dark
				return [0,192,0]
		elif self.color_table[1] == 3:
			#Cyan
			if self.color_table[0] == 0:
				#Light
				return [192,255,255]
			elif self.color_table[0] == 1:
				#Normal
				return [0,255,255]
			elif self.color_table[0] == 2:
				#Dark
				return [0,192,192]
		elif self.color_table[1] == 4:
			#Blue
			if self.color_table[0] == 0:
				#Light
				return [192,192,255]
			elif self.color_table[0] == 1:
				#Normal
				return [0,0,255]
			elif self.color_table[0] == 2:
				#Dark
				return [0,0,192]
		elif self.color_table[1] == 5:
			#Magenta
			if self.color_table[0] == 0:
				#Light
				return [255,192,255]
			elif self.color_table[0] == 1:
				#Normal
				return [255,0,255]
			elif self.color_table[0] == 2:
				#Dark
				return [192,0,192]

	def push_color(self):
		self.color_table[0] = (self.color_table[0] + 1) % 3
		return self.RGB()

	def write_color(self):
		self.color_table[0] = (self.color_table[0] + 2) % 3
		self.color_table[1] = (self.color_table[1] + 5) % 6
		return self.RGB()

current_color = Color()
piet_painting = []

def draw_block(size,num):
	block = np.zeros( (12,12,3), dtype=np.uint8 )	

	if num != 0:
		old_push_color = current_color.push_color()
		current_color.write_color()
		block[:,:] = current_color.RGB()
		block[0,0] = old_push_color
		size = size +1
	else:
		block[:,:] = current_color.RGB()
	
	pix_lft = 144-size
	div = pix_lft // 12
	rem = pix_lft % 12
	if div !=0:
		block[12-div:,]=0
	block[11-div:,:rem]=0

	pos_y = 12*num
	pos_x = 0
	piet_painting[pos_x:pos_x+12,pos_y:pos_y+12] = block

def draw_end(num):
	block = np.zeros( (12,5,3), dtype=np.uint8 )
	
	old_push_color = current_color.push_color()
	block[:,:] = 255
	block[0,0] = old_push_color
	block[0,1] = current_color.write_color()

	block[0:2,3] = 0
	block[1,1] = 0
	block[2,0] = 0
	block[2,4] = 0
	block[3,1:4] = 0
	block[2,1:4]=current_color.write_color()

	pos_y = 12*num
	pos_x = 0
	piet_painting[pos_x:pos_x+12,pos_y:pos_y+5] = block

message = input("Write your message here: \n")
painting_len = len(message)*12 + 5
piet_painting = np.zeros((12,painting_len,3), dtype=np.uint8)

i = 0
for char in message:
	draw_block(ord(char),i)
	i += 1
draw_end(i)

if painting_len < 390:
	plato_painting = imageio.v2.imread('Plato.png')
	plato_painting[0:12,0:painting_len] = piet_painting
	plato_img = Image.fromarray(plato_painting)
	imageio.imwrite('plato_code.png', plato_img)

img = Image.fromarray(piet_painting)
imageio.imwrite('piet_code_file.png', img)
