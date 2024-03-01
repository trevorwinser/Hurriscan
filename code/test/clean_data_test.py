import pandas as pd

def test_no_na_rows():
    # Read the cleaned data from the CSV file
    data = pd.read_csv('../../data/cleaned_data.csv')

    # Check if any rows contain NA values
    assert data.isna().sum().sum() == 0, "Some rows contain NA values."

# Run the test
test_no_na_rows()