#!/usr/bin/env python
import numpy as np

def extract_data_from_file(filename):
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

data = extract_data_from_file('sonar.rocks')

arr_train = np.array(data[2], dtype=np.float32).T
print len(arr_train)
print len(arr_train)
apply_pca(arr_train)