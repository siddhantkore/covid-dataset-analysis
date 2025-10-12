
# clean and take 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl


def is_valid_dataset(path):
    pass

def slice_by_last_dot(path):
    last_dot_index = path.rfind('.')
    
    if last_dot_index == -1:
        return -1
    else:
        return path[last_dot_index:]
    
def load_data_from_file(path):
   
    file_extension = slice_by_last_dot(path)
    print(file_extension)
    print(path)
    
    if file_extension == '.csv':
        try:
            df = pd.read_csv(path)
            print("Successfully read CSV:")
            print(df.head()) # Use .head() to avoid printing a very large DataFrame

            return df
        except FileNotFoundError:
            print(f"Error: CSV file not found at {path}")
    elif file_extension == '.xlsx':
        try:
            df = pd.read_excel(path)
            print("Successfully read Excel:")
            print(df.head()) # Use .head() to avoid printing a very large DataFrame
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

def main():
    abc('assets/sample_data.csv')

main()