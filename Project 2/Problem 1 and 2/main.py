import sys
sys.path.append("..")
import utils
from utils import *
from softmax_skeleton import softmaxRegression, getClassification, plotCostFunctionOverTime, computeTestError, computeTestErrorMod3, updateY
import numpy as np
import matplotlib.pyplot as plt
from features import *

# Load MNIST data:
trainX, trainY, testX, testY = getMNISTData()
# Plot the first 20 images of the training set.
plotImages(trainX[0:20,:])  


# TODO: first fill out functions in softmax_skeleton.py, or runSoftmaxOnMNIST will not work

# runSoftmaxOnMNIST: trains softmax, classifies test data, computes test error, and plots cost function
def runSoftmaxOnMNIST():
    trainX, trainY, testX, testY = getMNISTData()
    theta, costFunctionHistory = softmaxRegression(trainX, trainY, tempParameter, alpha= 0.3, lambdaFactor = 1.0e-4, k = 10, numIterations = 150)
    plotCostFunctionOverTime(costFunctionHistory)
    testError = computeTestError(testX, testY, theta, tempParameter)
    # Save the model parameters theta obtained from calling softmaxRegression to disk.
    writePickleData(theta, "./theta.pkl.gz")  
    
    # TODO: add your code here for the "Changing labels" section (7) 
    #      and print the testErrorMod3  
#    trainY, testY = updateY(trainY, testY)
#    testError = computeTestErrorMod3(testX, testY, theta, tempParameter)         
    return testError

# Don't run this until the relevant functions in softmax_skeleton.py have been fully implemented.
#print('Starting')
#tempParameter = 1
#print('testError =', runSoftmaxOnMNIST()) 


# TODO: Find the error rate for tempParameter = [.5, 1.0, 2.0]
#      Remember to return the tempParameter to 1, and re-run runSoftmaxOnMNIST
#tempParameter = 0.5
#print('testError0.5 =', runSoftmaxOnMNIST())
#tempParameter = 2.0
#print('testError2.0 =', runSoftmaxOnMNIST()) 
    
# runSoftmaxOnMNISTMod3: trains Softmax regression on digit (mod 3) classifications
def runSoftmaxOnMNISTMod3():
    trainX, trainY, testX, testY = getMNISTData()
    # Convert to mod 3
    trainY, testY = updateY(trainY, testY)
    theta, costFunctionHistory = softmaxRegression(trainX, trainY, tempParameter, alpha= 0.3, lambdaFactor = 1.0e-4, k = 10, numIterations = 150)
    plotCostFunctionOverTime(costFunctionHistory)
    testError = computeTestError(testX, testY, theta, tempParameter)
    # Save the model parameters theta obtained from calling softmaxRegression to disk.
    writePickleData(theta, "./thetaM.pkl.gz")       
    return testError

#tempParameter = 1
#print('testError =', runSoftmaxOnMNISTMod3())        
                                
######################################################
# This section contains the primary code to run when
# working on the "Using manually crafted features" part of the project.
# You should only work on this section once you have completed the first part of the project.
######################################################
## Dimensionality reduction via PCA ##

# TODO: First fill out the PCA functions in features.py as the below code depends on them.

n_components = 18
pcs = principalComponents(trainX)
train_pca = projectOntoPC(trainX, pcs, n_components)
test_pca = projectOntoPC(testX, pcs, n_components)
# train_pca (and test_pca) is a representation of our training (and test) data 
# after projecting each example onto the first 18 principal components.


# TODO: Train your softmax regression model using (train_pca, trainY) 
#       and evaluate its accuracy on (test_pca, testY).
def runSoftmaxOnMNISTPCA():
    trainX, trainY, testX, testY = getMNISTData()
    theta, costFunctionHistory = softmaxRegression(train_pca, trainY, tempParameter, alpha= 0.3, lambdaFactor = 1.0e-4, k = 10, numIterations = 150)
    plotCostFunctionOverTime(costFunctionHistory)
    testError = computeTestError(test_pca, testY, theta, tempParameter)        
    return testError
tempParameter = 1
#print('testError =', runSoftmaxOnMNISTPCA())

# TODO: Use the plotPC function in features.py to produce scatterplot 
#       of the first 100 MNIST images, as represented in the space spanned by the 
#       first 2 principal components found above.
plotPC(trainX[range(100),], pcs, trainY[range(100)])


# TODO: Use the reconstructPC function in features.py to show
#       the first and second MNIST images as reconstructed solely from 
#       their 18-dimensional principal component representation.
#       Compare the reconstructed images with the originals.
firstimage_reconstructed = reconstructPC(train_pca[0,], pcs, n_components, trainX)
plotImages(firstimage_reconstructed)
plotImages(trainX[0,]) 

secondimage_reconstructed = reconstructPC(train_pca[1,], pcs, n_components, trainX)
plotImages(secondimage_reconstructed)
plotImages(trainX[1,]) 



## Cubic Kernel ##
# TODO: Find the 10-dimensional PCA representation of the training and test set
print('Cubic bois')
n_components = 10
pcs = principalComponents(trainX)
train_pca10 = projectOntoPC(trainX, pcs, n_components)
test_pca10 = projectOntoPC(testX, pcs, n_components)

# TODO: First fill out cubicFeatures() function in features.py as the below code requires it.

print('Cubic train')
train_cube = cubicFeatures(train_pca10)
print('Cubic test')
test_cube = cubicFeatures(test_pca10)
# train_cube (and test_cube) is a representation of our training (and test) data 
# after applying the cubic kernel feature mapping to the 10-dimensional PCA representations.


# TODO: Train your softmax regression model using (train_cube, trainY) 
#       and evaluate its accuracy on (test_cube, testY).
print('Cubic softie')
def runSoftmaxOnMNISTcube():
    trainX, trainY, testX, testY = getMNISTData()
    theta, costFunctionHistory = softmaxRegression(train_cube, trainY, tempParameter, alpha= 0.3, lambdaFactor = 1.0e-4, k = 10, numIterations = 150)
    plotCostFunctionOverTime(costFunctionHistory)
    testError = computeTestError(test_cube, testY, theta, tempParameter)        
    return testError
tempParameter = 1
print('testError =', runSoftmaxOnMNISTcube())