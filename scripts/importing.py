
import pandas as pd
import numpy as np
import pymssql
import pyreadstat

pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 12)

def import_csv():
    landtemps = pd.read_csv(
        'data/raw/landtempssample.csv'
        , names = ['stationid', 'year', 'month', 'avgtemp', 'latitude', 'longitude', 'elevation', 'station', 'countryid', 'county']
        , skiprows = 1
        , parse_dates = [['month', 'year']]
        , low_memory = False
    )

    # initial exploration
    landtemps.head(5)
    landtemps.dtypes
    landtemps.shape

    # rename & check for NULL
    landtemps.rename(columns={'month_year':'measuredate'}, inplace = True)
    landtemps.avgtemp.describe()
    landtemps.isnull().sum()

    # drop NA
    landtemps.dropna(subset = ['avgtemp', 'county']).shape

def import_excel():
    percapitaGDP = pd.read_excel(
        "data/raw/GDPpercapita.xlsx"
        , sheet_name = "OECD.Stat export"
        , skiprows = 4
        , skipfooter = 1
        , usecols = "A, C:T"
    )

    percapitaGDP.head()
    percapitaGDP.info()
    percapitaGDP.rename(columns = {'Year': 'metro'}, inplace = True)
    percapitaGDP.metro.str.startswith(' ').any()
    percapitaGDP.metro.str.endswith(' ').any()
    percapitaGDP.metro = percapitaGDP.metro.str.strip()

    for col in percapitaGDP.columns[1:]:
        percapitaGDP[col] = pd.to_numeric(percapitaGDP[col], errors = "coerce")
        percapitaGDP.rename(columns = {col: 'pcGDP' + col}, inplace = True)

    percapitaGDP.head()
    percapitaGDP.dtypes
    percapitaGDP.describe()

    percapitaGDP.dropna(subset = percapitaGDP.columns[1:], how = "all", inplace = True)

    percapitaGDP.metro.count()
    percapitaGDP.set_index('metro', inplace = True)
    percapitaGDP.head()

def import_SQL():
    query = "SELECT studentid, school, sex, age, famsize, medu as mothereducation, fedu as fathereducation, traveltime, studytime, failures, famrel, freetime, goout, g1 as gradeperiod1, g2 as gradeperiod2, g3 as gradeperiod3 FROM studentmath"
    server = "pdcc.c9sqqzd5fulv.us-west-2.rds.amazonaws.com"
    user = "pdccuser"
    password = "pdccpass"
    database = "pdcctest"
    conn = pymssql.connect(server = server, user = user, password = password, database = database)

    studentmath = pd.read_sql(query, conn)
    conn.close()

    studentmath.head()
    studentmath.dtypes

    newcolorder = ['studentid', 'gradeperiod1', 'gradeperiod2', 'gradeperiod3', 'school', 'sex', 'age', 'famsize', 'mothereducation', 'fathereducation', 'traveltime', 'studytime', 'freetime', 'failures', 'famrel', 'goout']
    studentmath = studentmath[newcolorder]

    # confirm that each row has an ID and that the IDs are unique
    studentmath.studentid.count()
    studentmath.studentid.nunique()
    studentmath.set_index("studentid", inplace = True)

    # replace coded data with more informative values
    setvalues = {"famrel": {1: "1:very bad", 2: "2:bad", 3: "3:neutral", 4: "4:good", 5: "5:excellent"}, "freetime": {1: "1:very low", 2: "2:low", 3: "3:neutral", 4: "4:high", 5: "5:very high"}, "goout": {1: "1:very low", 2: "2:low", 3: "3:neutral", 4: "4:high", 5: "5:very high"}, "mothereducation": {0: np.nan, 1: "1:k-4", 2: "2:5-9", 3: "3:secondary ed", 4: "4:higher ed"}, "fathereducation": {0: np.nan, 1: "1:k-4", 2: "2:5-9", 3: "3:secondary ed", 4: "4:higher ed"}}
    studentmath.replace(setvalues, inplace = True)
    setvalueskeys = [k for k in setvalues]

    # change the type for columns with changed data to category
    studentmath[setvalueskeys].memory_usage(index = False)
    for col in studentmath[setvalueskeys].columns:
        studentmath[col] = studentmath[col].astype('category')
    studentmath[setvalueskeys].memory_usage(index = False)

    # calculate percentages for values in the `famrel` column
    studentmath['famrel'].value_counts(sort = False, normalize = True)
    studentmath.mothereducation.value_counts(sort = False, normalize = True)

    # use apply to calculate percentages for multiple columns
    studentmath[['freetime', 'goout']].apply(pd.Series.value_counts, sort = False, normalize = True)
    studentmath[['mothereducation', 'fathereducation']].apply(pd.Series.value_counts, sort = False, normalize = True)

def import_stat(): 
    # Importing SPPS, Stata, and SAS data
    nls97spss, metaspss = pyreadstat.read_sav('data/raw/nls97.sav')
    nls97spss.dtypes
    nls97spss.head()

    # grab metadata to improve column labels and value labels
    metaspss.variable_value_labels['R0536300']
    metaspss.variable_value_labels

    nls97spss['R0536300'].map(metaspss.variable_value_labels['R0536300']).value_counts(normalize = True)
    nls97spss = pyreadstat.set_value_labels(nls97spss, metaspss, formats_as_category = True)

    nls97spss.columns = metaspss.column_labels
    nls97spss['KEY!SEX (SYMBOL) 1997'].value_counts(normalize = True)
    nls97spss.dtypes

    nls97spss.columns = nls97spss.columns.\
        str.lower().\
        str.replace(' ', '_').\
        str.replace('[^a-z0-9_]', '', regex = True)
    nls97spss.set_index('pubid__yth_id_code_1997', inplace = True)

    # simplify the process by applying value labels from the beginning
    nls97spss, metaspss = pyreadstat.read_sav('data/raw/nls97.sav', apply_value_formats = True, formats_as_category = True)
    nls97spss.columns = metaspss.column_labels
    nls97spss.columns = nls97spss.columns.\
        str.lower().\
        str.replace(' ', '_').\
        str.replace('[^a-z0-9_]', '', regex = True)

    # show the column and a few rows
    nls97spss.dtypes
    nls97spss.head()

    # run frequencies on one of the columns and set the index
    nls97spss.govt_responsibility__provide_jobs_2006.value_counts(sort = False, normalize = True)
    nls97spss.set_index('pubid__yth_id_code_1997', inplace = True)


def main():
    print("Hello, World!")
    # import_csv()
    # import_excel()
    # import_SQL()
    # import_stat()

if __name__ == "__main__":
    main()
