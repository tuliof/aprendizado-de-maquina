#!/usr/bin/env python
import re
import numpy

def read_pgm(filename):
	pgm = []
	with open(filename, 'rb') as f:
		lines = f.read()
		# Remove first 3 lines
		lines = lines[11:]
		# Remove new lines and split into array
		lines = lines.replace('\n','').split(' ')
		# Remove last position, it is an empty string
		lines = lines[:4096]
		
		for i in xrange(0, len(lines), 64):
			pgm.append(lines[i:i+64])

		return pgm
		

if __name__ == "__main__":
	from matplotlib import pyplot
	image = read_pgm("./test17/1_007.BMP.inv.pgm")
	pyplot.imshow(image, pyplot.cm.gray)
	pyplot.show()