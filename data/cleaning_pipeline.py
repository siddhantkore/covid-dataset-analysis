

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

"""
    This function validates the dataset by analyzing
    and ensuring all the required fields are present or not
    :param df: DataFrame
    :return: 'True' if dataset is valid else 'False' 
"""
def is_valid_dataset(df):
    df_columns = df.columns
    if df_columns.contains(['Date', 'Region', 'Death', 'Active Cases', 'Recovered']):
        return True
    return False


"""
    This method identifies the file extension such as .csv .xlsx etc.
    By slicing the given path by dot
    :param path: path of the csv or excel file
    :return: the extension of file
"""
def slice_by_last_dot(path):
    last_dot_index = path.rfind('.')
    
    if last_dot_index == -1:
        return -1
    else:
        return path[last_dot_index:]


""" 
    This method cleans the data by 
        - Treaming leading and back spaces
        - Standardize the field i.e Date
        - Add Columns such as Day, Month, Year by extracting it from Date
        - Identify and delete NaN or missing value rows
    :param df: DataFrame for cleaning
    :return: cleaned DataFrame
"""
def clean_data(df):
    pass


""" 
    This function loads the data from file
    take help of functions such as
        - is_valid_dataset(df)
        - slice_by_last_dot(df)
        - clean_data(df)
    :param path: path of uploaded file
    :return: DataFrame for graph generation
"""
def load_data_from_file(path):
   
    file_extension = slice_by_last_dot(path)
    print(file_extension)
    print(path)
    
    if file_extension == '.csv':
        try:
            df = pd.read_csv(path)
            if is_valid_dataset(df):
                return clean_data(df)

            print("Successfully read CSV:")
            print(df.head())

        except FileNotFoundError:
            print(f"Error: CSV file not found at {path}")
            raise FileNotFoundError

    elif file_extension == '.xlsx':
        try:
            df = pd.read_excel(path)
            print("Successfully read Excel:")
            print(df.head())
            return df
        except FileNotFoundError:
            print(f"Error: Excel file not found at {path}")
        except Exception as e:
            print(f"Error reading Excel file: {e}")

    elif file_extension == '.tsv':
        try:
            pass
        except Exception as e:
            pass
    else:
        print(f"Unsupported file type for path: {path}")
        raise Exception


## Test
def main():
    abc('assets/sample_data.csv')

main()