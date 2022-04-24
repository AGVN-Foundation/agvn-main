# sklearn core

# https://en.wikipedia.org/wiki/Semi-supervised_learning
# import datasets/abcnews-date-text.csv
# read it
# split it into train and test for self labeling
# train it
# test it

import pandas as pd
import numpy as np
# import train_test_split
from sklearn.model_selection import train_test_split

data = pd.read_csv('datasets/abcnews-date-text.csv', verbose=True)

# 80-20 split
X_train, X_test, y_train, y_test = train_test_split(data['publish_date'], data['headline_text'], test_size=0.2, random_state=42)

# print data
print("X_train:", X_train)
print("X_test:", X_test)
print("y_train:", y_train)
print("y_train:", y_test)

# select NLP model
