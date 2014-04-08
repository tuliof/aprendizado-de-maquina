#!/usr/bin/env python
import numpy as np

def read_csv(filename):
	data = []
	classes = []

	with open(filename, 'rb') as f:
		lines = f.readlines()

		for line in lines:
			arr = line.split(',')
			obj_class = arr[len(arr)-1:][0].replace('\n','')
			classes.append(obj_class)
			data.append(map(float, arr[:len(arr)-1]))

	return (classes, data)

def extract_special_data(filename):
	test_set = []
	test_labels = []
	train_set = []
	train_labels = []
	test = True
	data_list = []
	data = ''

	with open(filename, 'rb') as f:
		lines = f.readlines()

		# Remove first 6 lines
		lines = lines[9:]
		
		for line in lines:
			if len(line) == 0:
				continue
			# Train
			elif len(line) == 8:
				test = False
				train_labels.append(line[1:6])
			# Test
			elif len(line) == 7:
				test = True
				test_labels.append(line[:5])
			else:
				data += line
				# End of data
				if data.find('}') != -1:
					data_list = data.lstrip().replace('\n','').replace('{','').replace('}','').split(' ')
					data_list = map(float, data_list)
					data = ''

					if test:
						test_set.append(data_list)
					else:
						train_set.append(data_list)
					data_list = []
	return (train_set, train_labels, test_set, test_labels)

def apply_pca(matrix):
	from matplotlib.mlab import PCA
	results = PCA(matrix)

	#this will return an array of variance percentages for each component
	print '\nVariance percentages: '
	variance = results.fracs

	print '\nMost variance found in series: '
	variance.sort()
	print variance[len(variance) - 1], variance[len(variance) - 2]

	showPCA2d(results.Y)

def svm_linear(matrix):
	#SVM Linear (C de 1e-3 a 1e4 em multiplos de 10)
	print 'ok'

def svm_rbf(matrix):
	#SVM RBF (C e gamma de 1e-3 a 1e4 em multiplos de 10)
	print 'ok'

def knn(train_data, train_classes, test_data, test_classes):
	#K vizinhos (K = 1,3,5,11,21,31)
	results = []
	number_of_classes = len(test_data)
	for n in (1,3,5,11,21,31):
		print 'Training with range %s' % n
		# Train
		clf = KNeighborsClassifier(n_neighbors=n, weights='uniform')
		clf.fit(train_data, train_classes)

		# Tests
		for x in range(0, len(test_data)):
			print 'Trying to predict: %s' % test_classes[x]
			preds = clf.predict(test_data[x])
			#print preds
			preds = np.array(preds.sort())
			#print np.where(preds==test_classes)
			accuracy = np.where(preds==np.array(test_classes.sort()), 1, 0).sum() / float(number_of_classes)

			results.append([n, accuracy])

	return results

def random_forrest():
	print 'ok'

def showPCA2d(pca_Y):
	x = []
	y = []

	#this will return a 2d array of the data projected into PCA space
	for item in pca_Y:
		x.append(item[0])
		y.append(item[1])

	import matplotlib.pyplot as plt
	plt.close('all')
	plt.plot(x, y, 'bo')
	plt.show()

def main():
	data = read_csv('sonar.all-data')
	classes = np.array(data[0])
	objects = np.array(data[1])
	apply_pca(objects)

if __name__ == '__main__':
	main()