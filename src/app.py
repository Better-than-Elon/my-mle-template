import configparser
from flask import Flask
from predict import Predictor

app = Flask(__name__)
predictor = None


@app.route("/predict/<pred_id>")
def get_predict(pred_id):
    X_test = predictor.X_test.iloc[int(pred_id):int(pred_id) + 1]
    y_test = predictor.y_test.iloc[int(pred_id), 0]
    y_pred = predictor.clf.predict(X_test)[0]
    return f'Data:{X_test.iloc[0]} Pred: {y_pred} Real: {y_test}', 200
    
@app.route("/")
def run():
    return "Hello"


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    predictor = Predictor.from_config(config)

    app.run(host="0.0.0.0", port=5000, debug=True)
