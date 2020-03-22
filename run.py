from classes.tree import TreeControl

def run():

    depth = 13
    divCrit = 0.5
    startAxis = 0
    MaxNumPoints = None
    newPath = 'assets/new_boxes.csv'

    t = TreeControl()
    t.getInitialItemBoxes('assets/47k.csv', MaxNumPoints)

    t.getInitialValues()

    t.initializeTree(depth, divCrit, startAxis)
    
    p = [i[0] for i in t.itemBoxes]
    t.tree.insert(p)

    t.tree.grow()

    # sanity check  
    t.isNumPointsConst()

    t.getBestNodes()

    # t.writeOutNewItemBoxes(newPath)
    t.writeNewBoxesCSV(newPath)

    # t.getNewItemBoxes(newPath)
    # t.getNewValues()

    t.printInfo(extended=False, bestN=True)


run()
