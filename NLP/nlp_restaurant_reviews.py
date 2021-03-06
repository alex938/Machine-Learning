import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#ignore double quotes (quoting = 3)
dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

#cleaning the text
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

corpus = []

for i in range(0, 1000):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if word not in set(stopwords.words('english'))]
    review = " ".join(review)
    corpus.append(review)
    
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values

#split into training and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

#NB model on the training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

#predict using test set (20%) of data
y_pred = classifier.predict(X_test)

#generate confusion matrix
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)

#function to test a new review
def predict(new_review):   
    new_review = re.sub("[^a-zA-Z]", " ", new_review)
    new_review = new_review.lower().split()
    new_review = [ps.stem(word) for word in new_review if word not in set(stopwords.words("english"))]   
    new_review = " ".join(new_review)   
    new_review = [new_review]   
    new_review = cv.transform(new_review).toarray()   
    if classifier.predict(new_review)[0] == 1:
        return "Positive"   
    else:
        return "Negative"
    
print(predict("poor food"))
