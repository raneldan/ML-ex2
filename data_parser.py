import csv
from mnist import MNIST
from digits_classifyer import classify_digits, check_classification
from pic_to_vector import PicToVec
import os
import run_perceptron
from typing import List


train_features_file_name = 'features/train_images.csv'
test_features_file_name = 'features/test_images.csv'
train_tags_file_name = "tags/train_tags"
test_tags_file_name = "tags/test_tags"

mndata = MNIST('data')

train_images, train_labels = mndata.load_training()

test_images, test_labels = mndata.load_testing()

predictions_results: List[List[bool]] = []


def build_features():
    files_to_remove = [os.path.join('features', f) for f in os.listdir('features')]
    for f in files_to_remove:
        os.remove(f)
    with open(train_features_file_name, 'w', newline='', encoding='utf-8') as csvoutForTrainFeatures1, \
            open(test_features_file_name, 'w', newline='', encoding='utf-8') as csvoutForTestFeatures1:
        csvoutForTrainFeatures = csv.writer(csvoutForTrainFeatures1)
        csvoutForTestFeatures = csv.writer(csvoutForTestFeatures1)
        for i in range(len(train_images)):
            var = PicToVec(train_images[i]).format()
            csvoutForTrainFeatures.writerow(var)
            csvoutForTrainFeatures1.flush()
        for i in range(len(test_images)):
            var = PicToVec(test_images[i]).format()
            csvoutForTestFeatures.writerow(var)
            csvoutForTestFeatures1.flush()


def build_tags():
    for i in range(0, 10):
        train_tags_file = train_tags_file_name + i.__str__() + '.csv'
        test_tags_file = test_tags_file_name + i.__str__() + '.csv'
        with open(train_tags_file, 'w', newline='', encoding='utf-8') as csvoutForTrainTags1, \
                open(test_tags_file, 'w', newline='', encoding='utf-8') as csvoutForTestTags1:
            csvoutForTrainTags = csv.writer(csvoutForTrainTags1)
            csvoutForTestTags = csv.writer(csvoutForTestTags1)
            counter = 0
            for label in train_labels:
                counter += 1
                tag_to_write = 1 if label == i else 0
                csvoutForTrainTags.writerow(tag_to_write)
                csvoutForTrainTags1.flush()
            counter = 0
            for label in test_labels:
                counter += 1
                tag_to_write = 1 if label == i else 0
                csvoutForTestTags.writerow(tag_to_write)
                csvoutForTestTags1.flush()
        print("Sucsses rate for digit ", i)
        predictions_results.append(
            run_perceptron.run(train_features_file_name, train_tags_file, test_features_file_name, test_tags_file))
    check_classification(classify_digits(predictions_results), list(test_labels))


def assert_number_of_lines(number_of_lines, file_path):
    with open(file_path, 'r') as file:
        counter = 0
        content = file.read()
        coList = content.split('\n')
        for i in coList:
            if i:
                counter += 1
        print(counter)
        assert (counter == number_of_lines)


build_features()
build_tags()
