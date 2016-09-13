from sklearn import linear_model

def lr_mining(X,enc,Y,le,result):
    clf = linear_model.LinearRegression()
    clf.fit(X,Y)
    text="model successfully built\n"
    text+=("Rsquare :")
    text+=str(clf.score(X,Y))+"\n\n"
    text+=("coefficients :")
    text+=str(clf.coef_)+"\n\n"
    text+=("intercept :")
    text+=str(clf.intercept_)
    result["text"]=text