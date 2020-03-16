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

	def getDeltaVs(self, bestN=None):

		deltaVs = []
		for node in self.tree.leaves:
			deltaVs.append((node.deltaV, node.id))

		deltaVs.sort(key=lambda tup:tup[0], reverse=True)

		return deltaVs

	def printInfo(self, numPoints, extended=False):

		print('Number of Points:			%.2e' % numPoints)
		print('initial total Volume:		%.4e' % self.initialTotalVolume)
		print('initial total DeadVolume:	%.4e' % self.initialTotalDeadVolume)
		print('Number of Leaves:			%s' % len(self.tree.leaves))
		
		if extended:

			kdTree.TREE_INFO.sort(key=lambda tup:tup[0])

			y = 0
			for n in kdTree.TREE_INFO:
				x = int(math.log2(n[0]))
				if x > y:
					print('')
					print(n[0], n[1], " ", end = '')
					y = x
				else:
					print(n[0],n[1] , " ", end = '')
			print('')


		

		

def run():

	depth = 2
	divCrit = 0.5
	startAxis = 0
	numPoints = 47000

	t = TreeController('assets/raw_data_01.csv')
	t.getInitialValues()
	t.initializeTree(depth, divCrit, startAxis)
	p = [i[0] for i in t.itemBoxes]
	t.tree.insert(p[0:numPoints])


	t.tree.grow()
	# t.tree.postOrderWalk()
	t.tree.breathFirstWalk()

	t.printInfo(numPoints, extended=True)

	for v in t.getDeltaVs():
		print(v)


run()
