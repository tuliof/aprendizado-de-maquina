#!/usr/bin/env python
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import PCA
from mpl_toolkits.mplot3d import Axes3D

def readCsv(csvFile):
	data = np.genfromtxt(csvFile, dtype=float, delimiter='\t', skip_header=1)
	return data

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
	ll = matrix.tolist()
	removedEntities = []
	for l in ll:
		if math.isnan(l[0]) or math.isnan(l[1]) or math.isnan(l[2]) or math.isnan(l[3]):
			removedEntities.append(l)
			ll.remove(l)
	matrix = np.array(ll, dtype=np.float32)
	return (matrix, removedEntities)

def calculateMedian(arr):
	arr.sort()
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
	
	# Outer fence - If the point falls outside the outer fence, it is a MAJOR outlier
	resultDict['outer_min'] = q1 - inter_range * major_modifier
	resultDict['outer_max'] = q3 + inter_range * major_modifier
	return (resultDict['outer_min'], resultDict['outer_max'])

def removeOutliers(matrix):
	ll = matrix.tolist()
	
	a = []
	b = []
	c = []
	d = []
	# Get each data period and calculate the median.
	for l in ll:
		a.append(l[0])
		b.append(l[1])
		c.append(l[2])
		d.append(l[3])
	
	a_lim = calculateMedian(a)
	b_lim = calculateMedian(b)
	c_lim = calculateMedian(c)
	d_lim = calculateMedian(d)
	
	print 'Outliers:'
	for l in ll:
		# A
		if isOutsideLimits(l[0], a_lim):
			print 'Data A, value: %s' % l[0]
			# Remove outlier from the list
			ll.remove(l)
		# B
		if isOutsideLimits(l[1], b_lim):
			print 'Data B, value: %s' % l[1]
			ll.remove(l)
		# C
		if isOutsideLimits(l[2], c_lim):
			print 'Data C, value: %s' % l[2]
			ll.remove(l)
		# D
		if isOutsideLimits(l[3], d_lim):
			print 'Data D, value: %s' % l[3]
			ll.remove(l)
	matrix = np.array(ll, dtype=np.float32)
	return matrix
	print '\n'

def isOutsideLimits(value, tupleLimits):
	return value < tupleLimits[0] or value > tupleLimits[1]

def printHistogram(matrix):
	matrixt = matrix.transpose()
	# Take column A
	hist, bins = np.histogram(matrixt[0], bins = 10)

	# Plot histogram
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)
	plt.show()

def covarMatrix(matrix):
	matrixt = matrix.transpose()
	x = np.cov(matrixt)
	return x

def calcAndDisplayPCA(matrix, graphType = '2d'):
	results = PCA(matrix)

	#this will return an array of variance percentages for each component
	print '\nVariance percentages: '
	variance = results.fracs
	print variance

	print '\nMost variance found in series: '
	variance.sort()
	print variance[len(variance) - 1], variance[len(variance) - 2]

	x = []
	y = []
	z = []
	#this will return a 2d array of the data projected into PCA space
	for item in results.Y:
		x.append(item[0])
		y.append(item[1])
		z.append(item[2])
	
	if graphType == '3d':
		showPCA3d(x,y,z)
	else:
		showPCA2d(x,y)

def showPCA2d(x, y):
	plt.close('all')
	plt.plot(x, y, 'bo')
	plt.show()

def showPCA3d(x, y, z):
	plt.close('all')
	ax = Axes3D(plt.figure())
	pltData = [x,y,z]
	ax.scatter(pltData[0], pltData[1], pltData[2], 'bo')
	# Plot the dots for each axis
	xAxisLine = ((min(pltData[0]), max(pltData[0])), (0, 0), (0,0))
	yAxisLine = ((0, 0), (min(pltData[1]), max(pltData[1])), (0,0))
	zAxisLine = ((0, 0), (0,0), (min(pltData[2]), max(pltData[2])))
	# Draw axis lines
	ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r') # X - Red
	ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'g') # Y - Green
	ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'b') # Z - Blue.
	plt.show()

def doWork():
	matrix = readCsv('dados1.csv')
	#print '1 - Matrix size: %s\n' % len(matrix)

	# Print the first 5 entities
	print 'First 5 entities:'
	for l in matrix[:5]:
		print l
	
	#print '\n2 - Matrix size: %s\n' % len(matrix)

	# Remove data with empty attributes
	sanitize_result = sanitize(matrix)
	matrix = sanitize_result[0]
	removedEntities = sanitize_result[1]

	print '\nLines with empty data (will not be considered): '
	for r in removedEntities:
		print r
	print '\n'
	
	#print '3 - Matrix size: %s\n' % len(matrix)
	matrix = removeOutliers(matrix)
	#print '\n4 - Matrix size: %s\n' % len(matrix)

	printHistogram(matrix)

	print '\nCovariance Matrix: '
	print '	A           B           C           D'
	print covarMatrix(matrix)

	# Can dislay 2D and 3D graphs, optional param graphType = 2d or 3d, default: 2d
	calcAndDisplayPCA(matrix)

def main():
	doWork()

if __name__ == '__main__':
	main()
