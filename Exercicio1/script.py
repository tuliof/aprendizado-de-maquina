#!/usr/bin/env python
import csv
import math

def readCsvToMatrix():
	with open('dados1.csv', 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		rowNum = 0
		for row in spamreader:
			rowNum += 1
			# Skip the first line(header)
			if rowNum == 1:
				continue
			elif rowNum == 2:
				matrix = [[rowNum,stringToFloat(row[0]),stringToFloat(row[1]),stringToFloat(row[2]),stringToFloat(row[3])]]
			matrix.append([rowNum,stringToFloat(row[0]),stringToFloat(row[1]),stringToFloat(row[2]),stringToFloat(row[3])])
	return matrix

def stringToFloat(stringFloat):
	num = 0
	try:
		num = float(stringFloat)
	except:
		num = float('nan')
	finally:
		return num

# Removes the records with missing data and return a list with each records line number.
def sanitize(matrix):
	lineNumberList = []
	for l in matrix:
		if math.isnan(l[1]) or math.isnan(l[2]) or math.isnan(l[3]) or math.isnan(l[4]):
			lineNumberList.append(l[0])
			matrix.remove(l)
	return lineNumberList

'''
The median of a data set is the data point above 
which half of  the data sits and below which half 
of the data sits - essentially, it's the "middle" 
point in a data set.
'''
def calculateMedian(arr):
	arr.sort()
	minor_modifier = 1.5
	major_modifier = 3
	
	q1 = 0
	q2 = 0
	q3 = 0
	#print 'Sorted array: %s' % arr
	half = len(arr) / 2 - 1
	quarter = int(math.ceil(half / 2.0))
	#print 'half: %s, quarter: %s' % (half, quarter)
	q1 = (arr[quarter] + arr[quarter+1]) / 2.0
	q3 = (arr[half+quarter] + arr[half+quarter+1]) / 2.0

	# Odd
	if (len(arr) % 2 == 1):
		q2 = arr[len(arr) / 2 + 1]
	else:
		#print 'Q2: [%s]:%s + [%s]:%s' % (half, arr[half], half + 1, arr[half + 1])
		q2 = (arr[half] + arr[half + 1]) / 2.0

	resultDict = {}
	resultDict['q1'] = q1
	resultDict['q2'] = q2
	resultDict['q3'] = q3

	inter_range = q3 - q1
	# Inner fence
	# If the point falls outside the inner fence, it is a minor outlier
	resultDict['inner_min'] = q1 - inter_range * minor_modifier
	resultDict['inner_max'] = q3 + inter_range * minor_modifier

	# Outer fence
	# If the point falls outside the outer fence, it is a MAJOR outlier
	resultDict['outer_min'] = q1 - inter_range * major_modifier
	resultDict['outer_max'] = q3 + inter_range * major_modifier
	# Return a tuple, for now...
	return (resultDict['outer_min'], resultDict['outer_max'])

def removeOutliers(matrix):
	a = []
	b = []
	c = []
	d = []
	# Get each data period and calculate the median.
	for l in matrix:
		a.append(l[1])
		b.append(l[2])
		c.append(l[3])
		d.append(l[4])
	
	a_lim = calculateMedian(a)
	b_lim = calculateMedian(b)
	c_lim = calculateMedian(c)
	d_lim = calculateMedian(d)
	
	print 'Outliers:'
	for l in matrix:
		# A
		if isOutsideLimits(l[1], a_lim):
			print 'Data A, line: %s, value: %s' % (l[0], l[1])
			# Remove outlier from the matrix
			matrix.remove(l)
		# B
		if isOutsideLimits(l[2], b_lim):
			print 'Data B, line: %s, value: %s' % (l[0], l[2])
			matrix.remove(l)
		# C
		if isOutsideLimits(l[3], c_lim):
			print 'Data C, line: %s, value: %s' % (l[0], l[3])
			matrix.remove(l)
		# D
		if isOutsideLimits(l[4], d_lim):
			print 'Data D, line: %s, value: %s' % (l[0], l[4])
			matrix.remove(l)
	print '\n'

def isOutsideLimits(value, tupleLimits):
	return value < tupleLimits[0] or value > tupleLimits[1]

def printHistogram():
	print 'a'

def test():
	entityList = readCsv()
	matrix = listToMatrix(entityList)
	print matrix

def doWork():
	matrix = readCsvToMatrix()
	# Print the first 5 entities
	print '1 - Matrix size: %s\n' % len(matrix)

	print 'First 5 entities:'
	for l in matrix[:5]:
		print 'Line %s: %s, %s, %s, %s' % (l[0], l[1], l[2], l[3], l[4])
	
	# Remove entities with empty attributes
	removedEntities = sanitize(matrix)
	print '\nLines with empty data (will not be considered): '
	for r in removedEntities:
		print r
	print '\n'
	
	print '2 - Matrix size: %s\n' % len(matrix)
	
	removeOutliers(matrix)

	print '3 - Matrix size: %s\n' % len(matrix)

	printHistogram()

def main():
	#test()
	doWork()

if __name__ == '__main__':
	main()
