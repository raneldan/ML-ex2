from typing import List

class digits_classfier:
    def __init__(self):
        self.classifiers: List = []
        self.result = []
        self.__init_classifiers()
        for classifier in self.classifiers:
            self.result.append(classifier())

    def __init_classifiers(self,):
        self.classifiers.append(self.classifier_0)
        self.classifiers.append(self.classifier_1)
        self.classifiers.append(self.classifier_2)
        self.classifiers.append(self.classifier_3)
        self.classifiers.append(self.classifier_4)
        self.classifiers.append(self.classifier_5)
        self.classifiers.append(self.classifier_6)
        self.classifiers.append(self.classifier_7)
        self.classifiers.append(self.classifier_8)
        self.classifiers.append(self.classifier_9)