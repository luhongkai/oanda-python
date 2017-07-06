from data_sources.csv import csv as datasource_csv
import data_sources.data_transformer as dtf
from charts_generator import charts_plotly


def main():
    filename = '.\\data\\test_ide.csv'

    data = datasource_csv.get_historical_data(filename)
    df, patterns_info = dtf.get_candlesticks_and_patterns(data)

    charts_plotly.display_chart(df, patterns_info,
                                '{}, {}'.format(data['instrument'].replace('_', '/'), data['granularity']))


if __name__ == "__main__":
    main()
