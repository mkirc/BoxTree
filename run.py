from classes.tree import TreeControl

def run():

    depth = 13
    divCrit = 0.5
    startAxis = 0
    MaxNumPoints = None
    inPath = 'assets/1M_old.csv'
    outPath = 'assets/candidates.csv'
    plotPath = 'assets/plots/best30.jpg'

    t = TreeControl()
    t.getInitialItemBoxes(inPath, MaxNumPoints)

    t.getInitialValues()

    t.initializeTree(depth, divCrit, startAxis)
    
    p = [i[0] for i in t.itemBoxes]
    t.tree.insert(p)

    t.tree.grow()

    # sanity check  
    t.isNumPointsConst()

    t.getBestNodes()

    t.writeNewBoxesCSV(30, outPath)

    t.printInfo(extended=False,leaves=False)
    # t.plotBest(30, plotPath)


run()
