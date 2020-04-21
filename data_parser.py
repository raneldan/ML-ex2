import csv
from mnist import MNIST
from pic_to_vector import PicToVec
import os
import run_perceptron


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


train_features_file_name = 'features/train_images.csv'
test_features_file_name = 'features/test_images.csv'
train_tags_file_name = "tags/train_tags"
test_tags_file_name = "tags/test_tags"

mndata = MNIST('data')

train_images, train_labels = mndata.load_training()

test_images, test_labels = mndata.load_testing()

filesToRemove = [os.path.join('features', f) for f in os.listdir('features')]
for f in filesToRemove:
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
                if i == 8:
                    if label != i:
                        csvoutForTrainTags.writerow("1")
                    else:
                        csvoutForTrainTags.writerow("0")
                else:
                    if label == i:
                        csvoutForTrainTags.writerow("1")
                    else:
                        csvoutForTrainTags.writerow("0")
                csvoutForTrainTags1.flush()
            print(counter)
            assert_number_of_lines(counter, train_tags_file)

            for label in test_labels:
                if i == 8:
                    if label != i:
                        csvoutForTestTags.writerow("1")
                    else:
                        csvoutForTestTags.writerow("0")
                else:
                    if label == i:
                        csvoutForTestTags.writerow("1")
                    else:
                        csvoutForTestTags.writerow("0")
                csvoutForTestTags1.flush()
            assert_number_of_lines(len(test_labels), test_tags_file)
        print("Sucsses rate for digit ", i)
        run_perceptron.run(train_features_file_name, train_tags_file, test_features_file_name, test_tags_file)