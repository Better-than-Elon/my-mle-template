import configparser
import pandas as pd
from sklearn.model_selection import train_test_split


def split(config):
    data = []
    sep = config['data.raw']['sep']
    for k, path in config['data.raw'].items():
        if 'data' in k:
            data.append(pd.read_csv(path, sep=sep))
    data = pd.concat(data)
    X_train, X_test, y_train, y_test = train_test_split(
        data.iloc[:, :-1], data.iloc[:, -1],
        train_size=float(config['data.raw']['train_pers']), random_state=42
    )
    X_train.to_csv(config['data.prep']['train_x'], index=False)
    y_train.to_csv(config['data.prep']['train_y'], index=False)
    X_test.to_csv(config['data.prep']['test_x'], index=False)
    y_test.to_csv(config['data.prep']['test_y'], index=False)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    split(config)
