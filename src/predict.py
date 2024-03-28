import configparser
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from joblib import load


def calc_score(X_test, y_test, clf):
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    X_test = pd.read_csv(config['data.prep']['test_x'])
    y_test = pd.read_csv(config['data.prep']['test_y'])
    clf = load(config['train']['save_path'])
    print(calc_score(X_test, y_test, clf))
