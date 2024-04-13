import os

import pytest

from src.train import Trainer
from src.predict import Predictor
from src.db_connection import DB_Connection
import numpy as np
import shutil


@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before your test, for example:
    os.makedirs("tests/tmp", exist_ok=True)  # ... do something to check the existing files
    # A test function will be run at this point
    yield
    # Code that will run after your test, for example:
    shutil.rmtree('tests/tmp')


def test_train():
    n, m = 50, 10
    X_train = np.random.rand(n, m) * 100
    y_train = np.random.randint(10, size=n)
    clf_cfg = {
        'model_name': 'random_forest',
        'n_estimators': 100,
        'criterion': 'gini',
        'random_state': 42,
        'save_path': 'tests/tmp/rf.joblib',
    }
    Trainer(X_train, y_train, clf_cfg).train()
    assert os.path.exists(clf_cfg['save_path'])


def test_predict_1():
    class ToyClf():
        def predict(self, x):
            return np.zeros(x.shape[0])

    n, m = 50, 10
    X = np.random.rand(n, m) * 100
    y = np.zeros(n)

    acc = Predictor(ToyClf()).calc_accuracy(X, y)
    assert acc == 1


def test_predict_2():
    class ToyClf():
        def predict(self, x):
            return np.array([1, 2, 3, 4, 5, 5, 4, 3, 2, 1])

    n, m = 50, 10
    X = np.random.rand(n, m) * 100
    y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    acc = Predictor(ToyClf()).calc_accuracy(X, y)
    assert acc == 0.5

def test_predict_db():
    table_name = 'test_predict_db'
    connection = DB_Connection()
    connection.drop(table_name)

    class ToyClf():
        def predict(self, x):
            return np.random.rand(x.shape[0])

    n, m = 50, 10
    X = np.random.rand(n, m) * 100
    Predictor(ToyClf(), table_name).predict(X)
    from_db = connection.get_df(table_name)
    assert len(from_db) == n
    Predictor(ToyClf(), table_name).predict(X)
    from_db = connection.get_df(table_name)
    assert len(from_db) == 2*n
