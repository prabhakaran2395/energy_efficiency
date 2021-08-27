import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from get_data import read_params
import argparse
import joblib
import json


def eval_metrics(test_y, predictions):
    rmse = np.sqrt(mean_squared_error(test_y, predictions))
    mae = mean_absolute_error(test_y, predictions)
    r2 = r2_score(test_y, predictions)

    return rmse, mae, r2


def train_and_evaluate(config_path):
    config = read_params(config_path)
    train_data_path = config["split_data"]["train_path"]
    test_data_path = config["split_data"]["test_path"]
    random_state = config["base"]["random_state"]
    model_dir = config["model_dir"]

    n_estimators = config["estimators"]["RandomForestRegressor"]["params"]["n_estimators"]
    min_samples_split = config["estimators"]["RandomForestRegressor"]["params"]["min_samples_split"]

    target_1 = config["base"]["target_col_1"]
    target_2 = config["base"]["target_col_2"]

    train = pd.read_csv(train_data_path)
    test = pd.read_csv(test_data_path)

    train_X = train.drop([target_1, target_2], axis=1)
    test_X = test.drop([target_1, target_2], axis=1)

    train_y = train[[target_1, target_2]]
    test_y = test[[target_1, target_2]]

    scaler = StandardScaler()
    rf_model = RandomForestRegressor(n_estimators=n_estimators,
                                     min_samples_split=min_samples_split,
                                     random_state=random_state)

    model_pipe = Pipeline(steps=[('scaler', scaler),
                                 ('rf_model', rf_model)])

    model_pipe.fit(train_X, train_y)

    predictions = model_pipe.predict(test_X)

    (rmse, mae, r2) = eval_metrics(test_y, predictions)

    scores_file = config["reports"]["scores"]
    params_file = config["reports"]["params"]

    with open(scores_file, "w") as f:
        scores = {
            "rmse": rmse,
            "mae": mae,
            "r2": r2
        }
        json.dump(scores, f, indent=4)

    with open(params_file, "w") as f:
        params = {
            "n_estimators": n_estimators,
            "min_samples_split": min_samples_split
        }
        json.dump(params, f, indent=4)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'rf_model.joblib')

    joblib.dump(model_pipe, model_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="params.yaml")
    parsed_args = parser.parse_args()
    train_and_evaluate(config_path=parsed_args.config)
