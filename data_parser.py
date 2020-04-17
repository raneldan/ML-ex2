from mnist import MNIST
from pic_to_vector import PicToVec

mndata = MNIST('data')

train_images, train_labels = mndata.load_training()

test_images, test_labels = mndata.load_testing()
for i in train_images:
    print(PicToVec(i).format())