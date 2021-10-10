
import pandas as pd
import numpy as np
from pandas.io.formats.style import no_mpl_message
import matplotlib.pyplot as plt

def first_look():
    nls97 = pd.read_csv("data/raw/nls97.csv")
    covidtotals = pd.read_csv("data/raw/covidtotals.csv", parse_dates = ['lastdate'])

    # set index and check whether index values are unique
    nls97.set_index('personid', inplace = True)
    nls97.index
    nls97.shape
    nls97.index.nunique()

    # show data types and non-null value counts
    nls97.info()

    # show the first row of the data
    nls97.head(2).T

    # set index for COVID data
    covidtotals.set_index("iso_code", inplace = True)
    covidtotals.index.nunique()
    covidtotals.shape
    covidtotals.info()

def select_cols():
    # get data
    nls97 = pd.read_csv("data/raw/nls97.csv")
    nls97.set_index("personid", inplace = True)
    nls97.loc[:, nls97.dtypes == "object"] = \
        nls97.select_dtypes(['object']). \
        apply(lambda x: x.astype('category'))

    # select cols using [], loc, and iloc
    nls97['gender'].__class__ # series
    nls97[['gender']].__class__ # dataframe
    nls97.loc[:, ['gender']].__class__
    nls97.iloc[:, [0]].__class__

    nls97[['gender', 'maritalstatus', 'highestgradecompleted']]
    nls97.loc[:, ['gender', 'maritalstatus', 'highestgradecompleted']]
    
    # select multiple columns based on a list
    keyvars = ['gender', 'maritalstatus', 'highestgradecompleted', 'wageincome', 'gpaoverall', 'weeksworked17', 'colenroct17']
    analysiskeys = nls97[keyvars]
    analysiskeys.info()
    analysiskeys.index

    # filter on column name/type
    nls97.filter(like = "weeksworked")
    nls97.select_dtypes(['category'])
    nls97.select_dtypes('number')
    nls97.select_dtypes(exclude = ['category'])

def select_rows():
    nls97 = pd.read_csv("data/raw/nls97.csv")
    nls97.set_index("personid", inplace = True)
    
    # slice
    nls97[1000:1004].T
    nls97[0:4].T
    nls97.iloc[0:4].T
    nls97.iloc[[0]]

    # select rows conditionally using boolean indexing
    nls97.nightlyhrssleep.quantile(0.05)
    nls97.nightlyhrssleep.count()
    nls97.loc[nls97.nightlyhrssleep <= 4.0]

    nls97.loc[(nls97.nightlyhrssleep <= 4.0) & (nls97.childathome >= 3), ['nightlyhrssleep', 'childathome']]

def generate_freq():
    "90% of what we're going to find, we'll see in the frequency distributions"
    nls97 = pd.read_csv("data/raw/nls97.csv")
    nls97.set_index("personid", inplace = True)
    nls97.loc[:, nls97.dtypes == 'object'] = nls97.select_dtypes('object').apply(lambda x: x.astype('category'))

    nls97.loc[:, nls97.dtypes == "category"].isnull().sum()
    nls97.maritalstatus.value_counts(sort = False, normalize = True)

    # show %s for all gov resp columns
    nls97.filter(like = "gov").apply(pd.value_counts, normalize = True, sort = False)
    nls97[nls97.maritalstatus == "Married"].filter(like = "gov").apply(pd.value_counts, normalize = True, sort = False)

    # find freq and perc for all category columns
    freqout = open("data/interim/frequencies.txt", "w")
    for col in nls97.select_dtypes("category"):
        print(col, "-----------", "frequencies", nls97[col].value_counts(sort = False), "percentages", nls97[col].value_counts(sort = False, normalize = True), sep = "\n\n", end = "\n\n\n", file = freqout)
    freqout.close()

def summary_stats():
    covidtotals = pd.read_csv("data/raw/covidtotals.csv", parse_dates = ["lastdate"])
    covidtotals.set_index("iso_code", inplace = True)

    # shape and structure of the data
    covidtotals.shape
    covidtotals.sample(2, random_state = 1).T
    covidtotals.dtypes
    covidtotals.describe()

    # distribution of values for cases and deaths column
    totvars = ['location', 'total_cases', 'total_deaths', 'total_cases_pm', 'total_deaths_pm']
    covidtotals[totvars].quantile(np.arange(0.0, 1.1, 0.1))

    # view distribution of total cases
    plt.hist(covidtotals['total_cases']/1000, bins = 12)
    plt.title("Total Covid Cases")
    plt.xlabel("Cases")
    plt.ylabel("Number of Counties")
    plt.show()



def main():
    print("Hello, World!")

if __name__ == "__main__": 
    main()
