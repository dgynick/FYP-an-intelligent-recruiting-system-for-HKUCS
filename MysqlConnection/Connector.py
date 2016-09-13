import mysql.connector
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
import json

def load_model():
    return json.dumps()



def loadAll(year):
    cnx = mysql.connector.connect(user="root", password="I9940714", host="localhost", database="fyp")
    cursor = cnx.cursor()
    query="select gender, apply_for,major_ug,norm_gpa_ug,norm_gpa_pg,papers,shortlisted,toefl,CET6,onQSRanking,QSRanking from applicants"+str(year)
    cursor.execute(query)
    X = []
    for row in cursor:
        temp=[]
        for i in range(0,11):
            temp.append(row[i])
        X.append(temp)
    return json.dumps(X)

def load_data(iv, dv,result):
    __variables__=["gender","apply_for","major_ug","norm_gpa_ug","norm_gpa_pg","papers","shortlisted","toefl","CET6","onQSRanking","QSRanking"]
    cnx = mysql.connector.connect(user="root", password="I9940714", host="localhost", database="fyp")
    cursor = cnx.cursor()
    ivList=""
    limit=""
    for i in iv:
        ivList+=__variables__[i-1]
        ivList+=","
        if i==4:
            limit+=" norm_gpa_ug>0 and norm_gpa_ug<=1 and"
        if i==5:
            limit+=" norm_gpa_pg>0 and norm_gpa_pg<=1 and"
        if i==8:
            limit+=" toefl>0 and"
        if i==9:
            limit+=" CET6>0 and"
        if i==11:
            limit+=" QSRanking>0 and"
    if dv==4:
        limit+=" norm_gpa_ug>0 and norm_gpa_ug<=1 and"
    if dv==5:
        limit+=" norm_gpa_pg>0 and norm_gpa_pg<=1 and"
    if dv==8:
        limit+=" toefl>0 and"
    if dv==9:
        limit+=" CET6>0 and"
    if dv==11:
        limit+=" QSRanking>0 and"

    ivList = ivList[:-1]
    if len(limit)>0:
        limit = limit[:-4]
        query = "SELECT "+ivList+" FROM applicants2016 where "+limit
    else:
        query = "SELECT "+ivList+" FROM applicants2016"
    cursor.execute(query)
    X = []
    for row in cursor:
        temp=[]
        for i in range(0,len(iv)):
            temp.append(convert(row[i],iv[i]))
        X.append(temp)
    result["count"]=cursor.rowcount

    cat=[]
    text=""
    j=0;
    for i in iv:
        if i==1 or i==2 or i==3 or i==7 or i==10:
            cat.append(j)
        j=j+1
    enc = OneHotEncoder(categorical_features=cat)
    enc.fit(X)
    X=enc.transform(X)
    if(not cat==[]):
        result["ivExplain"]=explainVariables(iv,enc.feature_indices_)

    dvList=__variables__[dv-1]

    if len(limit)>0:
        query = "SELECT "+dvList+" FROM applicants2016 where "+limit
    else:
        query = "SELECT "+dvList+" FROM applicants2016"
    cursor.execute(query)

    Y=[]
    for row in cursor:
        Y.append(row[0])
    cursor.close()
    cnx.close()

    if dv==1 or dv==2 or dv==3 or dv==7 or dv==11:
        le=LabelEncoder()
        le.fit(Y)
        Y=le.transform(Y)
        text="\nThe values of Y are: "+str(le.classes_)
        result["dvExplain"]=text
        print(Y)
        return (X,enc,Y,le)

    return (X,enc,Y,None)


def convert(v,index):
    if index==1:
        if(v=="M"):
            return 1
        if(v=="F"):
            return 0;
        else:
            raise Exception('undefined gender!')
    if index ==2:
        if(v=="phd"):
            return 2
        if(v=="either"):
            return 1
        if(v=="mphil"):
            return 0;
        else:
            raise Exception('undefined apply_for!')
    if index ==3:
        if v=="CS":
            return 0
        if v=="EE":
            return 1
        if v=="SE":
            return 2
        if v=="Auto":
            return 3
        if v=="Math":
            return 4
        else:
            return 5
    return v

def explainVariables(iv,indices):
    text="all categorical variables are converted to dummy variables and moved to the head of input list. " \
         "Numerical variables remain the same order at the end of input list\n\n"
    i=0;
    if(1 in iv):
        if(indices[i+1]-[i])>=1:
            text+="X"+str(indices[i])+"=1 for female, 0 otherwise\n"
        if(indices[i+1]-[i])>=2:
            text+="X"+str(indices[i]+1)+"=1 for male, 0 otherwise\n"
        i=i+1
    if(2 in iv):
        if(indices[i+1]-[i])>=1:
            text+="X"+str(indices[i])+"=1 for mphil, 0 otherwise\n"
        if(indices[i+1]-[i])>=2:
            text+="X"+str(indices[i]+1)+"=1 for either, 0 otherwise\n"
        if(indices[i+1]-[i])>=3:
            text+="X"+str(indices[i]+2)+"=1 for phd, 0 otherwise\n"
        i=i+1
    if(3 in iv):
        if(indices[i+1]-[i])>=1:
            text+="X"+str(indices[i])+"=1 for CS, 0 otherwise\n"
        if(indices[i+1]-[i])>=2:
            text+="X"+str(indices[i]+1)+"=1 for EE, 0 otherwise\n"
        if(indices[i+1]-[i])>=3:
            text+="X"+str(indices[i]+2)+"=1 for SE, 0 otherwise\n"
        if(indices[i+1]-[i])>=4:
            text+="X"+str(indices[i]+3)+"=1 for AUTO, 0 otherwise\n"
        if(indices[i+1]-[i])>=5:
            text+="X"+str(indices[i]+4)+"=1 for MATH, 0 otherwise\n"
        if(indices[i+1]-[i])>=6:
            text+="X"+str(indices[i]+5)+"=1 for OTHER, 0 otherwise\n"
        i=i+1
    if(7 in iv):
        if(indices[i+1]-[i])>=1:
            text+="X"+str(indices[i])+"=1 for not shortlisted, 0 otherwise\n"
        if(indices[i+1]-[i])>=2:
            text+="X"+str(indices[i]+1)+"=1 for shortlisted, 0 otherwise\n"
        i=i+1
    if(10 in iv):
        if(indices[i+1]-[i])>=1:
            text+="X"+str(indices[i])+"=1 for not onQSRanking, 0 otherwise\n"
        if(indices[i+1]-[i])>=2:
            text+="X"+str(indices[i]+1)+"=1 for onQSRanking, 0 otherwise\n"
        i=i+1
    text+="\nthe rest are numerical variables, in the same order as the table above\n"
    return text