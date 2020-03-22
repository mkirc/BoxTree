from classes.tree import *

def run():

    depth = 13
    divCrit = 0.5
    startAxis = 0
    numPoints = 47287
    newPath = 'assets/new_boxes_86.csv'

    t = TreeControl()
    t.getInitialItemBoxes('assets/raw_data_01.csv')
    t.getInitialValues()

    t.initializeTree(depth, divCrit, startAxis)
    p = [i[0] for i in t.itemBoxes]
    t.tree.insert(p[0:numPoints])


    t.tree.grow()

    # sanity check  
    t.isNumPointsConst()

    t.getBestNodes()

    t.writeOutNewItemBoxes(newPath)

    t.getNewItemBoxes(newPath)
    t.getNewValues()

    t.printInfo(numPoints, bestN=True)


run()
