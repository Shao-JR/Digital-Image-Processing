"""
... is the place where you need to fill in
"""
# This line is to re-install OpenCV, since the default version of OpenCV in Colab doesn't contain SIFT alorithm.
# After re-installing OpenCV, you need to restart Runtime of Colab. Then you can use the new version.
from tqdm import tqdm
import os
from cv2 import *
import numpy as np
from sklearn import svm
import pickle

def calcSiftFeature(img, idx):

    # create a SIFT function
    sift = cv2.xfeatures2d.SIFT_create()

    ###########################################################
    """
    Please use the sift.detectAndCompute to compute the SIFT feature.
    You can refer to https://docs.opencv.org/4.x/da/df5/tutorial_py_sift_intro.html
    """
    keypoints, features = sift.detectAndCompute(img, None)
    ###########################################################

    if idx == 0:
        draw_keyPoint(img, keypoints)

    return features

def draw_keyPoint(img, kp):
    """
        This function draw the key-points of SIFT Detection given an image.
    """
    kp_image = cv2.drawKeypoints(img, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('Original', cv2.resize(img, (150,150)))
    cv2.imshow('SIFT Keypoints', cv2.resize(kp_image, (150,150)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def learnVocabulary(features, wordCnt=50):
    """
    This function use the K-Means algorithm to create a dictionary for training images.
    """

    #set a criteria for stopping the iteration of K-Means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.1)

    #Initialize the centroids
    flags = cv2.KMEANS_RANDOM_CENTERS

    ###########################################################
    """    
    Please use cv2.kmeans to conduct K-Means algorithm.
    You can refer to https://docs.opencv.org/4.x/d5/d38/group__core__cluster.html#gga276000efe55ee2756e0c471c7b270949a78ddd00a99cd51db10ed63c024eb1e62
    Note that wordCnt represents that cluster number, which should be the input of cv2.kmeans 
    """
    compactness, labels, centers = cv2.kmeans(
        features,
        wordCnt,
        None,
        criteria,
        10,
        flags
    )
    ###########################################################
    return centers


def calcFeatVec(features, centers, wordCnt=50):
    """
    This function is to caculate the feature for each image represented by the obtained dictionary
    """
    featVec = np.zeros((1, wordCnt))

    for i in range(0, features.shape[0]):
        fi = features[i]

        #calculate the distance between the feature and each centroids
        diffMat = np.tile(fi, (wordCnt, 1)) - centers
        sqSum = (diffMat**2).sum(axis=1)
        dist = sqSum**0.5

        # sort the distance with ascending order
        sortedIndices = dist.argsort()

        #find the minimum
        idx = sortedIndices[0]

        # add the corresponding value in the feature vector
        featVec[0][idx] += 1
    return featVec


def build_center(train_imgs):
    """
    This function is to building a dictionary based on training set.
    """

    features = np.float32([]).reshape(0, 128)

    for idx in tqdm(range(len(train_imgs))):

        train_img = train_images[idx]
        ###########################################################
        """
        calculating features for a training image
        You need to complete the code of function calcSiftFeature
        """
        img_f = calcSiftFeature(train_img, idx)
        ###########################################################

        if img_f is not None:
            features = np.append(features, img_f, axis=0)

    ###########################################################
    """    
    Building a dictionary by K-means algorithm 
    You need to complete the code of function learnVocabulary
    """
    centers = learnVocabulary(features)
    ###########################################################

    #save the created dictionary
    filename = "./svm_centers.npy"
    np.save(filename, centers)

    print('Dictionary:', centers.shape)


def cal_vec(imgs, labels, wordCnt=50):
    """
    This function is to calculate SIFT features for the given images
    """

    centers = np.load("./svm_centers.npy")
    data_vec = np.float32([]).reshape(0, wordCnt)
    return_labels = np.float32([])

    for idx in range(len(imgs)):
            img = imgs[idx]
            label = labels[idx]
            img_f = calcSiftFeature(img, idx)
            if img_f is not None:
                # caculating the feature for each image represented by the obtained dictionary
                img_vec = calcFeatVec(img_f, centers)
                data_vec = np.append(data_vec,img_vec,axis=0)
                return_labels = np.append(return_labels, label)

    print('image features vector done!')

    return data_vec, return_labels


def SVM_Train(data_vec,labels):
    """
    This function is to train a SVM classifier
    """

    ###########################################################
    """
    Please use svm.SVC to Build a SVM classifier. 
    You can refer to https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html. 
    """
    clf = svm.SVC(kernel='linear', C=1.0)
    ###########################################################

    # Using the input feature and labels, train a SVM classifier.
    clf.fit(data_vec,labels)

    # Save a trained SVM model
    pick_save = open('./svm_model.m','wb')
    pickle.dump(clf, pick_save)
    pick_save.close()


def SVM_Test(test_images, test_labels):

    # Loading the trained SVM classifier
    pick_read = open('./svm_model.m','rb')
    clf = pickle.load(pick_read)
    pick_read.close()

    # Extract SIFT features for testing images
    data_vec, labels = cal_vec(test_images, test_labels)

    # Conduct the prediction using the trained SVM classifier
    res = clf.predict(data_vec)

    # Collect the testing results
    num_test = data_vec.shape[0]

    acc = 0
    for i in range(num_test):
        if labels[i] == res[i]:
            acc = acc+1

    return acc/num_test,res


def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict


###########################################################
"""
For preparing a training set and a testing set.
You need to download the CIFAR dataset from https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
and put the extracted files in a folder named cifar-10-batches-py. 
"""
root = "./cifar-10-batches-py"
data_list = ["data_batch_1", "data_batch_2", "data_batch_3", "data_batch_4", "data_batch_5", "test_batch"]

images = []
labels = []
selected_class = [0, 1]

for data_name in data_list:
    data_path = os.path.join(root, data_name)
    data_dict = unpickle(data_path)
    data = data_dict[b"data"]
    data_label = data_dict[b"labels"]

    interval = int(data.shape[1]/3)
    width = 32
    length = 32

    for index in range(data.shape[0]):

        one_image = data[index]

        R = one_image[0:interval].reshape(width, length)
        G = one_image[interval:2*interval].reshape(width, length)
        B = one_image[2*interval:].reshape(width, length)

        R = np.expand_dims(R, axis=2)
        G = np.expand_dims(G, axis=2)
        B = np.expand_dims(B, axis=2)

        img = np.concatenate((R,G,B), axis=2)

        if data_label[index] in selected_class:
            images.append(img)
            labels.append(data_label[index])

train_images = images[:10000]
train_labels = labels[:10000]
test_images = images[10000:]
test_labels = labels[10000:]
###########################################################

###########################################################
"""
Building a dictionary based on the training images, and you need to complete the code of build_center.
Please refer to the function above for details.
"""
build_center(train_images)
###########################################################

# Constructing the feature set for training set.
training_features, training_labels = cal_vec(train_images, train_labels)

###########################################################
"""
Train a SVM classifier, you need to complete the code of SVM_Train.
Please refer to the function above for details.
"""
SVM_Train(training_features, training_labels)
###########################################################

acc, res = SVM_Test(test_images, test_labels)

print("Accuracy: " + str(acc))