from sklearn import svm
import numpy as np


def svr_mining(X,enc,Y,le):
    clf= svm.SVR()
    clf.fit(X,Y)
    print("R square:",end="")
    print(clf.score(X,Y))