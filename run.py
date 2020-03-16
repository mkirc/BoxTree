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
		self.bestNodes = []

	def initializeTree(self, d, c, s):

		self.tree = kdTree(d, c, s)

	def getInitialValues(self):

		self.initialTotalVolume = np.sum(self.itemBoxes[:][0]).vol
		self.initialTotalDeadVolume =  (self.initialTotalVolume
										- np.sum(self.itemBoxes[:][1]).vol)

	def getDeltaVs(self, bestN=None):

		deltaVs = []
		for node in self.tree.leaves:
			deltaVs.append((node.deltaV, node))

		deltaVs.sort(key=lambda tup:tup[0], reverse=True)

		if bestN:
			return deltaVs[0:bestN]

		return deltaVs

	def getBestNodes(self):
		
		for mvp in self.getDeltaVs():
			dV, n = mvp
			self.bestNodes.append((n, dV))
			if dV == 0:
				break
		return


	def isNumPointsConst(self):

		allPoints = []

		for node in self.tree.leaves:

			allPoints += node.points

		assert len(allPoints) == len(self.tree.root.points)
		print('✔ no points lost!')
		print('')
		return


	def printInfo(self, numPoints, extended=False, bestN=False):

		print('Number of Points:\t\t\t%.2e' % numPoints)
		print('initial total Volume:\t\t%.4e' % self.initialTotalVolume)
		print('initial total DeadVolume:\t%.4e' % self.initialTotalDeadVolume)
		print('Number of Leaves:\t\t\t%s' % len(self.tree.leaves))
		
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

		if bestN:

			print(' Leaves with deltaV gain:	%i' % (len(self.bestNodes)))




		

		

def run():

	depth = 13
	divCrit = 0.5
	startAxis = 0
	numPoints = 47000

	t = TreeController('assets/raw_data_01.csv')
	t.getInitialValues()
	t.initializeTree(depth, divCrit, startAxis)
	p = [i[0] for i in t.itemBoxes]
	t.tree.insert(p[0:numPoints])


	t.tree.grow()
	t.tree.breathFirstWalk()
	# sanity check	
	t.isNumPointsConst()

	t.getBestNodes()

	t.printInfo(numPoints, bestN=True)


run()
