from typing import List

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

    def format(self):
        return self.vector
