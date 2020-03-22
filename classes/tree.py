import math
import numpy as np
from classes.point import Point, ItemBoxFactory
from classes.writer import Writer


class kdTree():

    TREE_INFO = []

    def __init__(self, depth, divCrit, startAxis):

        self.curDepth = 0
        self.maxDepth = depth
        self.axis = startAxis
        self.divCrit = divCrit
        self.root = Node(None)
        self.root.dim = [0, 0, 0]
        self.root.lastCut = [0, 0, 0]
        self.root.vol = self.root.dim[0] * self.root.dim[1] * self.root.dim[2]
        self.leaves = []

    def insert(self, points):

        self.root.points = points
        self.getMaxOfAllDim()

        print('points inserted.')

    def grow(self):

        print('growing tree...')
        self.root.split(self.maxDepth, self.axis, self.divCrit)

        self.getLeaves()

        self.breathFirstWalk()

        print('tree groth finished.')

    def getMaxOfAllDim(self):

        for i in range(0, 3):
            self.root.dim[i] = max([p.dim[i] for p in self.root.points])
        return


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
        self.dim = []
        self.lastCut = None
        self.vol = None
        self.deltaV = 0

    def getLeaves(self):

        
        if self.isLeaf:
            # print('leave')
            yield self
        else:
            yield from self.rightChild.getLeaves()
            yield from self.leftChild.getLeaves()   

    def calculateVolume(self):

        self.vol = self.dim[0] * self.dim[1] * self.dim[2]
    
    def calculateDeltaV(self):

        # look at the README for explanation
        self.deltaV = len(self.points) * (self.parent.vol - self.vol)

    def split(self, depth, axis, divCrit):

        if self.isLeaf:
            if depth > 0:
                self.leftChild = Node(self)
                self.leftChild.lastCut = [i for i in self.lastCut]
                self.rightChild = Node(self)
                self.rightChild.lastCut = [i for i in self.lastCut]
                self.isLeaf = False
                self.leftChild.depth += 1
                self.rightChild.depth += 1
                try:
                    divisor = int(divCrit * (self.dim[axis] - self.lastCut[axis])) + self.lastCut[axis]
                except ValueError:
                    # enter smart error handling here
                    # only happens when the leaf of interest is empty
                    divisor = 0

                for point in self.points:
                    if point.dim[axis] < divisor:
                        self.leftChild.points.append(point)
                    else:
                        self.rightChild.points.append(point)
                
                
                self.leftChild.dim = [int(i) for i in self.dim]
                self.leftChild.dim[axis] = divisor
                self.leftChild.calculateVolume()
                self.leftChild.calculateDeltaV()
                self.rightChild.lastCut[axis] = divisor
                self.rightChild.dim = [int(i) for i in self.dim]
                self.rightChild.calculateVolume()
                self.rightChild.deltaV = self.deltaV

                depth = depth - 1
                axis = (axis + 1) % 3
                

                self.leftChild.split((depth), axis, divCrit)
                self.rightChild.split((depth), axis, divCrit)

class TreeControl():

    def __init__(self):

        self.ibf = ItemBoxFactory()
        self.initialTotalDeadVolume = 0
        self.initialTotalVolume = 0
        self.endTotalVolume = 0
        self.writer = Writer()
        self.itemBoxes = []
        self.tree = None
        self.bestNodes = []
        self.newItemBoxes = None
        self.newTotalDeadVolume = 0
        self.newTotalVolume = 0
        self.gain = 0

    def getInitialItemBoxes(self, path, numPoints=None):

        self.ibf.loadCSV(path)
        self.itemBoxes = self.ibf.getItemBoxes(numPoints)
        self.ibf.reset()


    def initializeTree(self, d, c, s):

        self.tree = kdTree(d, c, s)

    def getInitialValues(self):

        self.initialTotalVolume = np.sum([b[0].vol for b in self.itemBoxes],dtype=np.int64)
        self.initialTotalDeadVolume = (np.sum([b[1].vol for b in self.itemBoxes],dtype=np.int64)
                                       - self.initialTotalVolume)

    def getDeltaVs(self, bestN=None):

        deltaVs = []
        for node in self.tree.leaves:
            deltaVs.append((node.deltaV, node))

        deltaVs.sort(key=lambda tup:tup[0], reverse=True)

        if bestN is not None:
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
        # print('✔ no points lost!')
        print('no points lost!')
        print('')
        return

    # def getNewItemBoxes(self, path):

    #     self.ibf.loadCSV(path)
    #     self.newItemBoxes = self.ibf.getItemBoxes()
    #     self.ibf.reset()

    # def writeOutNewItemBoxes(self, path):

    #     self.tree.leaves.sort(key=lambda node: node.id)
    #     bestNodesCopy = [i for i in self.bestNodes]
    #     bestNodesCopy.sort(key=lambda tup: tup[0])

    #     print('start writing...')
    #     self.writer.write(path, bestNodesCopy, self.tree.leaves)

    def writeNewBoxesCSV(self, path):

        print('writing new: %s' % (path))

        with open(path, 'w+') as openFile:

            for n in self.bestNodes:
                x = n[1].dim[0]
                y = n[1].dim[1]
                z = n[1].dim[2]

                line = ('KARTON %s,%s,%s,%s,%s,\n') % (n[0],n[2],x,y,z)
                openFile.write(line)


    def getNewValues(self):

        self.newTotalVolume = np.sum([b[0].vol for b in self.newItemBoxes],dtype=np.int64)
        self.newTotalDeadVolume = (np.sum([b[1].vol for b in self.newItemBoxes],dtype=np.int64)
                                   - self.newTotalVolume)
        self.gain = self.newTotalDeadVolume / self.initialTotalDeadVolume

    def printInfo(self, extended=False, bestN=False):

        print('Number of Points:\t\t\t%i' % len(self.itemBoxes))
        print('Dimension of Root:\t\t\t%s' % self.tree.root.dim)
        print('Initial total Volume:\t\t%.4e' % self.initialTotalVolume)
        print('Initial total DeadVolume:\t%.4e' % self.initialTotalDeadVolume)
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
            print('Leave Dimensions:')

            for n in self.tree.leaves:
                print(n.id, n.dim, n.lastCut)

        if bestN:

            print(' Leaves with deltaV gain:    %i' % (len(self.bestNodes)))

            w = Writer()
            w.plot([i[2] for i in self.bestNodes])

        # print('')
        # print('new total Volume:\t\t\t%.4e' % self.newTotalVolume)
        # print('new total DeadVolume:\t\t%.4e' % self.newTotalDeadVolume)
        # print('Thats like...%.3f of the initial!' % self.gain)