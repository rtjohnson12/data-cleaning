
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def find_missing():

    covidtotals = pd.read_csv("data/raw/covidtotals.csv")
    totvars = ['location', 'total_cases', 'total_deaths', 'total_cases_pm', 'total_deaths_pm']
    demovars = ['population', 'pop_density', 'median_age', 'gdp_per_capita', 'hosp_beds']

    # check for missing
    covidtotals[demovars].isnull().sum(axis = 0)
    covidtotals[demovars].isnull().sum(axis = 1)




def main():
    pass

if __name__ == "__main__":
    main()
