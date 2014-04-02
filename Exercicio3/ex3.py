#!/usr/bin/env python

def extract_data_from_file(filename):
	test_set = []
	train_set = []
	test = True
	data_list = []
	data = ''
	header = ''

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
				header = line[1:6]
			# Test
			elif len(line) == 7:
				test = True
				header = line[:5]
			else:
				data += line
				# End of data
				if data.find('}') != -1:
					data_list = data.lstrip().replace('\n','').replace('{','').replace('}','').split(' ')
					data_list = map(float, data_list)
					data = ''

					data_list.insert(0, header)
					print data_list
					if test:
						test_set.append(data_list)
					else:
						train_set.append(data_list)
					data_list = []
	return (train_set, test_set)


extract_data_from_file('sonar.mines')