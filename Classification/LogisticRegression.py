import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
import mysql.connector

# http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression
# shall use L2 regularization for small dataset


def logistic_regression_example():
    cnx =  mysql.connector.connect(user="root",password="I9940714",host="localhost",database="fyp")
    cursor = cnx.cursor()
    query = "SELECT CET6, gpa_ug/gpa_ug_scale FROM applicants2016 where CET6>0 and gpa_ug>0 and gpa_ug_scale>gpa_ug"
    cursor.execute(query)
    X=[]
    Y=[]
    Z=[]
    for (a,b) in cursor:
        X.append(a)
        Z.append(b)
    temp= sorted(zip(X,Z))
    cursor.close()
    cnx.close()

    X=[[a] for (a,b) in temp]
    Z=[b for (a,b) in temp]
    ##plt.plot(np.ravel(X),Z)
    ##plt.show()

    Y=[c>0.9 for c in Z]
    clf_l2_LR = LogisticRegression( penalty='l2', tol=0.01,solver="liblinear")
    clf_l2_LR.fit(X,Y)
    print(clf_l2_LR.coef_.ravel())
    print(clf_l2_LR.predict([[a] for a in range(400,600,10)]))


def logistic_mining(X,enc,Y,le,result):

    clf = LogisticRegression( penalty='l2', tol=0.01,solver="liblinear")
    clf.fit(X,Y)

    text=("model successfully built\n")
    text+=("mean accuracy: "+str(clf.score(X,Y))+"\n")
    i=0
    if(len(clf.coef_)==1):
        i=1
        for (coef,intercept) in zip(clf.coef_,clf.intercept_):
            text+="\n"
            text+=("for level ")
            text+=str(list(le.classes_)[i])
            text+=(" ,Pr(Y belongs to this class) = inverse_logit(intercept + sum(ci*Xi)) where intercept=")
            text+=str(intercept)+"\n"
            j=0
            for c in coef:
                text+=("c"+str(j)+"="+str(c)+"\n")
                j=j+1
            result["text"]=text
        return
    for (coef,intercept) in zip(clf.coef_,clf.intercept_):
        text+="\n"
        text+=("for level ")
        text+=str(list(le.classes_)[i])
        text+=(" ,Pr(Y belongs to this class) = inverse_logit(intercept + sum(ci*Xi)) where intercept=")
        text+=str(intercept)+"\n"
        j=0
        for c in coef:
            text+=("c"+str(j)+"="+str(c)+"\n")
            j=j+1
        i=i+1
    result["text"]=text

if __name__ == "__main__":
    logistic_regression_example()