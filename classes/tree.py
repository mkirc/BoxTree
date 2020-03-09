import numpy
import math

class kdTree():

	def __init__(self, depth, divCrit, startAxis):

		self.curDepth = 0
		self.maxDepth = depth
		self.axis = startAxis
		self.divCrit = divCrit
		self.root = Node(None)
		self.leaves = []

	def insert(self, points):

		self.root.points = points

	def grow(self):

		for d in range(self.maxDepth + 1):
				print(d)
				self.root.split(d, self.axis, self.divCrit)
				self.evaluate()

				self.axis = (self.axis + 1) % 3

		else:
			self.getLeaves()
			# print(str(self.curDepth))
			# print('last Axis: %s' % self.axis)
			print('finished.')


	def evaluate(self):
		pass

	def getLeaves(self):


		

		

class Node():

	def __init__(self, parent):

		self.depth = 0
		self.isLeaf = True
		self.leftChild = None
		self.rightChild = None
		self.parent = parent
		self.points = []
		# self.leaves = []


	def getMax(self, axis):

		cur_max = 0
		for p in self.points:
			cur_max = max(cur_max, p.dim[axis])
		return cur_max


	def getLeaves(self):

		
		if self.isLeaf:
			print('leave')
			return self
		else:
			self.rightChild.getLeaves()
			self.leftChild.getLeaves()	


	def split(self, depth, axis, divCrit):

		if self.isLeaf:
			if depth > 0:
				self.leftChild = Node(self)
				self.rightChild = Node(self)
				self.isLeaf = False
				for point in self.points:
					divisor = divCrit * self.getMax(axis)
					if point.dim[axis] <= divisor:
						self.leftChild.points.append(point)
					else:
						self.rightChild.points.append(point)
				depth = depth - 1
				self.leftChild.split((depth), axis, divCrit)
				self.leftChild.split((depth), axis, divCrit)
		else:
			depth = depth - 1
			self.leftChild.split((depth), axis, divCrit)
			self.leftChild.split((depth), axis, divCrit)	


