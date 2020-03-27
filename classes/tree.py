import math
import numpy as np
import random
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
        self.leaves = []

    def insert(self, points):

        self.root.points = points
        self.getMaxOfAllDim()
        self.root.calculateVolume()
        print('points inserted.')

    def grow(self, splitMode=0, dVMode=0):

        print('growing tree...')
        
        if splitMode == 0:
            self.root.split(self.maxDepth, self.axis, self.divCrit, dVMode)
        elif splitMode == 1:
            self.root.splitByMax(self.maxDepth, self.axis, self.divCrit, dVMode)
        elif splitMode == -1:
            self.root.splitRandom(self.maxDepth, self.axis, dVMode)


        self.getLeaves()

        self.breathFirstWalk()

        print('tree groth finished.')

    def getMaxOfAllDim(self):

        for i in range(0, 3):
            self.root.dim[i] = max([p.dim[i] for p in self.root.points])
        return

    def SortPointsByDiag(self):

        diagList = []
        diagSet = set()
        for p in self.root.points:
            q = int(math.sqrt(p.dim[0]**2 + p.dim[1]**2 + p.dim[2]**2))
            if q not in diagSet:
                diagSet.add(q)
                diagList.append((p,q))
        diagList.sort(reverse=True, key=lambda tup:tup[1])
        return diagList

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
    
    def calculateDeltaV(self, dVMode):

        # look at the README for explanation
        if dVMode == 1:
            try:
                rel = (self.parent.vol - self.vol)
                deltaV = len(self.points) * rel / (len(self.points) * self.parent.vol)
            except ZeroDivisionError:
                deltaV = 0

        elif dVMode == 0:
            deltaV = len(self.points) * (self.parent.vol - self.vol)
        

        elif dVMode == 2:
            deltaV = self.calculateLocalDeathVolume()

        return deltaV



    def getMax(self, axis):

        curMax = max([p.dim[axis] for p in self.points])

        return curMax


    def calculateLocalDeathVolume(self):

        pVol = np.sum([p.vol for p in self.points], dtype=np.int64)
        dVol = (self.vol * len(self.points)) - pVol
        return dVol


    def split(self, depth, axis, divCrit, dVMode):

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
                self.leftChild.deltaV = self.leftChild.calculateDeltaV(dVMode)
                self.rightChild.lastCut[axis] = divisor
                self.rightChild.dim = [int(i) for i in self.dim]
                self.rightChild.calculateVolume()
                self.rightChild.deltaV = self.deltaV

                depth = depth - 1
                axis = (axis + 1) % 3
                

                self.leftChild.split((depth), axis, divCrit, dVMode)
                self.rightChild.split((depth), axis, divCrit, dVMode)

    def splitByMax(self, depth, axis, divCrit, dVMode):

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
                    divisor = int(divCrit * (self.getMax(axis) - self.lastCut[axis])) + self.lastCut[axis]
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
                self.rightChild.dim = [int(i) for i in self.dim]
                try:
                    self.rightChild.dim[axis] = self.rightChild.getMax(axis)
                    self.rightChild.lastCut[axis] = self.rightChild.getMax(axis)
                except ValueError:
                    self.rightChild.dim[axis] = divisor
                    self.rightChild.lastCut[axis] = divisor

                try:
                    self.leftChild.dim[axis] = self.leftChild.getMax(axis)
                except ValueError:
                    self.leftChild.dim[axis] = divisor

                self.leftChild.calculateVolume()
                self.leftChild.deltaV = self.leftChild.calculateDeltaV(dVMode)
                
                

                self.rightChild.calculateVolume()
                self.rightChild.deltaV = self.deltaV

                depth = depth - 1
                axis = (axis + 1) % 3
                

                self.leftChild.splitByMax((depth), axis, divCrit, dVMode)
                self.rightChild.splitByMax((depth), axis, divCrit, dVMode)

    def splitRandom(self, depth, axis, dVMode):

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
                    divCrit = random.choice(range(30,80)) / 100
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
                self.leftChild.deltaV = self.leftChild.calculateDeltaV(dVMode)
                self.rightChild.lastCut[axis] = divisor
                self.rightChild.dim = [int(i) for i in self.dim]
                self.rightChild.calculateVolume()
                self.rightChild.deltaV = self.deltaV

                depth = depth - 1
                axis = (axis + 1) % 3
                
                self.leftChild.splitRandom(depth, axis, dVMode)
                self.rightChild.splitRandom(depth, axis, dVMode)


class TreeControl():

    def __init__(self):

        self.ibf = ItemBoxFactory()
        self.initialTotalDeadVolume = 0
        self.initialTotalBoxVolume = 0
        self.initialTotalItemVolume = 0
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

        self.initialTotalItemVolume = np.sum([b[0].vol for b in self.itemBoxes],dtype=np.int64)
        self.initialTotalBoxVolume = np.sum([b[1].vol for b in self.itemBoxes],dtype=np.int64)
        self.initialTotalDeadVolume = (self.initialTotalBoxVolume - self.initialTotalItemVolume)

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
            if len(n.points) > 0:
                self.bestNodes.append((n, dV))
                if dV == 0:
                    break
        return

    def optimiseBestNodes(self):

        for n in self.bestNodes:
            for c in range(0,3):
                n[0].dim[c] = n[0].getMax(c)
        print('nodes optimised!')
        return

    # def findLargestNonEmpty(self):

    #     largest = [None, None, None]
    #     nonempty = []

    #     for n in self.tree.leaves:
    #         if len(n.points) > 0:
    #             nonempty.append(n)

    #     print(len(sorted(nonempty, key=lambda n:n.deltaV)))

    #     for d in range(0, 3):
    #         largest[d] = sorted(nonempty, key=lambda n:n.dim[d], reverse=True)[0]
    #     return largest


    def isNumPointsConst(self):

        allPoints = []

        for node in self.tree.leaves:

            allPoints += node.points
        assert len(allPoints) == len(self.tree.root.points)
        # print('✔ no points lost!')
        print('no points lost!')
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

    def writeNewBoxesCSV(self, num, path, plot=False, plotPath=None):

        print('writing new: %s' % (path))

        with open(path, 'w+') as openFile:

            for n in self.bestNodes[:num]:
                x = n[0].dim[0]
                y = n[0].dim[1]
                z = n[0].dim[2]

                line = ('KARTON %s,%s,%s,%s,\n') % (n[0].id,x,y,z)
                openFile.write(line)
            
            else:

                # end = self.tree.root
                # line = ('KARTON %s,%s,%s,%s,\n') % (end.id,end.dim[0],end.dim[1],end.dim[2])
                # openFile.write(line)

                line68 = 'KARTON 68, 1290, 600, 210,\n'
                line24 = 'KARTON 24, 1185, 600, 600,\n'
                openFile.write(line68)
                openFile.write(line24)


                # x = self.bestNodes[-1][0].dim[0]
                # y = self.bestNodes[-1][0].dim[1]
                # z = self.bestNodes[-1][0].dim[2]
                # line = ('KARTON %s,%s,%s,%s,\n') % (n[0].id,x,y,z)
                # preEnd = self.bestNodes[-1][0]
                # line = ('KARTON %s,%s,%s,%s,\n') % (preEnd.id,preEnd.dim[0],preEnd.dim[1],preEnd.dim[2])
                # openFile.write(line)

        if plot:
            if plotPath is not None:
                candidates = [n[1] for n in self.bestNodes[:num]]
                candidates.append(self.bestNodes[-1][1])
                self.writer.plot(candidates, plotPath)


    def getNewValues(self):

        self.newTotalVolume = np.sum([b[0].vol for b in self.newItemBoxes],dtype=np.int64)
        self.newTotalDeadVolume = (np.sum([b[1].vol for b in self.newItemBoxes],dtype=np.int64)
                                   - self.newTotalVolume)
        self.gain = self.newTotalDeadVolume / self.initialTotalDeadVolume

    def printInfo(self, extended=False,leaves=False ,bestN=False):

        print('Number of Points:\t\t\t%i' % len(self.itemBoxes))
        print('Dimension of Root:\t\t\t%s' % self.tree.root.dim)
        print('Initial total ItemVolume:\t%.4e' % self.initialTotalItemVolume)
        print('Initial total BoxVolume:\t%.4e' % self.initialTotalBoxVolume)
        print('Initial total DeadVolume:\t%.4e' % self.initialTotalDeadVolume)
        print('Number of Leaves:\t\t%s' % len(self.tree.leaves))

        
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
            

        if leaves:
            print('Leave Dimensions:')
            for n in self.tree.leaves:
                print(n.id, n.dim, n.lastCut)

        if len(self.bestNodes) > 0:

            print(' Leaves with deltaV gain:    %i' % (len(self.bestNodes)))
