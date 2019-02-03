from utils.data_loader import train_data_loader, test_data_loader

import xgboost as xgb
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, Lasso, RidgeClassifier, ElasticNet, Lars, LassoLars
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import fbeta_score, make_scorer

import pandas as pd
import numpy as np
import pickle
import datetime

import warnings
warnings.filterwarnings('ignore')


# Print Current Time
time = str(datetime.datetime.now()).split()[1].split('.')[0]
print("---------- Strart ----------")
print("Start:", time, "\n")


# Print Information
name = 'KHW'
model = 'Stacking sklearn model'
summary = 'HyperParams tuning with 9 sklearn models'

print('Author Name :', name)
print('Model :', model)
print('Summary :', summary)


# Setting
pos_dir = "/data/train/positive/"
neg_dir = "/data/train/negative/"

do_n4 = False
do_ws = True
do_resample = True

do_shuffle = True
save_to_disk = False
return_patient_num = False


# Data Load
print("\n---------- Data Load ----------")
X_train, y_train = train_data_loader(pos_dir, neg_dir, do_n4, do_ws, do_resample, do_shuffle, save_to_disk, return_patient_num)


#########################################################################################################################
#########################################################################################################################
#### Modify here ####


# Fit Model with Training Data
print("\n---------- Start Train ----------")

#########
## model1
print("model1")
model1 = xgb.XGBClassifier(n_jobs=4)

m1_params1 = {
    'max_depth' : [3,5,7,9,11],
    'min_child_weight' : [0.5, 1],
    'gamma' : [0, 0.1],
    'subsample' : [0.5, 0.7, 0.9],
    'colsample_bytree' : [0.5, 0.7, 0.9],
}

m1_grid_1 = GridSearchCV(model1, param_grid=m1_params1, scoring=scorer, cv=5, verbose=0)
m1_grid_1.fit(X_train, y_train)

best_model1 = m1_grid_1.best_estimator_

print("Best Score : {}".format(m1_grid_1.best_score_))
print("Best Params : {}".format(m1_grid_1.best_params_))

m1_params2 = {
    'learning_rate' : [0.01, 0.05, 0.07, 0.1, 0.2],
    'n_estimators' : [n for n in range(100,1001,50)]
}

m1_grid_2 = GridSearchCV(best_model1, param_grid=m1_params2, scoring=scorer, cv=5, verbose=0)
m1_grid_2.fit(X_train, y_train)

best_model1 = m1_grid_2.best_estimator_

print("Best Score : {}".format(m1_grid_2.best_score_))
print("Best Params : {}".format(m1_grid_2.best_params_))

#########
## model2
print("\nmodel2")
model2 = SVC()

m2_params1 = {
    'C': [0.001, 0.01, 0.1, 1, 10, 50, 100], 
    'gamma' : [0.001, 0.01, 0.1, 1, 2, 5, 10, 20],
    'degree' : [2,3,4]
}

m2_grid_1 = GridSearchCV(model2, param_grid=m2_params1, scoring=scorer, cv=5, verbose=0, n_jobs=4)
m2_grid_1.fit(X_train, y_train)

best_model2 = m2_grid_1.best_estimator_

print("Best Score : {}".format(m2_grid_1.best_score_))
print("Best Params : {}".format(m2_grid_1.best_params_))

#########
## model3
print("\nmodel3")
model3 = LogisticRegression(n_jobs=4)

m3_params1 = {
    'C': [0.001, 0.01, 0.1, 1, 10, 50, 100],
    'max_iter' : [n for n in range(100,1101, 200)]
}

m3_grid_1 = GridSearchCV(model3, param_grid=m3_params1, scoring=scorer, cv=5, verbose=0, n_jobs=4)
m3_grid_1.fit(X_train, y_train)

best_model3 = m3_grid_1.best_estimator_

print("Best Score : {}".format(m3_grid_1.best_score_))
print("Best Params : {}".format(m3_grid_1.best_params_))

#########
## model4
print("\nmodel4")
model4 = RandomForestClassifier(n_jobs=4)

m4_params1 = {
    'max_depth' : [n for n in range(10, 101, 5)],
    'min_samples_leaf': [1, 2, 3, 4, 5,10, 20, 50],
    'min_samples_split': [1, 2, 4, 6, 8, 10, 12],
}

m4_grid_1 = GridSearchCV(model4, param_grid=m4_params1, scoring=scorer, cv=5, verbose=0, n_jobs=4)
m4_grid_1.fit(X_train, y_train)

best_model4 = m4_grid_1.best_estimator_

print("Best Score : {}".format(m4_grid_1.best_score_))
print("Best Params : {}".format(m4_grid_1.best_params_))

m4_params2 = {
    'n_estimators' : [n for n in range(100,1001,50)]
}

m4_grid_2 = GridSearchCV(best_model4, param_grid=m4_params2, scoring=scorer, cv=5, verbose=0, n_jobs=4)
m4_grid_2.fit(X_train, y_train)

best_model4 = m4_grid_2.best_estimator_

print("Best Score : {}".format(m4_grid_2.best_score_))
print("Best Params : {}".format(m4_grid_2.best_params_))

#########
## model5
print("\nmodel5")
model5 = LogisticRegression(n_jobs=4, penalty="l1")

m5_params1 = {
    'C': [0.001, 0.01, 0.1, 1, 10, 50, 100],
    'max_iter' : [n for n in range(100,1101, 200)]
}

m5_grid_1 = GridSearchCV(model5, param_grid=m5_params1, scoring=scorer, cv=5, verbose=0, n_jobs=4)
m5_grid_1.fit(X_train, y_train)

best_model5 = m3_grid_1.best_estimator_

print("Best Score : {}".format(m5_grid_1.best_score_))
print("Best Params : {}".format(m5_grid_1.best_params_))

#########
## model6
print("\nmodel6")
model6 = RidgeClassifier()

m6_params1 = {
    'alpha': [0.1, 1, 2, 5, 10, 20, 50, 100],
    'max_iter' : [None]+[n for n in range(100,1101, 200)]
}

m6_grid_1 = GridSearchCV(model6, param_grid=m6_params1, scoring=scorer, cv=5, verbose=0, n_jobs=4)
m6_grid_1.fit(X_train, y_train)

best_model6 = m6_grid_1.best_estimator_

print("Best Score : {}".format(m6_grid_1.best_score_))
print("Best Params : {}".format(m6_grid_1.best_params_))

#########
## model7
print("\nmodel7")
model7 = ElasticNet()

m7_params1 = {
    'alpha': [0.1, 1, 2, 5, 10, 20, 50, 100],
    'l1_ratio':[0.3, 0.4, 0.5, 0.6], 
    'max_iter' : [n for n in range(800, 2001, 200)]
}

m7_grid_1 = GridSearchCV(model7, param_grid=m7_params1, scoring=scorer, cv=5, verbose=0, n_jobs=4)
m7_grid_1.fit(X_train, y_train)

best_model7 = m7_grid_1.best_estimator_

print("Best Score : {}".format(m7_grid_1.best_score_))
print("Best Params : {}".format(m7_grid_1.best_params_))

#########
## model8
print("\nmodel8")
model8 = Lars()

m8_params1 = {
    'n_nonzero_coefs': [n for n in range(30, 150, 10)],
}

m8_grid_1 = GridSearchCV(model8, param_grid=m8_params1, scoring=scorer, cv=5, verbose=0, n_jobs=4)
m8_grid_1.fit(X_train, y_train)

best_model8 = m8_grid_1.best_estimator_

print("Best Score : {}".format(m8_grid_1.best_score_))
print("Best Params : {}".format(m8_grid_1.best_params_))

#########
## model9
print("\nmodel9")
model9 = LassoLars()

m9_params1 = {
    'alpha': [0.1, 1, 2, 5, 10, 20, 50, 100],
    'max_iter' : [n for n in range(800, 2001, 200)]
}

m9_grid_1 = GridSearchCV(model9, param_grid=m9_params1, scoring=scorer, cv=5, verbose=0, n_jobs=4)
m9_grid_1.fit(X_train, y_train)

best_model9 = m9_grid_1.best_estimator_

print("Best Score : {}".format(m9_grid_1.best_score_))
print("Best Params : {}".format(m9_grid_1.best_params_))


# Model Stacking
print("\n---------- Model Stacking ----------")
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils

def stacking(models, data) : 
    result = []
    
    for model in models :
        result.append(model.predict_proba(data))
        
    return np.array(result).T

def stack_fn(num_models=9):
    model = Sequential()
    model.add(Dense(16, input_dim=num_models, activation='relu'))
    model.add(Dense(2, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

models = [best_model1, best_model2, best_model3, best_model4, best_model5, best_model6, best_model7, best_model8, best_model9]
S_train = stacking(models, X_train)

meta_model = KerasClassifier(build_fn=stack_fn)
meta_model.fit(S_train, y_train)


# Save model to file
print("\n---------- Save Stacking ----------")
pickle.dump(model1, open('/data/model/model1.pickle.dat', 'wb'))
pickle.dump(model2, open('/data/model/model2.pickle.dat', 'wb'))
pickle.dump(model3, open('/data/model/model3.pickle.dat', 'wb'))
pickle.dump(model4, open('/data/model/model4.pickle.dat', 'wb'))
pickle.dump(model5, open('/data/model/model5.pickle.dat', 'wb'))
pickle.dump(model6, open('/data/model/model6.pickle.dat', 'wb'))
pickle.dump(model7, open('/data/model/model7.pickle.dat', 'wb'))
pickle.dump(model8, open('/data/model/model8.pickle.dat', 'wb'))
pickle.dump(model9, open('/data/model/model9.pickle.dat', 'wb'))

meta_model.model.save_weights('/data/model/model_weights.h5')

with open('/data/model/model_architecture.json', 'w') as f :
    f.write(meta_model.to_json())





