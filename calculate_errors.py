import os
import json
import pandas as pd


def generate_file_dicts(dir):
    json_files = {}
    sorted_filenames = sorted(os.listdir(dir), key= lambda x: len(x))
    for filename in sorted_filenames:
        if filename.endswith(".json"):
            key_name = filename.replace('.json', '')
            file_path = os.path.join(dir, filename)
            json_files[key_name] = file_path
    
    return json_files        


def calculate_abs_error(json_file, target):
    with open(json_file, 'r') as f:
        data = json.load(f)

    abs_error = []

    for _, value in data.items():
        pred = value.get(target, {}).get('pred')
        label = value.get(target, {}).get('label')
        if pred is None or label is None:
            continue
        error = round(abs(pred - label), 3)
        abs_error.append(error)   
    return abs_error


def numerical_task_error(classifiers):
    purity_errors = {}
    fga_errors = {}

    for classifier_name, json_file in classifiers.items():
        if 'Purity' in classifier_name:
            purity_errors[classifier_name] = calculate_abs_error(json_file, "purity")
        if 'FGA' in classifier_name:
            fga_errors[classifier_name] = calculate_abs_error(json_file, "FRACTION_GENOME_ALTERED")

    return pd.DataFrame(purity_errors), pd.DataFrame(fga_errors)


def main():
    json_dir = 'data'
    json_files = generate_file_dicts(json_dir)

    purity_errors, fga_errors = numerical_task_error(json_files)
    purity_errors.to_csv('errors/purity.csv', index_label='Sample')
    fga_errors.to_csv('errors/fga.csv', index_label='Sample')


if __name__ == "__main__":
    main()
