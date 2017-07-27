from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import SGDClassifier, PassiveAggressiveClassifier
from sklearn.externals import joblib
import numpy as np
import pickle

#clf = svm.SVC()
clf1 = PassiveAggressiveClassifier()
clf2 = SGDClassifier()
scaler = StandardScaler()

X = np.loadtxt('features.txt')
y = [0]*4192 + [1]*3317
#X = SelectKBest(chi2, k=10).fit_transform(X, y)
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
#clf.fit(X_train, y_train)
clf1.fit(X, y)
clf2.fit(X, y)
print clf1.score(X_test, y_test)
print clf2.score(X_test, y_test)
joblib.dump(clf1, 'passive_aggressive.pkl')
joblib.dump(clf2, 'sgd.pkl')
#joblib.dump(scaler, 'scaler.pkl')