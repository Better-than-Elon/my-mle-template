import configparser
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from joblib import dump

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')

    X_train = pd.read_csv(config['data.prep']['train_x'])
    y_train = pd.read_csv(config['data.prep']['train_y'])
    X_test = pd.read_csv(config['data.prep']['test_x'])
    y_test = pd.read_csv(config['data.prep']['test_y'])

    clf = RandomForestClassifier(n_estimators=int(config['random_forest']['n_estimators']),
                                 random_state=int(config['random_forest']['random_state']), )
    print('Training...')
    clf = clf.fit(X_train, y_train.iloc[:, 0])
    print('Saving model...')
    dump(clf, config['random_forest']['save_path'])

    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy:\t{accuracy}')
