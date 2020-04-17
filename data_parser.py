import csv
from mnist import MNIST
from pic_to_vector import PicToVec
import os
import glob

mndata = MNIST('data')

train_images, train_labels = mndata.load_training()

test_images, test_labels = mndata.load_testing()

files = glob.glob('/features')
for f in files:
    os.remove(f)

with open('features/train_images.csv', 'w', newline='', encoding='utf-8') as csvoutForFeatures:
    csvoutForFeatures = csv.writer(csvoutForFeatures)
    for i in train_images:
        csvoutForFeatures.writerow(PicToVec(i).format())
