import configparser
from flask import Flask, request
from src.predict import Predictor
import pandas as pd

app = Flask(__name__)
app.json.sort_keys = False


@app.route("/get-test/<pred_id>")
def get_test_json(pred_id):
    X = X_test_df.iloc[int(pred_id)]
    y = y_test_df.iloc[int(pred_id)]
    return {"X": [X.to_dict()], "y": [y.to_dict()]}

@app.route('/predict', methods=['POST'])
def predict():
    res = request.json
    df = pd.DataFrame.from_records(res['X'])
    y_real = pd.DataFrame.from_records(res['y']).iloc[:, 0].tolist()
    y_pred = predictor.predict(df).tolist()
    return {"y_real":y_real, "y_pred": y_pred}
    
@app.route("/")
def run():
    return "Hello"


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    X_test_df = pd.read_csv(config['data.prep']['test_x'])
    y_test_df = pd.read_csv(config['data.prep']['test_y'])
    predictor = Predictor.from_config(config)

    app.run(host="0.0.0.0", port=5000, debug=True)
