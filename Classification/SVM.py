from sklearn import svm
import mysql.connector
#http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC
#for w= coef[i], the seperating hyperpane is w[0]X1+w[1]X2-intercept[i]=0
def svm_example():
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
    clf = svm.SVC()
    clf.fit(X, Y)
    print(clf.predict([[a] for a in range(400,600,10)]))
    cursor.close()
    cnx.close()

    X=[[1,1],[1,2],[2,1],[2,2]]
    Y=[0,0,1,1]
    clf = svm.SVC(decision_function_shape="ovo")
    clf.fit(X, Y)
    print(clf._get_coef())
    print(clf.intercept_)


def svm_mining(X,enc,Y,le):
    clf = svm.SVC("ovo")
    clf.fit(X, Y)
    print(clf.support_vectors_)
    print(clf.support_)
    print(clf.n_support_)




if __name__ == "__main__":
    svm_example()
