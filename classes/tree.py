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

		self.root.split(self.maxDepth, self.axis, self.divCrit)
		self.evaluate()


		self.getLeaves()
			

		# print(str(self.curDepth))
		# print('last Axis: %s' % self.axis)
		print('finished.')


	def evaluate(self):
		pass

	def getLeaves(self):

		for l in self.root.getLeaves():
			self.leaves.append(l)

	def postOrderWalk(self):

		self.root.postOrderWalk()


		

		

class Node():

	NODE_ID = 1
	NODE_INFO = []

	def __init__(self, parent):

		self.id = Node.NODE_ID
		self.depth = 0
		self.isLeaf = True
		self.leftChild = None
		self.rightChild = None
		self.parent = parent
		self.points = []

		Node.NODE_ID += 1


	def getMax(self, axis):

		cur_max = max([p.dim[axis] for p in self.points])

		return cur_max


	def getLeaves(self):

		
		if self.isLeaf:
			# print('leave')
			yield self
		else:
			yield from self.rightChild.getLeaves()
			yield from self.leftChild.getLeaves()	

	def postOrderWalk(self):

		if self.leftChild:
			self.leftChild.postOrderWalk()
		if self.rightChild:
			self.rightChild.postOrderWalk()

		Node.NODE_INFO.append((self.id, len(self.points)))

	def split(self, depth, axis, divCrit):

		if self.isLeaf:
			if depth > 0:
				self.leftChild = Node(self)
				self.rightChild = Node(self)
				self.isLeaf = False
				try:
					divisor = divCrit * self.getMax(axis)
				except ValueError:
					# enter smart error handling here
					# probably this only happens when the 
					# divisor gets too small
					# print(depth)
					pass
				finally:
					for point in self.points:
						if point.dim[axis] <= divisor:
							self.leftChild.points.append(point)
						else:
							self.rightChild.points.append(point)
					
					depth = depth - 1
					axis = (axis + 1) % 3
					self.leftChild.split((depth), axis, divCrit)
					self.rightChild.split((depth), axis, divCrit)
		else:
			depth = depth - 1
			axis = (axis + 1) % 3
			self.leftChild.split((depth), axis, divCrit)
			self.rightChild.split((depth), axis, divCrit)	


