#!/usr/bin/env python
# coding: utf-8

# In[129]:


import pandas as pd


# In[130]:


df = pd.read_excel('/Users/aaryanbahl/Desktop/Classifier and Model for Prediction /Training_Data_Binary_Model_V1.xlsx')


# In[131]:


import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing
#creating labelEncoder
le = preprocessing.LabelEncoder()
# Converting string labels into numbers.
labels=le.fit_transform(df["Service/Goods"])
df["label"] = labels


# In[132]:


labels.mean()


# In[133]:


sku_train, sku_test, label_train, label_test = train_test_split(df["Short Text"], df["label"], train_size = 0.7, test_size = 0.3)


# In[15]:


sku_hold, sku_test, label_hold, label_test = train_test_split(sku_test, label_test, train_size = 0.5)


# In[16]:


vectorizer = TfidfVectorizer()
vect_train = vectorizer.fit_transform(sku_train)


# In[17]:


len(label_train)


# In[18]:


vect_test = vectorizer.transform(sku_test)


# In[1009]:


vect_hold = vectorizer.transform(sku_hold)


# In[1010]:


vect_train.count_nonzero()
len(vectorizer.get_feature_names())
vect_train.shape


# In[1011]:


vect_test.count_nonzero()


# In[1012]:


vect_train.count_nonzero()


# In[1013]:


vect_hold.count_nonzero()


# In[1014]:


from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB(alpha = 0.51)
nb.fit(vect_train,label_train)


# In[1015]:


l_pred = (nb.predict_proba(vect_test)[:,1] >= 0.5)
print("Accuracy test data:",metrics.accuracy_score(label_test, l_pred))


# In[1016]:


pred = nb.predict(vect_test)


# In[22]:


from sklearn import metrics
print("Accuracy test data:",metrics.accuracy_score(label_test, pred))


# In[1018]:


label_test.mean()


# In[1019]:


pred2 = nb.predict(vect_train)


# In[1020]:


print("Accuracy train data:",metrics.accuracy_score(label_train, pred2))


# In[1021]:


np.mean(label_train)


# In[1022]:


pred3 = nb.predict(vect_hold)


# In[1023]:


print("Accuracy hold data:",metrics.accuracy_score(label_hold, pred3))


# In[1024]:


np.mean(label_hold)


# In[1025]:


y_pred_prob = nb.predict_proba(vect_test)[:, 1]


# In[1026]:


print(metrics.roc_auc_score(label_test, y_pred_prob))


# In[1027]:


from sklearn.model_selection import cross_val_score
cross_val_score(nb, vect_full, labels, cv=10, scoring='roc_auc').mean()


# In[1028]:


print(metrics.confusion_matrix(label_test, pred))


# In[547]:


print(metrics.confusion_matrix(label_train, pred2))


# In[548]:


print(metrics.confusion_matrix(label_hold, pred3))


# In[817]:


from sklearn.linear_model import LogisticRegression

# instantiate model
logreg = LogisticRegression()

# fit model
logreg.fit(vect_train,label_train)


# In[818]:


predl1 = logreg.predict(vect_test)


# In[819]:


print("Accuracy test data:",metrics.accuracy_score(label_test, predl1))


# In[820]:


predl2 = logreg.predict(vect_train)
print("Accuracy test data:",metrics.accuracy_score(label_train, predl2))


# In[821]:


predl3 = logreg.predict(vect_hold)
print("Accuracy test data:",metrics.accuracy_score(label_hold, predl3))


# In[588]:


from sklearn.ensemble import RandomForestClassifier

#Create a Gaussian Classifier
clf=RandomForestClassifier(random_state=1,n_estimators=300, min_samples_leaf=1)

#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(vect_train,label_train)


# In[590]:


predf1 = logreg.predict(vect_test)
print("Accuracy test data:",metrics.accuracy_score(label_test, predf1))


# In[591]:


predf2 = logreg.predict(vect_train)
print("Accuracy test data:",metrics.accuracy_score(label_train, predf2))


# In[1298]:


df1 = df.drop(df[df["label"]==0].sample(7838).index)


# In[1299]:


df1


# In[1300]:


df


# In[1309]:


sku_train1, sku_test1, label_train1, label_test1 = train_test_split(df1["Short Text"], df1["label"], train_size = 0.7)


# In[1310]:


sku_train1, sku_train2, label_train1, label_train2 = train_test_split(sku_train1, label_train1, train_size = 0.34)


# In[1311]:


sku_train3, sku_train2, label_train3, label_train2 = train_test_split(sku_train2, label_train2, train_size = 0.5)


# In[1312]:


sku_test1, sku_test2, label_test1, label_test2 = train_test_split(sku_test1, label_test1, train_size = 0.33)
sku_test3, sku_test2, label_test3, label_test2 = train_test_split(sku_test2, label_test2, train_size = 0.5)


# In[1313]:


vect1 = TfidfVectorizer()
vect_train1 = vect1.fit_transform(sku_train1)
vect_test1 = vect1.transform(sku_test1)
vect2 = TfidfVectorizer()
vect_train2 = vect2.fit_transform(sku_train2)
vect_test2 = vect2.transform(sku_test2)
vect3 = TfidfVectorizer()
vect_train3 = vect3.fit_transform(sku_train3)
vect_test3 = vect3.transform(sku_test3)


# In[1314]:


nb1 = MultinomialNB(alpha = 0.6)
nb1.fit(vect_train1,label_train1)
pred1 = nb1.predict(vect_test1)
print("Accuracy test data:",metrics.accuracy_score(label_test1, pred1))


# In[1315]:


nb2 = MultinomialNB()
nb2.fit(vect_train2,label_train2)
pred2 = nb2.predict(vect_test2)
print("Accuracy test data:",metrics.accuracy_score(label_test2, pred2))


# In[1316]:


nb3 = MultinomialNB(alpha = 0.5)
nb3.fit(vect_train3,label_train3)
pred3 = nb3.predict(vect_test3)
print("Accuracy test data:",metrics.accuracy_score(label_test3, pred3))


# In[1240]:


import random


# In[1297]:


random.seed(325)

sku = df["Short Text"]
# In[5]:


sku = df["Short Text"]


# In[6]:


sku


# In[135]:


tfidfvect = TfidfVectorizer()


# In[136]:


vect_sku = tfidfvect.fit_transform(sku)


# In[141]:


from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB(alpha = 0.0001)
model.fit(vect_sku,labels)


# In[11]:


import pickle

pickle.dump(tfidfvect, open("/Users/aaryanbahl/Desktop/Classifier and Model for Prediction /tfidf.pickle", "wb"))


# In[118]:


filename = '/Users/aaryanbahl/Desktop/Classifier and Model for Prediction /finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))

