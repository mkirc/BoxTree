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

def run():

	depth = 2
	divCrit = 0.6
	startAxis = 0

	t = TreeController('assets/raw_data_01.csv')
	t.getInitialValues()
	t.initializeTree(depth, divCrit, startAxis)
	p = [i[0] for i in t.itemBoxes]
	# print([i.dim[1] for i in p[0:10]])
	t.tree.insert(p[0:10])
	t.tree.grow()
	t.printInfo()


run()
