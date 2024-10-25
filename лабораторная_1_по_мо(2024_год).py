# -*- coding: utf-8 -*-
"""Лабораторная 1 по МО(2024 год).ipynb"

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18Sryr7XLATsM9up_oBej3c8o4eqoE9Jy
"""



import pandas as pd
import numpy as np
import seaborn as sns

"""Загружаем датасет"""

ds=pd.read_csv("/content/drive/MyDrive/Spotify_Youtube.csv")
ds.head()

"""Получаем общую информацию"""

ds.describe()

ds.info()
url_cols = ['Url_spotify', 'Uri', 'Url_youtube', 'Title', 'Description']
ds.drop(url_cols, axis=1, inplace=True)

ds.describe()

ds.info()

"""Мы видим, что всего 20718 строк, но при этом в некоторых столбцах гораздо меньше значений, значит их нужно удалить"""

ds.dropna(inplace=True)

ds.info()

ds.describe()

ds.drop('Unnamed: 0', axis=1, inplace=True)

ds = ds.drop_duplicates()
ds.info()



sns.scatterplot(data = ds, x = 'Instrumentalness', y = 'Views')

sns.scatterplot(data = ds, x = 'Liveness', y = 'Views')

sns.scatterplot(data = ds, x = 'Views', y = 'Likes')

sns.scatterplot(data = ds, x = 'Liveness', y = 'Likes')

sns.scatterplot(data = ds, x = 'Instrumentalness', y = 'Likes')

sns.scatterplot(data = ds, x = 'Duration_ms', y = 'Likes')

sns.scatterplot(data = ds, x = 'Tempo', y = 'Danceability')

sns.scatterplot(data = ds, x = 'Loudness', y = 'Energy')

sns.scatterplot(data = ds, x = 'Acousticness', y = 'Loudness')

sns.histplot(data = ds, x = 'Energy', bins = 100)

sns.histplot(data = ds, x = 'Danceability', bins = 100)

sns.histplot(data = ds, x = 'Loudness', bins = 50)

sns.histplot(data = ds, x = 'Tempo', bins = 30)

sns.boxplot(data = ds, x ='Danceability')

import matplotlib.pyplot as plt
plt.hist(ds['Danceability'], bins=100)
plt.title('Danceability')

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import normalize
numeric_ds = ds.select_dtypes(exclude='object')
imp = SimpleImputer(strategy='mean')
new_ds = pd.DataFrame(data = imp.fit_transform(numeric_ds),columns=numeric_ds.columns, index =numeric_ds.index)
new_ds.info()
norm_ds = pd.DataFrame(data = normalize(new_ds.values),columns = new_ds.columns,index=new_ds.index)
norm_ds.describe()
del numeric_ds
del new_ds

norm_ds.describe()

for col in norm_ds.columns:
    ds[col] = norm_ds[col]
del norm_ds

ds.info()

plt.hist(ds['Danceability'], bins=100, range=(0.0,0.00000009))
plt.title('Danceability')

sns.boxplot(data = ds, x ='Views')

sns.heatmap(ds.select_dtypes(exclude = 'object').corr(), annot=True, fmt='.1g', annot_kws={"size":6}, linewidths=1, linecolor='black', square=True, cbar_kws= {'orientation': 'vertical'})

y=ds['Stream']
ds=ds.drop('Stream', axis=1)

test=ds['Track']
ds=ds.select_dtypes(exclude='object')
ds.info()

ds.insert(loc=len(ds.columns), column = 'y', value = y)
ds.info()

"""Так как у нас нет столбца с Id, то нужно добавить его, чтобы потом смочь как-то отследить"""

ds.reset_index(inplace=True)
ds.info()
ds=ds.drop('level_0',axis=1)

ds['y'].mean()



ds['y'].median()

"""Определим target переменную - количество стримов. Разобьем их следующим образом:
1 категория - меньше среднего количества стримов
2 категория - между средним и медианным значениями
3 категория - больше медианного
"""

def get_target_status(ds):
  if (ds['y'] <= 0.8279840218539499):
    return 1
  if ((ds['y'] <= 0.9500946548910993) and (ds['y'] > 0.8279840218539499)):
    return 2
  if (ds['y'] > 0.9500946548910993):
    return 3

  return None

ds['Target'] = ds.apply(get_target_status, axis=1)
ds['Target'].max()

import matplotlib.pyplot as plt
Targets = ds['Target'].value_counts().head(3)
plt.xlabel('Target')
plt.ylabel('Количество')
plt.bar(x=Targets.index, height=Targets.values)

Y=ds['Target']
X=ds.drop('Target',axis=1)
ds

"""Теперь будем работать с X и Y"""

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=35)

X_train.shape

X_test.shape

"""kNN"""

from sklearn.neighbors import KNeighborsClassifier

classifier_kNN = KNeighborsClassifier(n_neighbors=3)

classifier_kNN.fit(X_train, Y_train)

Y_pred = classifier_kNN.predict(X_test)

from sklearn.metrics import confusion_matrix ,classification_report,ConfusionMatrixDisplay

print(classification_report(Y_pred,Y_test))

cm = confusion_matrix(Y_test, Y_pred, labels=classifier_kNN.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                      display_labels=classifier_kNN.classes_)
disp.plot()

from sklearn.metrics import RocCurveDisplay
RocCurveDisplay.from_predictions(Y_test, Y_pred, pos_label=1)

"""SVM"""

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

classifier_SVC = SVC(gamma='auto',probability=True)

classifier_SVC.fit(X_train, Y_train)

Y_pred=classifier_SVC.predict(X_test)

from sklearn.metrics import RocCurveDisplay
RocCurveDisplay.from_predictions(Y_test, Y_pred, pos_label=1)

"""DECISION TREE"""

from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(max_features = 1)

model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)

print(classification_report(Y_pred,Y_test))

from sklearn.metrics import RocCurveDisplay
RocCurveDisplay.from_predictions(Y_test, model.predict(X_test), pos_label=1)

from sklearn import tree
fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(model,
                   feature_names=X_train.columns.values.tolist(),
                   class_names=Y_train.astype("str").unique().tolist(),
                   filled=True)

from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score

def metrics(type_, Y_test, Y_pred, Y_score):
  print(type_, " Metrics: \n")
  print("Accuracy: ", accuracy_score(Y_test, Y_pred))
  print("Precision: ", precision_score(Y_test, Y_pred, average=None))
  print("Recall: ", recall_score(Y_test, Y_pred, average=None))

  print("F1 score: ", f1_score(Y_test, Y_pred, average=None))
  print("ROC-AUC score: ", roc_auc_score(Y_test, Y_score, multi_class='ovr'))
  print()

metrics("KNN classifier", Y_test, classifier_kNN.predict(X_test), classifier_kNN.predict_proba(X_test))

metrics("SVM", Y_test, classifier_SVC.predict(X_test), classifier_SVC.predict_proba(X_test))

metrics("Decision Tree", Y_test, model.predict(X_test), model.predict_proba(X_test))

