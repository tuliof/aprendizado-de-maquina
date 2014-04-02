#!/usr/bin/env python
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
import pandas as pd
import pylab as pl

def read_data(folder_path):
	from os import walk

	data = []
	data_class = []
	files = []

	# Loop all files in the folder
	for (dirpath, dirnames, filenames) in walk(folder_path):
		files.extend(filenames)
		break
	
	for f in files:
		#print 'Processing: %s' % f
		file_metadata = os.path.basename(f).split('.')
		if file_metadata[3] != 'pgm':
			break
		else:
			data_class.append(get_class(file_metadata[0]))
			data.append(read_pgm_file(os.path.join(folder_path, f)))

	return (data, data_class)

def read_pgm_file(filename):
	with open(filename, 'rb') as f:
		lines = f.read()
		# Remove first 3 lines
		lines = lines[12:]
		# Remove new lines and split into array
		lines = lines.replace('\n','').replace('\r','').replace('\'','').split(' ')
		# Remove last position, it is an empty string
		lines = map(int, lines[:4096])
		
		return lines
		
def get_class(filename):
	return int(os.path.basename(filename).split('.')[0][0])

def train(n, train_data, train_data_classes):
	print 'Training with range %s' % n
	clf = KNeighborsClassifier(n_neighbors=n, weights='uniform')
	# Train
	clf.fit(train_data, train_data_classes)
	return clf

def predict(clf, test_data, test_classes):
	results = []
	# Predict

	print test_classes
	number_of_classes = len(test_classes)

	for x in range(0, len(test_data)):
		print test_data[x]
		print 'Trying to predict number: %s' % test_classes[x]
		preds = clf.predict(test_data[x])
		print preds
		preds = np.array(preds.sort())
		#print np.where(preds==test_classes)
		accuracy = np.where(preds==np.array(test_classes.sort()), 1, 0).sum() / float(number_of_classes)
		#print "Neighbors: %d, Accuracy: %3f" % (n, accuracy)
		#results.append([n, accuracy])
	
def plot_result(results):
	# Plot results
	results = pd.DataFrame(results, columns=["n", "accuracy"])
	pl.plot(results.n, results.accuracy)
	pl.title("Accuracy with Increasing K")
	pl.show()

def main():
	train_folder = './train17'
	test_folder = './test17'
	# Read data from file
	
	# LEARN
	print 'Processing training files...'
	train_data = read_data(train_folder)
	# PREDICT
	print 'Processing testing files...'
	test_data = read_data(test_folder)

	np_test = np.array(test_data[0])
	np_test_classes = np.array(test_data[1])
	np_train = np.array(train_data[0])
	np_classes = np.array(train_data[1])
	results = []

	#for n in range(1, 51, 2):
	clf = train(23, np_train, np_classes)
	predict(clf, np_test, np_test_classes)

	print 'Test data classes'
	print test_data[1]

	#plot_result(results)

if __name__ == "__main__":
	main()
	#folder = './test17'
	#read_data(folder)
