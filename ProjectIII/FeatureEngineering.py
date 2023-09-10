import pickle
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn import naive_bayes
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit, learning_curve
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from gensim import corpora, matutils
from sklearn.metrics import classification_report

X_data = pickle.load(open('DataDemo/X_data.pkl', 'rb'))
y_data = pickle.load(open('DataDemo/y_data.pkl', 'rb'))

X_test = pickle.load(open('DataDemo/X_test.pkl', 'rb'))
y_test = pickle.load(open('DataDemo/y_test.pkl', 'rb'))

# word level - we choose max number of words equal to 30000 except all words (100k+ words)
tfidf_vect = TfidfVectorizer(analyzer='word', max_features=30000)
tfidf_vect.fit(X_data) # learn vocabulary and idf from training set
X_data_tfidf =  tfidf_vect.transform(X_data)
# assume that we don't have test set before
X_test_tfidf =  tfidf_vect.transform(X_test)

svd = TruncatedSVD(n_components=300, random_state=42)
svd.fit(X_data_tfidf)

X_data_tfidf_svd = svd.transform(X_data_tfidf)
X_test_tfidf_svd = svd.transform(X_test_tfidf)

encoder = preprocessing.LabelEncoder()
y_data_n = encoder.fit_transform(y_data)
y_test_n = encoder.fit_transform(y_test)

encoder.classes_

def train_model(classifier, X_data, y_data, X_test, y_test, is_neuralnet=False, n_epochs=3):       
    X_train, X_val, y_train, y_val = train_test_split(X_data, y_data, test_size=0.1, random_state=42)
    
    if is_neuralnet:
        classifier.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=n_epochs, batch_size=512)
        
        val_predictions = classifier.predict(X_val)
        test_predictions = classifier.predict(X_test)
        val_predictions = val_predictions.argmax(axis=-1)
        test_predictions = test_predictions.argmax(axis=-1)
    else:
        classifier.fit(X_train, y_train)
    
        train_predictions = classifier.predict(X_train)
        val_predictions = classifier.predict(X_val)
        test_predictions = classifier.predict(X_test)
        print("Train accuracy: ", metrics.accuracy_score(train_predictions, y_train))
    
        
    print("Validation accuracy: ", metrics.accuracy_score(val_predictions, y_val))
    print("Test accuracy: ", metrics.accuracy_score(test_predictions, y_test))
    
#train_model(naive_bayes.MultinomialNB(), X_data_tfidf, y_data, X_test_tfidf, y_test, is_neuralnet=False)
#train_model(naive_bayes.GaussianNB(), X_data_tfidf_svd, y_data, X_test_tfidf_svd, y_test, is_neuralnet=False)

class Classifier(object):
    def __init__(self, features_train = None, labels_train = None, features_test = None, labels_test = None,  estimator = None):
        self.features_train = features_train
        self.features_test = features_test
        self.labels_train = labels_train
        self.labels_test = labels_test
        self.estimator = estimator

    def training(self):
        self.estimator.fit(self.features_train, self.labels_train)
        self.__training_result()

    #def save_model(self, filePath):
    #    FileStore(filePath=filePath).save_pickle(obj=est)

    def __training_result(self):
        y_true, y_pred = self.labels_test, self.estimator.predict(self.features_test)
        print(classification_report(y_true, y_pred))
        X_train, X_val, y_train, y_val = train_test_split(self.features_train, self.labels_train, test_size=0.1, random_state=42)
        train_predictions = self.estimator.predict(X_train)
        val_predictions = self.estimator.predict(X_val)
        test_predictions = self.estimator.predict(self.features_test)
        print("Train accuracy: ", metrics.accuracy_score(train_predictions, y_train))    
        print("Validation accuracy: ", metrics.accuracy_score(val_predictions, y_val))
        print("Test accuracy: ", metrics.accuracy_score(test_predictions, self.labels_test))
        
        
#est = Classifier(features_train=X_data_tfidf_svd, features_test=X_test_tfidf_svd, labels_train=y_data, labels_test=y_test, estimator=naive_bayes.GaussianNB())
#est.training()

print(X_data)

