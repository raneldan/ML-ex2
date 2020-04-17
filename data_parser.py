import csv
from mnist import MNIST
from pic_to_vector import PicToVec
import os
import run_perceptron

train_features_file_name = 'features/train_images.csv'
test_features_file_name = 'features/test_images.csv'

mndata = MNIST('data')

train_images, train_labels = mndata.load_training()

test_images, test_labels = mndata.load_testing()

filesToRemove = [os.path.join('features', f) for f in os.listdir('features')]
for f in filesToRemove:
    os.remove(f)

with open(train_features_file_name, 'w', newline='', encoding='utf-8') as csvoutForTrainFeatures,\
     open(test_features_file_name, 'w', newline='', encoding='utf-8') as csvoutForTestFeatures:
    csvoutForTrainFeatures = csv.writer(csvoutForTrainFeatures)
    csvoutForTestFeatures = csv.writer(csvoutForTestFeatures)
    for i in train_images:
        csvoutForTrainFeatures.writerow(PicToVec(i).format())
    for i in test_images:
        csvoutForTestFeatures.writerow(PicToVec(i).format())

    #run_perceptron.run(train_features_file_name, test_features_file_name)

