
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl


def is_valid_dataset(df):
    """
        This function validates the dataset by analyzing
        and ensuring all the required fields are present or not
        
        Args:
            df: DataFrame

        Returns:
            'True' if dataset is valid else 'False'
        Example:
            >>> import pandas as pd
            >>> df = pd.DataFrame({'Date': [], 'Region': [], 'Death': [], 'Active Cases': [], 'Recovered': []})
            >>> is_valid_dataset(df)
            True
    """
    df_columns = df.columns
    required_columns = {'Date', 'Region', 'Death', 'Active Cases', 'Recovered'}
    return required_columns.issubset(df.columns)


def slice_by_last_dot(path):
    """
        This method identifies the file extension such as .csv .xlsx etc.
        By slicing the given path by dot
        
        Args:
            path: path of the csv or excel file
        
        Returns:
            the extension of file
    """
    last_dot_index = path.rfind('.')
    
    if last_dot_index == -1:
        return -1
    else:
        return path[last_dot_index:]


def clean_data(df):
    """ 
        This method cleans the data by 
            - Treaming leading and back spaces
            - Standardize the field i.e Date
            - Add Columns such as Day, Month, Year by extracting it from Date
            - Identify and delete NaN or missing value rows

        Args:
            df: DataFrame for cleaning
        
        Returns:
            cleaned DataFrame
    """
    pass


def load_data_from_file(path):
    """ 
        This function loads the data from file take help of functions such as
            - is_valid_dataset(df)
            - slice_by_last_dot(df)
            - clean_data(df)

        Args:    
            path: path of uploaded file
        
        Returns:    
            DataFrame for graph generation
    """   
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
    load_data_from_file('../assets/sample_data.csv')

main()