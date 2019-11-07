import numpy as np
import sys
# import time


class SVM:

    def __init__(self, x, y, epochs=200, learning_rate=0.01):
        self.x = np.c_[np.ones((x.shape[0])), x]
        self.y = y
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.w = np.random.uniform(size=np.shape(self.x)[1],)
        self.train()

    def get_loss(self, x, y):
        loss = max(0, 1 - y * np.dot(x, self.w))
        return loss

    def cal_sgd(self, x, y, w):
        if y * np.dot(x, w) < 1:
            w = w - self.learning_rate * (-y * x)
        else:
            w = w
        return w

    def train(self):
        for epoch in range(self.epochs):
            randomize = np.arange(len(self.x))
            np.random.shuffle(randomize)
            x_ = self.x[randomize]
            y_ = self.y[randomize]
            loss = 0
            for xi, yi in zip(x_, y_):
                loss += self.get_loss(xi, yi)
                self.w = self.cal_sgd(xi, yi, self.w)
            # print('epoch: {0} loss: {1}'.format(epoch, loss))

    def predict(self, _):
        x_test = np.c_[np.ones((_.shape[0])), _]
        return np.sign(np.dot(x_test, self.w))


# global:
timebudget = 0
x = []
y = []
test_x = []
test_y = []


def initialize():
    global timebudget
    global x
    global y
    global test_x
    global test_y

    trainpath = sys.argv[1]
    testpath = sys.argv[2]
    timebudget = int(sys.argv[4])
    # traindata:
    x = np.loadtxt(trainpath, usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
    y = np.loadtxt(trainpath, usecols=10)
    # testdata:
    test_x = np.loadtxt(testpath, usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
    # test_y = np.loadtxt(testpath, usecols=10)


def main():
    # start = time.time()
    initialize()
    svm = SVM(x, y)
    res = svm.predict(test_x)
    # error = 0
    for i in range(len(res)):
        print(int(res[i]))
        # if res[i] != test_y[i]:
        #     error += 1
    # print('error rate:'+str(error/len(test_y)))
    # print("time:"+str(time.time()-start))


if __name__ == '__main__':
    main()
