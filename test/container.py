# from item import Item
# import numpy

class Container:

    def __init__(self, dim):

        self.items = []
        # self.spaces = []
        self.dimension = sorted(dim,reverse=True)
        self.name = ''
        # print(self.name)
        # print(self.dimension)
        self.volume = dim[0]*dim[1]*dim[2]


    def __str__(self):
        return str(self.dimension) + ' ' +str(self.name)
    def log(self):
        return f'{self.name}, {self.dimension[0]}, {self.dimension[1]}, {self.dimension[2]}, {len(self.items)}, {self.volume}'

    def fit(self, item):
        for i in range(3):            
            if self.dimension[i] <= item.dimension[i]:
                return False
        return True