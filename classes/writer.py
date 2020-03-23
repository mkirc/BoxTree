
# import matplotlib.pyplot as plt

class Writer():

    def __init__(self):

        pass

    # def plot(self, nodeVolList, path, show=False):

    #         fig, ax = plt.subplots()
    #         ax.plot(nodeVolList, marker='x')
    #         ax.set_xlabel('index in Treecontrol.bestNodes')
    #         ax.set_ylabel('Node.deltaV')
    #         # ax.set_yscale('log')
    #         if show:
    #             plt.show()
    #         else:
    #             plt.savefig(path)

    def write(self, path, bestNodesCopy, leaves):
        '''conceptually wrong, should be avoided'''

        with open(path, 'w+') as openFile:
            for l in leaves:

                if l.id < bestNodesCopy[0][0]:

                    kNom = 'KARTON' + ' ' + str(bestNodesCopy[0][0])
                    kDimX = bestNodesCopy[0][1].dim[0]
                    kDimY = bestNodesCopy[0][1].dim[1]
                    kDimZ = bestNodesCopy[0][1].dim[2]

                    for point in l.points:

                        pDimX = point.dim[0]
                        pDimY = point.dim[1]
                        pDimZ = point.dim[2]

                        line = '%s,%s,%s,%s,%s,%s,%s,\n' % (
                            kNom, kDimX, kDimY, kDimZ, pDimX, pDimY, pDimZ)

                        openFile.write(line)

                elif l.id == bestNodesCopy[0][0]:

                    kNom = 'KARTON' + ' ' + str(bestNodesCopy[0][0])
                    kDimX = bestNodesCopy[0][1].dim[0]
                    kDimY = bestNodesCopy[0][1].dim[1]
                    kDimZ = bestNodesCopy[0][1].dim[2]

                    for point in l.points:

                        pDimX = point.dim[0]
                        pDimY = point.dim[1]
                        pDimZ = point.dim[2]

                        line = '%s,%s,%s,%s,%s,%s,%s,\n' % (
                            kNom, kDimX, kDimY, kDimZ, pDimX, pDimY, pDimZ)

                        openFile.write(line)

                    lastNode = bestNodesCopy.pop(0)
                    # print('last Node: %s. Only %s to go!' % (lastNode[0], len(self.bestNodes)))
            else:

                # print('✔ finished writing %s' % (path))
                print('finished writing %s' % (path))
                print('')
                return


