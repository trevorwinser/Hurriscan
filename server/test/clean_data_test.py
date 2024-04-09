import pandas as pd
import numpy as np
from pathlib import Path
import pytest

# Define pytest fixtures
@pytest.fixture
def data():
    # Construct the file path for test data
    current_file_dir = Path(__file__).parent
    data_file_path = current_file_dir / '..' / '..' / 'data' / 'cleaned_data.csv'
    absolute_data_file_path = data_file_path.resolve()

    # Load and return the test data
    test_data = pd.read_csv(absolute_data_file_path)
    return test_data

@pytest.fixture
def expected_data_types():
    # Define the expected data types for columns
    return {
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

def test_no_na_rows(data):
    assert data.isna().sum().sum() == 0, "Some rows contain NA values."

def test_random_row(data):
    random_index = np.random.randint(0, len(data))
    assert data.iloc[random_index].isna().sum() == 0, f"Row {random_index} contains NA values."

def test_data_types(data, expected_data_types):
    for column, expected_type in expected_data_types.items():
        # Only perform the check if the column exists in the data
        if column in data.columns:
            assert data[column].dtype == expected_type, f"Column '{column}' has incorrect data type."
