from classes.tree import TreeControl

def run():

    depth = 2
    divCrit = 0.5
    startAxis = 0
    MaxNumPoints = 10
    newPath = 'assets/new_boxes.csv'

    t = TreeControl()
    t.getInitialItemBoxes('assets/1M_old.csv', MaxNumPoints)

    t.getInitialValues()

    t.initializeTree(depth, divCrit, startAxis)
    
    p = [i[0] for i in t.itemBoxes]
    t.tree.insert(p)

    t.tree.grow()

    # sanity check  
    t.isNumPointsConst()

    t.getBestNodes()

    t.writeOutNewItemBoxes(newPath)

    t.getNewItemBoxes(newPath)
    t.getNewValues()

    t.printInfo(bestN=True)


run()
