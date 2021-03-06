import pandas as pd
import numpy as np
import pickle
import sklearn.ensemble as ske
from sklearn import cross_validation, tree, linear_model
from sklearn.feature_selection import SelectFromModel
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt

data = pd.read_csv('Main_data.csv', sep='\t')
X = data.drop(['Legitimate'], axis=1).values
y = data['Legitimate'].values


X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y ,test_size=0.2)


#Algorithm comparison
algorithms = {
        "DecisionTree": tree.DecisionTreeClassifier(max_depth=10),
        "RandomForest": ske.RandomForestClassifier(n_estimators=50),
        "GradientBoosting": ske.GradientBoostingClassifier(n_estimators=50),
        "AdaBoost": ske.AdaBoostClassifier(n_estimators=100),
        "GNB": GaussianNB()
    }

results = {}
print("\nNow testing algorithms")
for algo in algorithms:
    clf = algorithms[algo]
    clf.fit(X_train, y_train)
    scores = cross_val_score(clf, X, y, cv=5)
    print("Accuracy of %s: %0.2f (+/- %0.2f)" % (algo,scores.mean()*100, scores.std() * 2))
    results[algo] = scores.mean()
values=[]
for key,value in results.iteritems():

   value=value*100.00
   values.append(value);
labels = ['GNB','Decision Tree','GradientBoosting','Random Forest','AdaBoost']
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','blue']
 # explode 1st slice

total = sum(values)
explode=(0, 0, 0, 0, 0)
plt.title('Accuracy rate')
plt.pie(values, explode=explode, labels=labels,autopct=lambda(p): '{:.0f}'.format(p * total / 100),shadow=True, startangle=90) 
plt.axis('equal')
plt.show()

    
winner = max(results, key=results.get)
print winner


print('\nWinner algorithm is %s with a %f %% success' % (winner, results[winner]*100))


# Save the algorithm and the feature list for later predictions
print('Saving algorithm and feature list in classifier directory...')
joblib.dump(algorithms[winner], 'classifier/classifier.pkl')
print('Saved')

# Identify false and true positive rates
clf = algorithms[winner]
res = clf.predict(X_test)
mt = confusion_matrix(y_test, res)
print("False positive rate : %f %%" % ((mt[0][1] / float(sum(mt[0])))*100))
print('False negative rate : %f %%' % ( (mt[1][0] / float(sum(mt[1]))*100)))


