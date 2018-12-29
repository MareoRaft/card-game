#!/usr/bin/env python
# The PIL library does not yet support python3.  Use python 2.
# Afterwards, use https://manytools.org/hacker-tools/convert-images-to-ascii-art/ at 26 with color

NUM_COLS = 13
NUM_ROWS = 5

WIDTH = 167.46
HEIGHT = 243.2

TOP_OFFSET = 6
RIGHT_OFFSET = 0
BOTTOM_OFFSET = 2
LEFT_OFFSET = 2

from PIL import Image
img = Image.open('data/cards.png')
for y_row in range(0, NUM_ROWS):
	y_offset = y_row * HEIGHT
	# the 'id' corresponds to the suit value
	y_id = y_row + 1
	for x_col in range(0, NUM_COLS):
		x_offset = x_col * WIDTH
		# set x id
		if (x_col == 0):
			x_id = 14
		else:
			x_id = x_col + 1
		# calculate boundaries
		x_left = x_offset + LEFT_OFFSET
		y_top = y_offset + TOP_OFFSET
		x_right = x_offset + WIDTH + RIGHT_OFFSET
		y_bottom = y_offset + HEIGHT + BOTTOM_OFFSET
		# crop and save
		img_cropped = img.crop((x_left, y_top, x_right, y_bottom))
		card_id = '{}-{}'.format(x_id, y_id)
		file_path = 'data/images/{}.png'.format(card_id)
		img_cropped.save(file_path)
