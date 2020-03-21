import numpy
import math

from classes.point import *
from classes.tree import *

class TreeController():

	def __init__(self):

		# self.pf = PointFactory()
		self.ibf = ItemBoxFactory()
		self.initialTotalDeadVolume = 0
		self.initialTotalVolume = 0
		self.endTotalVolume = 0
		# self.pf.loadPoints(path)
		# self.itemBoxes = self.pf.getItemBoxes()
		self.itemBoxes = []
		self.tree = None
		self.bestNodes = []
		self.newItemBoxes = None
		self.newTotalDeadVolume = 0
		self.newTotalVolume = 0
		self.gain = 0

	def getInitialItemBoxes(self, path):

		self.ibf.loadCSV(path)
		self.itemBoxes = self.ibf.getItemBoxes()
		self.ibf.reset()


	def initializeTree(self, d, c, s):

		self.tree = kdTree(d, c, s)

	def getInitialValues(self):

		self.initialTotalVolume = np.sum([b[0].vol for b in self.itemBoxes])
		self.initialTotalDeadVolume =  (np.sum([b[1].vol for b in self.itemBoxes])
										- self.initialTotalVolume)

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
			self.bestNodes.append((n.id, n, dV))
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

	def writeOutNewItemBoxes(self, path):

		print('start writing...')
		self.tree.leaves.sort(key=lambda node:node.id)
		bestNodesCopy = [i for i in self.bestNodes]

		with open(path, 'w+') as openFile:

			
			bestNodesCopy.sort(key=lambda tup:tup[0])

			for l in self.tree.leaves:

				if l.id < bestNodesCopy[0][0]:
					
					kNom = 'KARTON' + ' ' + str(self.bestNodes[0][0])
					kDimX = bestNodesCopy[0][1].dim[0]
					kDimY = bestNodesCopy[0][1].dim[1]
					kDimZ = bestNodesCopy[0][1].dim[2]

					for point in l.points:

						pDimX = point.dim[0]
						pDimY = point.dim[1]
						pDimZ = point.dim[2]

						line = '%s,%s,%s,%s,%s,%s,%s,\n' % (kNom,kDimX,kDimY,kDimZ,pDimX,pDimY,pDimZ)

						openFile.write(line)

				elif l.id == bestNodesCopy[0][0]:

					kNom = 'KARTON' + ' ' + str(self.bestNodes[0][0])
					kDimX = bestNodesCopy[0][1].dim[0]
					kDimY = bestNodesCopy[0][1].dim[1]
					kDimZ = bestNodesCopy[0][1].dim[2]

					for point in l.points:
						
						pDimX = point.dim[0]
						pDimY = point.dim[1]
						pDimZ = point.dim[2]

						line = '%s,%s,%s,%s,%s,%s,%s,\n' % (kNom,kDimX,kDimY,kDimZ,pDimX,pDimY,pDimZ)

						openFile.write(line)

					lastNode = bestNodesCopy.pop(0)
					# print('last Node: %s. Only %s to go!' % (lastNode[0], len(self.bestNodes)))
			else:

				print('✔ finished writing %s' % (path))
				print('')
				return

	def getNewItemBoxes(self, path):

		self.ibf.loadCSV(path)
		self.newItemBoxes = self.ibf.getItemBoxes()
		self.ibf.reset()


	def getNewValues(self):

		# self.pf.loadPoints(path, new=True)
		# self.newItemBoxes = self.pf.getNewItemBoxes()
		self.newTotalVolume = np.sum([b[0].vol for b in self.newItemBoxes])
		self.newTotalDeadVolume =  (np.sum([b[1].vol for b in self.newItemBoxes])
										- self.newTotalVolume)
		self.gain = self.newTotalDeadVolume / self.initialTotalDeadVolume



	def printInfo(self, numPoints, extended=False, bestN=False):

		print('Number of Points:\t\t\t%i' % numPoints)
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

		print('')
		print('new total Volume:\t\t\t%.4e' % self.newTotalVolume)
		print('new total DeadVolume:\t\t%.4e' % self.newTotalDeadVolume)
		print('Thats like...%.3f of the initial!' % self.gain)



		

		

def run():

	depth = 13
	divCrit = 0.5
	startAxis = 0
	numPoints = 47287

	outPath = 'assets/new_boxes_86.csv'

	# t = TreeController('assets/raw_data_01.csv')
	t = TreeController()
	t.getInitialItemBoxes('assets/raw_data_01.csv')
	t.getInitialValues()
	t.initializeTree(depth, divCrit, startAxis)
	p = [i[0] for i in t.itemBoxes]
	t.tree.insert(p[0:numPoints])


	t.tree.grow()
	t.tree.breathFirstWalk()
	# sanity check	
	t.isNumPointsConst()

	t.getBestNodes()

	t.writeOutNewItemBoxes(outPath)

	t.getNewItemBoxes(outPath)
	t.getNewValues()

	t.printInfo(numPoints, bestN=True)


run()
