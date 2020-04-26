import csv
from mnist import MNIST
from digits_classifyer import classify_digits, check_classification
from pic_to_vector import PicToVec
import os
import run_perceptron
from typing import List

train_features_file_name = 'features/train_images.csv'
backup_train_features_file_name = 'features/backup_train_images.csv'
test_features_file_name = 'features/test_images.csv'
backup_test_features_file_name = 'features/backup_test_images.csv'

train_tags_file_name = "tags/train_tags"
test_tags_file_name = "tags/test_tags"

mndata = MNIST('data')

train_images, train_labels = mndata.load_training()

test_images, test_labels = mndata.load_testing()

USE_BACKUP = True


def write_feature_to_file(filename: str, is_backup: bool, images):
    with open(filename, 'w', newline='', encoding='utf-8') as csvoutForFeatures1:
        csvoutForFeatures = csv.writer(csvoutForFeatures1)
        for i in range(len(images)):

            if is_backup:
                pic = PicToVec(images[i], [0])
                var = pic.back_up_format()
            else:
                pic = PicToVec(images[i])
                var = pic.format()

            csvoutForFeatures.writerow(var)
            csvoutForFeatures1.flush()


def build_features(use_backup: bool = False):
    files_to_remove = [os.path.join('features', f) for f in os.listdir('features')]
    for f in files_to_remove:
        os.remove(f)
    write_feature_to_file(train_features_file_name, images=train_images, is_backup=False)
    write_feature_to_file(test_features_file_name, images=test_images, is_backup=False)
    if use_backup:
        write_feature_to_file(backup_train_features_file_name, images=train_images, is_backup=True)
        write_feature_to_file(backup_test_features_file_name, images=test_images, is_backup=True)


def build_tags(use_backup: bool = False):
    predictions_results: List[List[bool]] = []
    backup_predictions_results: List[List[bool]] = []
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
                tag_to_write = (1 if label == i else 0).__str__()
                csvoutForTrainTags.writerow(tag_to_write)
                csvoutForTrainTags1.flush()
            counter = 0
            for label in test_labels:
                counter += 1
                tag_to_write = (1 if label == i else 0).__str__()
                csvoutForTestTags.writerow(tag_to_write)
                csvoutForTestTags1.flush()
        print("Sucsses rate for digit ", i)

        restult_list = []
        predictions_results.append(
            run_perceptron.run(train_features_file_name, train_tags_file, test_features_file_name, test_tags_file))
        if use_backup:
            backup_predictions_results.append(
                run_perceptron.run(backup_train_features_file_name, train_tags_file, backup_test_features_file_name,
                                   test_tags_file))
    check_classification(
        classify_digits(binary_classification_results=predictions_results,
                        backup_binary_classification_results=backup_predictions_results),
        list(test_labels))


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


if __name__ == '__main__':
    build_features(USE_BACKUP)
    build_tags(USE_BACKUP)
