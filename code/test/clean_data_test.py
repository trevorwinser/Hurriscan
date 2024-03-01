import pandas as pd
import numpy as np

def test_no_na_rows(data):
    assert data.isna().sum().sum() == 0, "Some rows contain NA values."

def test_random_row(data):
    assert data.iloc[np.random.randint(0, len(data))].isna().sum() == 0, f"Row {random_index} contains NA values."

def test_data_types(data):
    expected_data_types = {
        'obs': 'int64',
        'year': 'int64',
        'month': 'int64',
        'day': 'int64',
        'date': 'int64',
        'latitude': 'float64',
        'longitude': 'float64',
        'zon.winds': 'float64',
        'mer.winds': 'float64',
        'humidity': 'float64',
        'air': 'float64',
        'temp.': 'float64'
    }

    for column, expected_type in expected_data_types.items():
        assert data[column].dtype == expected_type, f"Column '{column}' has incorrect data type."

def run_tests():
    data = pd.read_csv('../../data/cleaned_data.csv')
    test_no_na_rows(data)
    test_random_row(data)
    test_data_types(data)


run_tests()