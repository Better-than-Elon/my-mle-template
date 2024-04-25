import configparser
import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score
from src.kafka_connection import KafkaSingleConnection


class Predictor:
    def __init__(self, clf, log_db_table_name='predicts') -> None:
        self.clf = clf
        self.log_db_table_name = log_db_table_name


    @classmethod
    def from_config(cls, config: configparser.ConfigParser):
        clf = load(config['train']['save_path'])
        return cls(clf)

    def predict(self, X_test):
        y_pred = self.clf.predict(X_test)
        connection = KafkaSingleConnection(self.log_db_table_name, 1)
        connection.send(y_pred.tolist())
        connection.close()
        return y_pred

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

