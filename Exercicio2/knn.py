#!/usr/bin/env python
import re
import numpy

def read_pgm(filename, byteorder='>'):
	"""Return image data from a raw PGM file as numpy array.

	Format specification: http://netpbm.sourceforge.net/doc/pgm.html

	"""
	pgm = []
	pgm_line = []
	FULL_LINE = 64
	LINE_SIZE = 17
	offset = 0
	with open(filename, 'rb') as f:
		lines = f.readlines()
		
		for line in lines:
			# Ignore first three lines
			if len(line) != 35:
				continue

			offset = FULL_LINE - len(pgm_line)
			if offset > LINE_SIZE:
				offset = 17
			
			pgm_line.extend(line.split(' ')[:offset]) # Ignore new line char
			#print pgm_line
			if len(pgm_line) == 64:
				pgm.append(pgm_line)
				pgm_line = []
		
		# Check if data is OK
		s = 0
		for l in pgm:
			s += len(l)

		print s / len(pgm)
		print len(pgm)

if __name__ == "__main__":
	from matplotlib import pyplot
	image = read_pgm("./test17/1_007.BMP.inv.pgm")
	#pyplot.imshow(image, pyplot.cm.gray)
	#pyplot.show()