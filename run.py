from classes.tree import TreeControl

def run():

    depth = 11
    divCrit = 0.5
    startAxis = 0
    MaxNumPoints = None
    inPath = 'assets/data_new_biggest_02.csv'
    outPath = 'assets/candidates.csv'
    plotPath = 'assets/plots/best30.jpg'

    t = TreeControl()
    t.getInitialItemBoxes(inPath, MaxNumPoints)

    t.getInitialValues()

    t.initializeTree(depth, divCrit, startAxis)
    
    p = [i[0] for i in t.itemBoxes]
    t.tree.insert(p)

    t.tree.grow(splitMode=0, dVMode=0)  
    t.isNumPointsConst()

    t.getBestNodes()
    for i in range(0, 50):
        try:
            print(t.bestNodes[i][1], t.bestNodes[i][0].dim)
        except IndexError:
            pass
    t.optimiseBestNodes()

    t.writeNewBoxesCSV(27, outPath, plot=False, plotPath=plotPath)
    t.printInfo(extended=False,leaves=False)


run()
