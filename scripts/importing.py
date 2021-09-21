
import pandas as pd
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



def main():
    print("Hello, World!")
    # import_csv()
    # improt_excel()


if __name__ == "__main__":
    main()
