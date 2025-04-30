import numpy as np

class Node:
    
    def __init__(self, feature = None, threshold = None, left = None, right = None, *, value = None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value 

    def isLeaf(self):
        return self.value is not None
    

class DecisionTree:

    def __init__(self, minSamples = 2, maxDepth = 100, numFeatures = None):
        self.minSamples = minSamples
        self.maxDepth = maxDepth
        self.numFeatures = numFeatures
        self.root = None

    def fit(self, X, y):

        #if numFeatures is equal to None, use all features in X.shape[1]
        #else, use the minimum number of features in the data and numFeatures
        self.numFeatures = X.shape[1] if not self.numFeatures else min(X.shape[1], self.numFeatures)
        #initialtes the growTree method
        self.root = self.growTree(X, y)

    def growTree(self, X, y, depth=0):
        #unbacks the samples and features form the np array X
        samples, features = X.shape
        #sets labels to the length of unique labels in y 
        labels = len(np.unique(y))

        #checks for the stopping criteria
        if depth >= self.maxDepth or labels == 1 or samples < self.minSamples:
            leafVal = self.commonLabel(y)
            #creates leaft node
            return Node(value=leafVal)
        
        #selects random feature to be considered for splitting the data
        featureIndex = np.random.choice(features, self.numFeatures, replace=False)

        #identify the best split
        bestFeature, bestThreshold = self.bestSplit(X, y, featureIndex)

        leftIndex, rightIndex = self.split(X[:, bestFeature], bestThreshold)
        left = self.growTree(X[leftIndex, :], y[leftIndex], depth + 1)
        right = self.growTree(X[:, rightIndex], y[rightIndex], depth + 1)
        return Node(bestFeature, bestThreshold, left, right)
    
     
    def bestSplit(self, X, y, indexes):
        bestGain = -1
        splitIndex = None
        thresholdIndex = None

        for index in indexes:
            X_column = X[:, index]
            thresholds = np.unique(X_column)

            for threshold in thresholds:
                gain = self.infoGain(y, X_column, threshold)

                if gain > bestGain:
                    bestGain = gain
                    splitIndex = index
                    thresholdIndex = threshold
                 
        return splitIndex, thresholdIndex

    def infoGain(self, y, X_column, threshold):

        parentEntropy = self.entropy(y)

        leftIndex, rightIndex = self.split(X_column, threshold)

        leftIndexLen = len(leftIndex)
        rightIndexLen = len(rightIndex)

        if leftIndexLen == 0 or rightIndexLen == 0:
            return 0
        
        yLen = len(y)
        leftEntropy = self.entropy(y[leftIndex])
        rightEntropy = self.entropy(y[rightIndex])
        childEntropy = (leftIndexLen / yLen) * leftEntropy + (rightIndexLen / yLen) * rightEntropy

        #calculate infomation gain
        return parentEntropy - childEntropy
        
    
         
    
    def entropy(self, y):
        frequency = np.bincount(y)
        probabilities = frequency / len(y)
        return -np.sum([p * np.log(p) for p in probabilities if p > 0])

    def split(self, X_column, splitThreshold):
        leftIndex = np.argwhere(X_column <= splitThreshold).flatten()
        rightIndex = np.argwhere(X_column > splitThreshold).flatten()
        
        return leftIndex, rightIndex
    
    def mostCommonLabel(self, y):
        labels, counts = np.unique(y, return_counts = True)
        return labels[np.argmax(counts)]
        return 
    
    def predict(self, X):
        #returns np array of predictions
        return np.array([self.traverseTree(x, self.root) for x in X])
    
    def traverseTree(self, x, node):
        
        #stopping condition
        if node.isLeaf():
            return node.value
        
        #recursive call
        if x[node.feature] <= node.threshold:
            return self.traverseTree(x, node.left)
        return self.traverseTree(x, node.right)