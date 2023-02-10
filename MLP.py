import pandas as pd

data = pd.read_csv(r'covid_symptoms.csv')
datas = pd.DataFrame(data)


dataset = data.to_numpy()
X = dataset[:, :-1] # X
Y = dataset[:, -1] # Y


# split data 
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 0)
print ('Train set:', X_train.shape,  Y_train.shape)
print ('Test set:', X_test.shape,  Y_test.shape)

from sklearn.metrics import accuracy_score 
import pickle

#Neural Networks (MLP)
from sklearn.neural_network import MLPClassifier
MLP = MLPClassifier(random_state=0, max_iter=600).fit(X_train, Y_train)
Y_pred = MLP.predict(X_test)


#save model
filename = 'finalized_model.sav'
pickle.dump(MLP, open(filename, 'wb'))



print("\nMLP")
print('Accuracy: ', accuracy_score(Y_test, Y_pred)*100)