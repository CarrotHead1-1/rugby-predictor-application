
from decisionTree import DecisionTree
import numpy as np

class RandomForest:

    def __init__(self, numTrees=10, maxDepth = 10, minSamples = 2, numFeatures=None):
        self.numTrees = numTrees
        self.maxDepth = maxDepth
        self.minSamples = minSamples
        self.numFeatures = numFeatures
        self.trees = []

    def fit(self, X, y):
        self.trees = []
        for _ in range(self.numTrees):
            tree = DecisionTree(maxDepth=self.maxDepth, minSamples=self.minSamples, numFeatures=self.numFeatures)
            XBootstrap, yBootstrap = self.bootstrap(X, y)
            tree.fit(XBootstrap, yBootstrap)
            self.trees.append(tree)
    
    def bootstrap(self, X, y):
        samples = X.shape[0]
        indexes = np.random.choice(samples, samples, replace=True)
        return X[indexes], y[indexes]
    
    def commonLabel(self, y):
        labels, counts = np.unique(y, return_counts = True)
        return labels[np.argmax(counts)]
    
    def predict(self, X):
        predictions = np.array([tree.predict(X) for tree in self.trees]) 
        treePredictions = np.swapaxes(predictions, 0, 1)
        predictions = np.array([self.commonLabel(prediction) for prediction in treePredictions])
        return predictions
    
    def importance(self):
        importance = {}

        for tree in self.trees:
            for feature, weight in tree.featureWeight.items():
                if feature in importance:
                    importance[feature] += weight
                else:
                    importance[feature] = weight
        
        total = sum(importance.values())
        for feature in importance:
            importance[feature] /= total
        
        return importance