import configparser
import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score
from src.db_connection import DB_Connection


class Predictor:
    def __init__(self, clf, log_db_table_name='predicts') -> None:
        self.clf = clf
        self.log_db_table_name = log_db_table_name
        self.connection = DB_Connection()


    @classmethod
    def from_config(cls, config: configparser.ConfigParser):
        clf = load(config['train']['save_path'])
        return cls(clf)

    def predict(self, X_test):
        y_pred = self.clf.predict(X_test)
        self.connection.append_df(pd.DataFrame(data={"y_real":y_pred}), self.log_db_table_name)
        return self.clf.predict(X_test)

    def calc_accuracy(self, X_test, y_test) -> float:
        y_pred = self.clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    X_test = pd.read_csv(config['data.prep']['test_x'])
    y_test = pd.read_csv(config['data.prep']['test_y'])

    predictor = Predictor.from_config(config)
    predictor.predict(X_test)
    print(predictor.calc_accuracy(X_test, y_test))
