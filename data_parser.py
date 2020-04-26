import csv
from mnist import MNIST
from digits_classifyer import classify_digits, check_classification
from pic_to_vector import PicToVec
import run_perceptron
from typing import List
import numpy as np
import struct as st
import matplotlib.pyplot as plt
from skimage import img_as_bool
from skimage.color import rgb2gray
from skimage.morphology import skeletonize, binary_closing
import os
import tensorflow as tf
from skimage.filters import threshold_otsu

def get_binary(img):
    thresh = threshold_otsu(img)
    binary = img > thresh
    return binary

train_features_file_name = 'features/train_images.csv'
backup_train_features_file_name = 'features/backup_train_images.csv'
test_features_file_name = 'features/test_images.csv'
backup_test_features_file_name = 'features/backup_test_images.csv'

train_tags_file_name = "tags/train_tags"
test_tags_file_name = "tags/test_tags"

mndata = MNIST('data')

(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data(path = 'data')

def uploadData(filename , text):
    train_imagesfile = open(filename[text], 'rb')
    train_imagesfile.seek(0)
    magic = st.unpack('>4B', train_imagesfile.read(4))
    nImg = st.unpack('>I', train_imagesfile.read(4))[0]  # num of images
    nR = st.unpack('>I', train_imagesfile.read(4))[0]  # num of rows
    nC = st.unpack('>I', train_imagesfile.read(4))[0]  # num of column
    nBytesTotal = nImg * nR * nC * 1  # since each pixel data is 1 byte
    images_array = 255 - np.asarray(st.unpack('>' + 'B' * nBytesTotal, train_imagesfile.read(nBytesTotal))).reshape((nImg, nR, nC))
    return images_array

filename = {'images' : 'data/train-images-idx3-ubyte' ,'test' : 'data/t10k-images-idx3-ubyte'}
train_images = uploadData(filename , 'images')
test_images = uploadData(filename , 'test')

# im = rgb2gray(images_array[0])
# bin = get_binary(im)
# out = binary_closing(skeletonize(bin))

# f, (ax0, ax1) = plt.subplots(1, 2)
# ax0.imshow(im, cmap='gray', interpolation='nearest')
# ax1.imshow(out, cmap='gray', interpolation='nearest')
# plt.show()

USE_BACKUP = False


def write_feature_to_file(filename: str, is_backup: bool, images):
    with open(filename, 'w', newline='', encoding='utf-8') as csvoutForFeatures1:
        csvoutForFeatures = csv.writer(csvoutForFeatures1)
        for i in range(len(images)):

            if is_backup:
                pic = PicToVec(images[i], [0, 1, 3, 4])
                var = pic.back_up_format()
            else:
                im = rgb2gray(images[i])
                bin = get_binary(im)
                skel = skeletonize(bin)
                out = binary_closing(skel)
                out = out.astype(int)
                vec = out.flatten()
                pic = PicToVec(vec)
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
