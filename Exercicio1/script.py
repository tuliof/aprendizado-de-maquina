import csv
import math

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
	with open('dados2.csv', 'rb') as csvfile:
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

def listToMatrix(itemList):
	matrix = [[0 for x in xrange(5)] for x in xrange(len(itemList)) ]
	line = 0

	for item in itemList:
		matrix[line][0] = item.lineNumber
		matrix[line][1] = item.a
		matrix[line][2] = item.b
		matrix[line][3] = item.c
		matrix[line][4] = item.d
		line += 1

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
def sanitize(entityList):
	lineNumberList = []
	for ent in entityList:
		if math.isnan(ent.a) or math.isnan(ent.b) or math.isnan(ent.c) or math.isnan(ent.d):
			lineNumberList.append(ent.lineNumber)
			entityList.remove(ent)
	return lineNumberList

def test():
	entityList = readCsv()
	matrix = listToMatrix(entityList)
	print matrix

def doWork():
	entityList = readCsv()
	# Print the first 5 entities
	print 'First 5 entities:'
	for ent in entityList[:5]:
		print 'Line %s: %s, %s, %s, %s' % (ent.lineNumber, ent.a, ent.b, ent.c, ent.d)
	
	# Remove entities with empty attributes
	removedEntities = sanitize(entityList)
	print '\nLines with empty data (will not be considered): '
	for r in removedEntities:
		print r
	#

def main():
	#test()
	doWork()

if __name__ == '__main__':
	main()
