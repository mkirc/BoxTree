import numpy as np

class Point():

	def __init__(self, xyzList):

		self.dim = xyzList
		self.vol = self.dim[0] * self.dim[1] * self.dim[2]

	def __add__(self, other):
		x = self.dim[0] + other.dim[0]
		y = self.dim[1] + other.dim[1]
		z = self.dim[2] + other.dim[2]
		return Point([x, y, z])

	def __sub__(self, other):
		x = np.sqrt((self.dim[0] - other.dim[0])**2)
		y = np.sqrt((self.dim[1] - other.dim[1])**2)
		z = np.sqrt((self.dim[2] - other.dim[2])**2)
		return Point([x, y, z])

	def __lt__(self, other):

		return self.vol < other.vol

class PointFactory():

	def __init__(self):
		
		self.itemBoxes = []

	def loadPoints(self, path):

		with open(path) as openFile:
			for line in openFile:
				self.parse(line)

	def parse(self, line):

		line = [i.strip() for i in line.split(',')]


		bbdim = [int(line[4]), int(line[5]), int(line[6])]
		# pick longest as x-axis 
		bbdim.sort()

		bb = Point([bbdim[2], bbdim[1], bbdim[0]])
		box = Point([int(line[1]), int(line[2]), int(line[3])])

		self.itemBoxes.append([bb, box])

	def getItemBoxes(self):

		return self.itemBoxes
