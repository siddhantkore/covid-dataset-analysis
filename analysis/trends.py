
#3 chart generation

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class DataFrameOfCovid:
    def __init__(self, df):
        self.df = df
    
    def get_values_by_month(month):
        return df[df['month']]

    def get_values_by_year(year):
        pass

    def get_values_by_region(region):
        pass

    def get_values_by_():
        pass
        


class Plot:
    def __init__(self):
        pass

    def plot_bar_graph():
        pass

    def plot_scatter_graph():
        pass

    def plot_line_graph():
        pass

def main():

    path = input("Give Dataset Path ")
    try:
        dataframe = pd.read_csv(path)
        df = DataFrameOfCovid(dataframe)


    except Exception as e:
        print(e)
    finally:
        pass
