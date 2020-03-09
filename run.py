import numpy
import math

from classes.point import *
from classes.tree import *

class TreeController():

	def __init__(self, path):

		self.pf = PointFactory()
		self.initialTotalDeadVolume = 0
		self.initialTotalVolume = 0
		self.endTotalVolume = 0
		self.pf.loadPoints(path)
		self.itemBoxes = self.pf.getItemBoxes()
		self.tree = None

	def initializeTree(self, d, c, s):

		self.tree = kdTree(d, c, s)

	def getInitialValues(self):

		self.initialTotalVolume = np.sum(self.itemBoxes[:][0]).vol
		self.initialTotalDeadVolume =  self.initialTotalVolume - np.sum(self.itemBoxes[:][1]).vol

	def printInfo(self):

		print('initial total Volume:		%.4e' % self.initialTotalVolume)
		print('initial total DeadVolume:	%.4e' % self.initialTotalDeadVolume)
		print('Number of Leaves:			%s' % len(self.tree.leaves))
		self.sortNodeInfo()
		y = 0
		for n in Node.NODE_INFO:
			x = int(math.log2(n[0]))
			if x > y:
				print('')
				print(n[0], n[1], " ", end = '')
				y = x
			else:
				print(n[0] , n[1] , " ", end = '')
		print('')
			

	def sortNodeInfo(self):

		Node.NODE_INFO.sort(key=lambda tup: tup[0])

		

def run():

	depth = 4
	divCrit = 0.1
	startAxis = 0
	numPoints = 47000

	t = TreeController('assets/raw_data_01.csv')
	t.getInitialValues()
	t.initializeTree(depth, divCrit, startAxis)
	p = [i[0] for i in t.itemBoxes]
	# print([i.dim[1] for i in p[0:10]])
	t.tree.insert(p[0:numPoints])


	t.tree.grow()
	t.tree.postOrderWalk()

	t.printInfo()


run()
