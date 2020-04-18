import csv
from mnist import MNIST
from pic_to_vector import PicToVec
import os
import run_perceptron

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

with open(train_features_file_name, 'w', newline='', encoding='utf-8') as csvoutForTrainFeatures, \
         open(test_features_file_name, 'w', newline='', encoding='utf-8') as csvoutForTestFeatures:
    csvoutForTrainFeatures = csv.writer(csvoutForTrainFeatures)
    csvoutForTestFeatures = csv.writer(csvoutForTestFeatures)
    for i in train_images:
        csvoutForTrainFeatures.writerow(PicToVec(i).format())
    for i in test_images:
        csvoutForTestFeatures.writerow(PicToVec(i).format())
    for i in range(0, 10):
        train_tags_file = train_tags_file_name + i.__str__() + '.csv'
        test_tags_file = test_tags_file_name + i.__str__() + '.csv'
        with open(train_tags_file, 'w', newline='', encoding='utf-8') as csvoutForTrainTags, \
                open(test_tags_file, 'w', newline='',encoding='utf-8') as csvoutForTestTags:
            csvoutForTrainTags = csv.writer(csvoutForTrainTags)
            csvoutForTestTags = csv.writer(csvoutForTestTags)
            for label in train_labels:
                if label == i:
                    csvoutForTrainTags.writerow("1")
                else:
                    csvoutForTrainTags.writerow("0")
            for label in test_labels:
                if label == i:
                    csvoutForTestTags.writerow("1")
                else:
                    csvoutForTestTags.writerow("0")
        run_perceptron.run(train_features_file_name, train_tags_file, test_features_file_name, test_tags_file)



