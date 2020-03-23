import itertools
import math
class Item:

    def __init__(self, dim, pos=[0,0,0], name=None):

        self.dimension = sorted(dim,reverse=True)
        self.pos = pos

        # cryptische größenangabe
        self.size = sum(self.dimension)
        self.length = math.sqrt(sum(i**2 for i in self.dimension))

        self.name = name

        
        self.volume = dim[0]*dim[1]*dim[2]
        self.surface = 2 * (dim[0] * dim[1]) + 2 * (dim[0] * dim[2] ) + 2 * (dim[1] * dim[2])

        self.comp = self.volume/self.surface
        

    def __str__(self):

        return str(self.dimension) + ' item at' + str(self.pos)

    # check if a other item fits into this item
    def __le__(self, other):

        for i in range(3):
            if self.dimension[i] > other.dimension[i]:
                return False
        return True

    def __lt__(self, other):
        return self.size > other.size

    # subtrac other from self resulting in a list of items(spaces) left in self
    def __sub__(self, other):
        spaces = []

        x_off = abs(self.pos[0] - other.pos[0])
        y_off = abs(self.pos[1] - other.pos[1])
        z_off = abs(self.pos[2] - other.pos[2])

        x = self.dimension[0] - other.dimension[0]
        y = self.dimension[1] - other.dimension[1]
        z = self.dimension[2] - other.dimension[2]

        # SUB LEADS TO WRONG POS OF REST WEEN NOT SUBBING FROM 0,0,0
        # if positions are equal
        # print('-')

        if x > 0:
            if x_off > 0:
                spaces.append(
                    Item([x_off, self.dimension[1], self.dimension[2]], self.pos))

            else:
                spaces.append(Item([x, self.dimension[1], self.dimension[2]], [
                              self.pos[0] + other.dimension[0], self.pos[1], self.pos[2]]))

        if y > 0:
            if y_off > 0:
                spaces.append(
                    Item([self.dimension[0], y_off, self.dimension[2]], self.pos))

            else:
                spaces.append(Item([self.dimension[0], y, self.dimension[2]], [
                              self.pos[0], self.pos[1] + other.dimension[1], self.pos[2]]))

        if z > 0:
            if z_off > 0:
                spaces.append(
                    Item([self.dimension[0], self.dimension[1], z_off], self.pos))

            else:
                spaces.append(Item([self.dimension[0], self.dimension[1], z], [
                              self.pos[0], self.pos[1], self.pos[2] + other.dimension[2]]))

        # self.rest = spaces
        #print([str(i) for i in spaces])

        return spaces

    def isOverlapping(self, i, o):
        # print('over')
        dx = min(i.pos[0] + i.dimension[0], o.pos[0] +
                 o.dimension[0]) - max(i.pos[0], o.pos[0])
        dy = min(i.pos[1] + i.dimension[1], o.pos[1] +
                 o.dimension[1]) - max(i.pos[1], o.pos[1])
        dz = min(i.pos[2] + i.dimension[2], o.pos[2] +
                 o.dimension[2]) - max(i.pos[2], o.pos[2])
        if (dx > 0) and (dy > 0) and (dz > 0):
            pos = [max(i.pos[0], o.pos[0]), max(
                i.pos[1], o.pos[1]), max(i.pos[2], o.pos[2])]
            return Item([dx, dy, dz], pos)

    def fit(self, other):
        x = self.dimension[0] - other.dimension[0]
        y = self.dimension[1] - other.dimension[1]
        z = self.dimension[2] - other.dimension[2]
        return abs(x * y * z)

    def rotations(self):

        return [Item(i, self.pos, name=self.name) for i in list(itertools.permutations(self.dimension))]
