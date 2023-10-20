import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=300, n_features=4, n_classes=3, n_clusters_per_class=1, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_predict = model.predict(X_test)

cf_m = confusion_matrix(y_test, y_predict)
print('confusion matrix', cf_m)

plt.figure(figsize=(6, 6))
plt.imshow(cf_m, interpolation='nearest', cmap='viridis')
plt.colorbar()

classes = [0, 1, 2]
num_classes = len(cf_m)
tick_marks = np.arange(num_classes)

plt.xticks(tick_marks, [f'Class {i}' for i in range(num_classes)], rotation=45)
plt.yticks(tick_marks, [f'Class {i}' for i in range(num_classes)])

plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')

for i in range(num_classes):
    for j in range(num_classes):
        plt.text(j, i, str(cf_m[i, j]), horizontalalignment='center', color='white')

plt.show()
