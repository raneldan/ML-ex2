from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import numpy as np
from perceptron_algo import Perceptron

from typing import List, Tuple


def to_np_num(list_of_str):
    temp = np.array(list_of_str)
    ans = temp.astype(np.float)
    return ans


def run(features_file_name, tags_file_name, test_file_name, test_tags_file_name) -> List[bool]:
    features_file = open(features_file_name, 'r', encoding="utf8")
    lines = features_file.read().splitlines()
    training_inputs = list(map(lambda line: list(line.split(",")), lines))

    tags_file = open(tags_file_name, 'r', encoding="utf8")
    labels = tags_file.read().splitlines()
    labels = list(map(lambda line: list(line.split(",")), labels))

    test_file = open(test_file_name, 'r', encoding="utf8")
    test = test_file.read().splitlines()
    test = list(map(lambda line: list(line.split(",")), test))

    test_tags_file = open(test_tags_file_name, 'r', encoding="utf8")
    test_tags = test_tags_file.read().splitlines()
    test_tags = list(map(lambda line: list(line.split(",")), test_tags))

    # train, test, train_tags, test_tags = model_selection.train_test_split(training_inputs, labels, test_size=0.3)
    num_of_features = len(training_inputs[0])

    # training_inputs = [float(x) for x in training_inputs.split(',')]
    # test = [float(x) for x in test.split(',')]

    train = np.array(list(map((lambda line: to_np_num(line)), training_inputs)))
    test = np.array(list(map((lambda line: to_np_num(line)), test)))

    Encoder = LabelEncoder()
    train_tags = Encoder.fit_transform(labels)
    test_tags = Encoder.fit_transform(test_tags)

    perceptron = Perceptron(num_of_features)
    perceptron.train(train, np.array(train_tags))
    predictions_perceptron: List[bool] = list()
    for vec in test:
        p = perceptron.predict(vec)
        predictions_perceptron.append(p)

    # print("Perceptron Accuracy Score -> ", accuracy_score(predictions_perceptron, test_tags) * 100)
    result = accuracy_score(predictions_perceptron, test_tags) * 100
    print(result)
    return predictions_perceptron
