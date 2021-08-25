import os
import yaml
import pandas as pd
import argparse
from get_data import get_data, read_params

def load_and_save(config_path):
    config = read_params(config_path)
    df = get_data(config_path)
    column_names = ['Relative_Compactness', 'Surface_Area', 'Wall_Area',
    'Roof_Area', 'Overall_Height', 'Orientation', 'Glazing_Area',
    'Glazing_Area_Distribution', 'Heating_Load', 'Cooling_Load'
    ]

    df.columns = column_names

    raw_data_path = config["load_data"]["raw_dataset_csv"]
    df.to_csv(raw_data_path, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="params.yaml")
    parsed_args = parser.parse_args()
    load_and_save(config_path=parsed_args.config)
