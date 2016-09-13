from sklearn import tree
from subprocess import check_call

def tree_regression_mining(X,enc,Y,le,result):

    clf = tree.DecisionTreeRegressor(min_samples_leaf=result["count"]/10)
    clf.fit(X, Y)
    text=("R square:")
    text+=str(clf.score(X,Y))+"\n"
    text+=("feature importances:\n")
    j=0
    for i in clf.feature_importances_:
        text+=("X"+str(j)+": "+str(i)+"\n")
        j=j+1
    ##text+=str(clf.feature_importances_)+"\n\n"
    result["text"]=text
    tree.export_graphviz(clf,out_file='tree.dot')
    check_call(['dot','-Tpng','tree.dot','-o','treeRegression.png'])
    result["graphURL"]="treeRegression.png"