import configparser
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import dump


def train(X_train, y_train, clf_cfg):
    if clf_cfg['model_name'] == 'random_forest':
        clf = RandomForestClassifier(n_estimators=int(clf_cfg['n_estimators']),
                                     random_state=int(clf_cfg['random_state']), )
    else:
        clf = RandomForestClassifier()
    print('Training...')
    clf = clf.fit(X_train, y_train)
    print('Saving model...')
    dump(clf, clf_cfg['save_path'])
    print('Training finished')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    X_train = pd.read_csv(config['data.prep']['train_x'])
    y_train = pd.read_csv(config['data.prep']['train_y'])
    clf_cfg = config['train']
    train(X_train, y_train, clf_cfg)
