from typing import List
import numpy as np


dimension = 28
treshold = 10

class PicToVec:
    def __init__(self, pic: List[int]):
        self.pic: List[int] = pic
        self.funcs: List = []
        self.vector = []
        self.__init_funcs()
        for func in self.funcs:
            result = func()
            for value in result:
                self.vector.append(value)

    def __init_funcs(self,):
        self.funcs.append(self.num_of_pixels)
        self.funcs.append(self.symmetry_x)
        self.funcs.append(self.symmetry_y)
        self.funcs.append(self.symmetry_cross)
        self.funcs.append(self.min_width)
        self.funcs.append(self.max_width)
        self.funcs.append(self.distance_from_row_start)

    def num_of_pixels(self) -> int:
        counter = 0
        for cell in self.pic:
            if cell != 0:
                counter += 1
        return [counter]

    def symmetry_x(self):
        score = 0
        for index, cell in enumerate(self.pic):
            if (index % dimension) < dimension / 2:
                if cell != 0 and abs(cell - self.pic[index + int(dimension/2)]) < treshold:
                    score += 1
        return [score]

    def symmetry_y(self):
        score = 0
        for index, cell in enumerate(self.pic):
            if index < dimension * dimension / 2:
                if cell != 0 and abs(cell - self.pic[self.calc_y_position(index)]) < treshold:
                    score += 1
        return [score]

    def symmetry_cross(self):
        score = 0
        for index, cell in enumerate(self.pic):
            if index < dimension * dimension / 2:
                if cell != 0 and abs(cell - self.pic[dimension * dimension - index]) < treshold:
                    score += 1
        return [score]

    def min_width(self):
        pic = np.reshape(self.pic, (-1, dimension))
        min_width = dimension
        for row in pic:
            left_index = np.min(np.nonzero(row)) if np.nonzero(row)[0].size > 0 else 0
            right_index = np.max(np.nonzero(row)) if np.nonzero(row)[0].size > 0 else 0
            row_width = right_index - left_index if left_index != 0 and right_index != 0 else dimension
            min_width = min(min_width, row_width)
        return [min_width]

    def max_width(self):
        pic = np.reshape(self.pic, (-1, dimension))
        max_width = 0
        for row in pic:
            left_index = np.min(np.nonzero(row)) if np.nonzero(row)[0].size > 0 else 0
            right_index = np.max(np.nonzero(row)) if np.nonzero(row)[0].size > 0 else 0
            row_width = right_index - left_index
            max_width = max(max_width, row_width)
        return [max_width]

    def distance_from_row_start(self):
        pic = np.reshape(self.pic, (-1, dimension))
        distances = []
        for row in pic:
            distances.append(np.min(np.nonzero(row)) if np.nonzero(row)[0].size > 0 else 0)
        maximum = max(distances)
        minimum = min(distances)
        diff = []
        for index, value in enumerate(distances):
            if index == 0:
                diff.append(value)
            else:
                diff.append(value-diff[index-1])
        for diff_value in diff:
            distances.append(diff_value)
        distances.append(maximum)
        distances.append(minimum)
        return distances


    def calc_y_position(self, index):
        return (index % dimension) + ((dimension - int(index/dimension) - 1) * dimension)

    def format(self):
        return self.vector
