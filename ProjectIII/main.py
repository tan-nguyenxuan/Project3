from pyvi import ViTokenizer, ViPosTagger # thư viện NLP tiếng Việt
from tqdm import tqdm
import numpy as np
import gensim # thư viện NLP
import pickle
import nltk
from nltk.corpus import stopwords
import os 

dir_path = os.path.dirname(os.path.realpath(os.getcwd()))
dir_path = os.path.join(dir_path, 'ProjectIII\DataDemo')
 
stop_word_list = set(stopwords.words('vietnam'))

def get_data(folder_path):
    X = []
    y = []
    dirs = os.listdir(folder_path)
    for path in tqdm(dirs):
        file_paths = os.listdir(os.path.join(folder_path, path))
        for file_path in tqdm(file_paths):
            with open(os.path.join(folder_path, path, file_path), 'r', encoding="utf-8") as f:
                lines = f.readlines()
                for i in range(len(lines)):
                    lines[i] = " ".join([word for word in lines[i].split() if word not in stop_word_list])
                lines = ' '.join(lines)
                lines = gensim.utils.simple_preprocess(lines)
                lines = ' '.join(lines)
                lines = ViTokenizer.tokenize(lines)

                X.append(lines)
                y.append(path)
    return X, y

#train_path = os.path.join(dir_path, 'datatrain')
#X_data, y_data = get_data(train_path)

test_path = os.path.join(dir_path, 'datatest')
X_test, y_test = get_data(test_path)

pickle.dump(X_test, open('DataDemo/X_test.pkl', 'wb'))
pickle.dump(y_test, open('DataDemo/y_test.pkl', 'wb'))