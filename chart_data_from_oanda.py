import datetime
from data_sources.oanda import oanda as oanda
import data_sources.data_transformer as dtf
from charts_generator import charts_plotly


def main():
    datetime_from = datetime.datetime(2017, 7, 1, 0, 0, 0)
    datetime_to = datetime.datetime(2017, 7, 6, 0, 0, 0)
    granularity = 'M15'
    instrument = 'EUR_USD'

    data = oanda.get_historical_data(instrument=instrument,
                                                  granularity=granularity,
                                                  datetime_from=datetime_from,
                                                  datetime_to=datetime_to)

    df, patterns_info = dtf.get_candlesticks_and_patterns(data)

    charts_plotly.display_chart(df, patterns_info,
                                '{}, {}'.format(data['instrument'].replace('_', '/'), data['granularity']))


if __name__ == "__main__":
    main()
