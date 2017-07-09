from data_sources.csv import csv as datasource_csv
import data_sources.data_transformer as dtf
import pandas as pd
import datetime


def main():
    filename = '.\\data\\test_data_analyze.csv'

    data = datasource_csv.get_historical_data(filename)
    df, patterns_info = dtf.get_candlesticks_and_patterns(data)

    df_pinbars = pd.DataFrame(patterns_info['pinbar'])
    df_pinbars.set_index([df_pinbars.time.apply(lambda x: datetime.datetime.date(x))], inplace=True)
    df_pinbars.index.names = ['date']

    df_group = df_pinbars.groupby([df_pinbars.index])

    print('test')

if __name__ == "__main__":
    main()
