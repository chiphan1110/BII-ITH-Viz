import json
import pandas as pd

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

def process_classifiers(classifiers):
    purity_errors = {}
    fga_errors = {}

    for classifier_name, json_file in classifiers.items():
        purity_errors[classifier_name] = calculate_abs_error(json_file, "purity")
        fga_errors[classifier_name] = calculate_abs_error(json_file, "FRACTION_GENOME_ALTERED")

    return pd.DataFrame(purity_errors), pd.DataFrame(fga_errors)

def main():
    json_files = {
    'Purity-FGA': 'data\Purity-FGA.json',
    'Staging-Purity-FGA': 'data\Staging-Purity-FGA.json',
    'Subtyping-Purity-FGA': 'data\Subtyping-Purity-FGA.json',
    'Subtyping-Staging-Purity-FGA': 'data\Subtyping-Staging-Purity-FGA.json'
    }

    purity_errors, fga_errors = process_classifiers(json_files)
    purity_errors.to_csv('errors/purity_errors.csv', index_label='Sample')
    fga_errors.to_csv('errors/fga_errors.csv', index_label='Sample')

if __name__ == "__main__":
    main()