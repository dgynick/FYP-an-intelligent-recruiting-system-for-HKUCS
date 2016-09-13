import mysql.connector
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from subprocess import check_call



#http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier


def tree_example():
    cnx =  mysql.connector.connect(user="root",password="I9940714",host="localhost",database="fyp")
    cursor = cnx.cursor()
    query = "SELECT apply_for, gpa_ug/gpa_ug_scale FROM applicants2016 where gpa_ug>0 and gpa_ug_scale>gpa_ug"
    cursor.execute(query)
    Y=[]
    X=[]
    Z=[]
    for (a,b) in cursor:
        X.append([b])
        if a.lower() == "mphil":
            Y.append('m')
            Z.append(0)
        elif a.lower()=="either":
            Y.append('e')
            Z.append(1)
        elif a.lower() =="phd":
            Y.append('p')
            Z.append(2)
        else:
            raise Exception

    cursor.close()
    cnx.close()

    le=LabelEncoder()
    le.fit(Y)
    le.transform(Y)
    clf1 = tree.DecisionTreeClassifier()
    clf1.fit(X,Y)
    print(clf1.predict([[x*0.01] for x in range(60,90,1)]))

    clf2 = tree.DecisionTreeClassifier()
    clf2.fit(X,Z)
    print(clf2.predict([[x*0.01] for x in range(60,90,1)]))


def tree_mining(X,enc,Y,le,result):
    clf = tree.DecisionTreeClassifier(min_samples_leaf=result["count"]/10)
    clf.fit(X,Y)
    text=("model successfully built\n\n")
    text+=("accuracy "+str(clf.score(X,Y)))+"\n\n"
    text+=("feature importance:\n")
    j=0
    for i in clf.feature_importances_:
        text+=("X"+str(j)+": "+str(i)+"\n")
        j=j+1
    ##text+=str(clf.feature_importances_)+"\n\n"
    result["text"]=text
    tree.export_graphviz(clf,out_file='tree.dot')
    check_call(['dot','-Tpng','tree.dot','-o','tree.png'])
    result["graphURL"]="tree"+".png"

    ##Gtmp = pgv.AGraph('tree.dot')

if __name__ == "__main__":
    tree_example()
