import matplotlib.pyplot as plt

files = ['brakes', 'throttles', 'steers']

try:
	for file in files:
		with open(file + '.csv', 'r') as f:
			reference_values = []
			our_values = []
			timesteps = []
			lines = f.readlines()
			for i, line in enumerate(lines):
				if i == 0: continue
				reference_value, our_value = map(float, line.split(','))
				reference_values.append(reference_value)
				our_values.append(our_value)
				timesteps.append(i)

			plt.plot(timesteps, our_values)
			plt.plot(timesteps, reference_values)
			plt.ylabel('value')
			plt.xlabel('timestep')
			plt.title(file)
			plt.legend(['ours', 'reference'])
			plt.show()
except:
	print('run dbw_test first')
