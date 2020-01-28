files = ['brakes', 'throttles', 'steers']

try:
	for file in files:
		with open(file + '.csv', 'r') as f:
			error = 0.0
			lines = f.readlines()
			for i, line in enumerate(lines):
				if i == 0: continue
				reference_value, our_value = map(float, line.split(','))
				error += abs(reference_value - our_value)
			print(file + " error: " + str(error))
except:
	print('run dbw_test first')
