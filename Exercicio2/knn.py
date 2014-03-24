#!/usr/bin/env python
import os
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn import svm

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
		print 'Processing: %s' % f
		file_metadata = os.path.basename(f).split('.')
		if file_metadata[3] != 'pgm':
			break
		else:
			data_class.append(get_class(file_metadata[0]))
			data.append(read_pgm_file(os.path.join(folder_path, f)))
	#print 'Number of samples: %s' % len(data)
	#print 'Number of classes: %s' % len(data_class)
	return (data, data_class)

def read_pgm_file(filename):
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
			pgm.append(map(int, lines[i:i+64]))

		return pgm
		
def get_class(filename):
	return os.path.basename(filename).split('.')[0][0]

def learn(samples, expected_values):
	'''
	In scikit-learn, we learn from existing data by creating 
	an estimator and calling its fit(X, Y) method.

	X -> The samples(Usually a 2d vector)
	y -> The expected values(Usually a 1d vector)
	'''
	clf = svm.LinearSVC()
	# Learn from the data
	clf.fit(samples, expected_values)

	# Return trained
	return clf

def predict(clf, data):
	print clf.predict(data)

def main():
	train_folder = './train17'
	test_folder = './test17'
	# Read data from file
	train_data = read_data(train_folder)
	
	# LEARN
	clf = learn(np.array(train_data[0]), np.array(train_data[1]))
	# PREDICT
	test_data = read_data(test_folder)
	predict(clf, np.array(test_data))

	#nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
	#distances, indices = nbrs.kneighbors(X)

	#data_class = get_class(filename)
	#print data_class

if __name__ == "__main__":
	main()
	#folder = './test17'
	#read_data(folder)
