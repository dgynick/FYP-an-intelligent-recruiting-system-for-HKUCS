import sys
from MysqlConnection.Connector import load_data
from Classification import *
from Regression import *


def main(iv,dv,model):
    result={}
    (X,enc,Y,le)=load_data(iv,dv,result)
    if dv==1 or dv==2 or dv==3 or dv==7 or dv==10:
        if model =="decisionTree":
            DecisionTree.tree_mining(X,enc,Y,le,result)
        if model =="logisticRegression":
            LogisticRegression.logistic_mining(X,enc,Y,le,result)

    else:
        if model=="decisionTree":
            DecisionTreeRegression.tree_regression_mining(X,enc,Y,le,result)
        if model=="linearRegression":
            LinearRegression.lr_mining(X,enc,Y,le,result)

    return result

def getSampleSize(iv,dv,model):
    result={}
    (X,enc,Y,le)=load_data(iv,dv,result)
    return len(Y);



if __name__ == "__main__":
    main()