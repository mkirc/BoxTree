import numpy
import math



class kdTree():

	TREE_INFO = []

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

		print('finished tree groth.')


	def evaluate(self):
		pass

	def getLeaves(self):

		for l in self.root.getLeaves():
			self.leaves.append(l)

	def postOrderWalk(self):

		self.root.postOrderWalk()

	def breathFirstWalk(self):

		root = self.root
		toVisit = [root]
		NODE_ID = 1
		while toVisit:
			cur = toVisit.pop(0)
			
			kdTree.TREE_INFO.append((cur.id, len(cur.points)))
			if cur.leftChild:
				NODE_ID += 1
				cur.leftChild.id = NODE_ID
				toVisit.append(cur.leftChild)
			if cur.rightChild:
				NODE_ID += 1
				cur.rightChild.id = NODE_ID
				toVisit.append(cur.rightChild)



		

		

class Node():



	def __init__(self, parent):

		self.id = 1
		self.depth = 0
		self.isLeaf = True
		self.leftChild = None
		self.rightChild = None
		self.parent = parent
		self.points = []

		# Node.NODE_ID += 1


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
		

	def split(self, depth, axis, divCrit):

		if self.isLeaf:
			if depth > 0:
				self.leftChild = Node(self)
				self.rightChild = Node(self)
				self.isLeaf = False
				self.leftChild.depth += 1
				self.rightChild.depth += 1
				try:
					divisor = divCrit * self.getMax(axis)
				except ValueError:
					# enter smart error handling here
					# only happens when the leaf of interest is empty
					divisor = 0

				for point in self.points:
					if point.dim[axis] < divisor:
						self.leftChild.points.append(point)
					else:
						self.rightChild.points.append(point)
				
				depth = depth - 1
				axis = (axis + 1) % 3
				

				self.leftChild.split((depth), axis, divCrit)
				self.rightChild.split((depth), axis, divCrit)

		# else:
		# 	depth = depth - 1
		# 	axis = (axis + 1) % 3
		# 	self.leftChild.split((depth), axis, divCrit)
		# 	self.rightChild.split((depth), axis, divCrit)	


