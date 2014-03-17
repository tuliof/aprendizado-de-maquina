import csv
import math
from scipy import numpy

class Entity:
	a = -1
	b = -1
	c = -1
	d = -1
	lineNumber = 0

def readCsvToObject():
	entityList = []
	
	with open('dados2.csv', 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		rowNum = 0
		for row in spamreader:
			rowNum += 1
			# Skip the first line(header)
			if rowNum == 1:
				continue
			
			data = Entity()
			data.a = stringToFloat(row[0])
			data.b = stringToFloat(row[1])
			data.c = stringToFloat(row[2])
			data.d = stringToFloat(row[3])
			data.lineNumber = rowNum
			
			entityList.append(data)
	return entityList

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


def findMedian(matrix):
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
	calculateMedian(a)
	calculateMedian(b)
	calculateMedian(c)
	calculateMedian(d)

'''
The median of a data set is the data point above 
which half of  the data sits and below which half 
of the data sits - essentially, it's the "middle" 
point in a data set.
'''
def calculateMedian(dataList):
	sortedList = dataList.sort()
	

def test():
	entityList = readCsv()
	matrix = listToMatrix(entityList)
	print matrix

def doWork():
	matrix = readCsvToMatrix()
	# Print the first 5 entities
	#print '1 - %s' % len(matrix)
	print 'First 5 entities:'
	for l in matrix[:5]:
		print 'Line %s: %s, %s, %s, %s' % (l[0], l[1], l[2], l[3], l[4])
	
	# Remove entities with empty attributes
	removedEntities = sanitize(matrix)
	print '\nLines with empty data (will not be considered): '
	for r in removedEntities:
		print r
	#print '2 - %s' % len(matrix)
	findMedian(matrix)

def main():
	#test()
	doWork()

if __name__ == '__main__':
	main()
