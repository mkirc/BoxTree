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
			deltaVs.append((node.deltaV, node))

		deltaVs.sort(key=lambda tup:tup[0], reverse=True)

		if bestN:
			return deltaVs[0:bestN]

		return deltaVs

	def isNumPointsConst(self):

		allPoints = []

		for node in self.tree.leaves:

			allPoints += node.points

		assert len(allPoints) == len(self.tree.root.points)
		print('✔ No points lost!')
		print('')		

	def printInfo(self, numPoints, extended=False, bestN=False):

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

		if bestN:

			count = []
			for mvp in self.getDeltaVs():
				dV, n = mvp
				count.append(mvp)
				if dV == 0:
					break

			print(' Leaves with deltaV gain:	%i' % (len(count)))




		

		

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

	t.printInfo(numPoints, bestN=100)


run()
