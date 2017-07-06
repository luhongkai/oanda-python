from data_sources.csv import csv as datasource_csv
import data_sources.data_transformer as dtf
import pandas as pd

def main():
    filename = '.\\data\\test_data_analyze.csv'

    data = datasource_csv.get_historical_data(filename)
    df, patterns_info = dtf.get_candlesticks_and_patterns(data)

    df_1 = pd.DataFrame(patterns_info['pinbar']['candle'])
    df_2 = pd.DataFrame(patterns_info['pinbar']['data'])

    print('test')

if __name__ == "__main__":
    main()
