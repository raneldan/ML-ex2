from typing import List

dimension = 28

class PicToVec:
    def __init__(self, pic: List[int]):
        self.pic: List[int] = pic
        self.funcs: List = []
        self.vector = []
        self.__init_funcs()
        for func in self.funcs:
            self.vector.append(func())

    def __init_funcs(self,):
        self.funcs.append(self.sum_of_values)
        self.funcs.append(self.num_of_pixels)
        self.funcs.append(self.symmetry_x)
        self.funcs.append(self.symmetry_y)

    def sum_of_values(self) -> int:
        sum = 0
        for cell in self.pic:
            sum += cell
        return sum

    def num_of_pixels(self) -> int:
        counter = 0
        for cell in self.pic:
            if (cell != 0):
                counter += 1
        return counter

    def symmetry_x(self):
        score = 0
        for index, cell in enumerate(self.pic):
            if (index % dimension < dimension / 2):
                if (cell != 0 and cell == self.pic[index+ int(dimension/2)]):
                    score += 1
        return score

    def symmetry_y(self):
        score = 0
        for index, cell in enumerate(self.pic):
            if index < dimension * dimension / 2:
                if cell != 0 and cell == self.pic[self.calc_y_position(index)]:
                    score += 1
        return score

    def calc_y_position(self, index):
        return (index % dimension) + ((dimension - int(index/dimension) - 1) * dimension)

    def format(self):
        return self.vector
