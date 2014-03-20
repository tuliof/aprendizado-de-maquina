#!/usr/bin/python
import numpy as np
import math

def remove_empty(matrix):
	missingDataList = []
	for arr in matrix:
		for d in arr:
			if np.isnan(d):
				missingDataList.append(arr)
				matrix.remove(arr)
	return missingDataList

def getMedian(numericValues):
	theValues = sorted(numericValues)
	if len(theValues) % 2 == 1:
		return theValues[(len(theValues)+1)/2-1]
	else:
		lower = theValues[len(theValues)/2-1]
		upper = theValues[len(theValues)/2]
	
	return (float(lower + upper)) / 2  

def doWork():
	# Read csv file
	matrix = np.recfromcsv('dados2.csv', delimiter='\t', filling_values=np.nan, case_sensitive=True, deletechars='', replace_space=' ')
	dataList = matrix.tolist()
	# Print the first 5 entities
	for d in dataList[:5]:
		print d
	# Remove entities with empty attributes
	removed = remove_empty(dataList)
	# Print removed lines
	print '\nData removed:'
	for r in removed:
		print r
	# Remove outliers
	print reject_outliers(dataList)

def main():
	doWork()

if __name__ == '__main__':
	main()