from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR as SupportVectorRegression
from matplotlib import pyplot
import numpy as np
import copy

class PlayerModel():

    def __init__(self):
        # get and parse the data
        levelData = open("../level.txt")
        dataset = np.loadtxt(levelData, delimiter = "\t")
        self.dataset = dataset
        print "raw data: "
        print dataset
        self.row = dataset.shape[0]
        self.col = dataset.shape[1]
        # print self.row, self.col
        new_data = self.normalize()
        self.dataset_X_train = new_data[:, 0:self.col - 1]
        self.dataset_Y_train = new_data[:, self.col - 1]

    def getTrainingX(self):
        return self.dataset_X_train

    def getTrainingY(self):
        return self.dataset_Y_train

    def normalize(self):
        new_data = np.zeros((self.row, self.col))
        tmp_list = []
        raw_data = self.dataset[:, 0:self.col].T

        # print raw_data
        for row in raw_data:
            maximum = row[0]
            minimum = row[0]
            for num in row:
                if num > maximum:
                    maximum = num
                if num < minimum:
                    minimum = num
            tmp_list.append((maximum, minimum))

        self.maxmin_list = tmp_list
        # print tmp_list
        raw_data = raw_data.T
        # print raw_data
        # print new_data
        # print range(self.col)

        # minmax normalization
        for i in range(self.row):
            for j in range(self.col):
                new_data[i, j] = (raw_data[i, j] - tmp_list[j][1]) / (tmp_list[j][0] - tmp_list[j][1])

        # print "normalize: "
        # print new_data
        return new_data

    def normalizeTest(self, data):
        new_data = np.zeros(self.col - 1)
        # print "maxmin_list: ", self.maxmin_list
        for i in range(self.col - 1):
            new_data[i] = (data[i] - self.maxmin_list[i][1]) / (self.maxmin_list[i][0] - self.maxmin_list[i][1])
        # print "normalize test: ", new_data
        return new_data


### a python wrapper to build player model using linear regression
class LR(PlayerModel):
    ### a wrapper for linear regression using scikit-learn for this project
    def __init__(self):
        PlayerModel.__init__(self)
        # configure linear regression and start training
        self.regr = LinearRegression()
        self.regr.fit(self.dataset_X_train, self.dataset_Y_train)
        print "Finish building player model."
        print('Coefficients: \n', self.regr.coef_)

    def testScore(self, test_X):
        score = self.regr.predict(self.normalizeTest(test_X))
        return np.mean(score)

    def getParams(self):
        return self.regr.coef_

    def visualize(self):
        x = np.zeros((10, self.col - 1))
        for i in range(10):
            x[i, :] = self.dataset_X_train[0, :]
        x[:, 3:4] = np.array([np.arange(0., 1.2, 0.12)]).T
        y = self.regr.predict(x)
        pyplot.scatter(self.dataset_X_train[:, 3:4], self.dataset_Y_train, c='k', label='data')
        pyplot.hold('on')
        pyplot.plot(x[:, 3:4], y, c = "r", label='Linear Regression')
        pyplot.xlabel('data collect from player')
        pyplot.ylabel('score')
        pyplot.title('Linear Regression')
        pyplot.legend()
        pyplot.show()


### a python wrapper to build player model using support vector regression with RBF kernel
class SVR(PlayerModel):
    ### a wrapper for support vector regression using scikit-learn for this project
    def __init__(self):
        PlayerModel.__init__(self)
        # configure support vector regression and start training
        self.regr = SupportVectorRegression(kernel = 'rbf', C = 1e3)
        self.regr.fit(self.dataset_X_train, self.dataset_Y_train)
        print "Finish building player model."
        print self.regr.get_params()

    def testScore(self, test_X):
        score = self.regr.predict(self.normalizeTest(test_X))
        # print("Predicted Score: %.2f" % np.mean(score))
        return np.mean(score)

    def getParams(self):
        return self.regr.get_params()

    def visualize(self):
        # print self.dataset_X_train[:, 3:4]
        # print self.dataset_Y_train
        # x = np.arange(0., 1., 0.05)
        x = np.zeros((10, self.col - 1))
        for i in range(10):
            x[i, :] = self.dataset_X_train[0, :]
        x[:, 3:4] = np.array([np.arange(0., 1.2, 0.12)]).T
        # print x
        y = self.regr.predict(x)
        # print y
        pyplot.scatter(self.dataset_X_train[:, 3:4], self.dataset_Y_train, c='k', label='data')
        pyplot.hold('on')
        pyplot.plot(x[:, 3:4], y, c = "r", label='Support Vector Regression')
        pyplot.xlabel('data collect from player')
        pyplot.ylabel('score')
        pyplot.title('Support Vector Regression')
        pyplot.legend()
        pyplot.show()


if __name__ == "__main__":
    ### unit testing client
    test_X = np.array([  5.,         2.,           0.03089701])
    test_X = np.array([  3.,         6.,           1.22868792])
    # test for linear regression
    linearModel = LR()
    score1 = linearModel.testScore(test_X)
    print "Score by linear model: ", score1
    linearModel.visualize()

    # test for SVR
    svr = SVR()
    score2 = svr.testScore(test_X)
    print "Score by suppor vector regression", score2
    svr.visualize()
