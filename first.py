import os
import plotly.offline as py
import plotly.graph_objs as go
from data_sources import oanda
from data_sources import tools
import datetime


def display_chart(data, annotations, title):
    layout = go.Layout(title=title, annotations=annotations)
    fig = go.Figure(data=[data], layout=layout)

    py.plot(fig)


def main():
    client = oanda.get_client(os.environ.get('OANDA_API_ACCESS_TOKEN'))

    datetime_from = datetime.datetime(2017, 1, 1, 0, 0, 0)
    datetime_to = datetime.datetime(2017, 7, 6, 0, 0, 0)
    granularity = 'M5'
    instrument = 'EUR_USD'

    response = oanda.get_historical_data(client, instrument=instrument, granularity=granularity,
                                         datetime_from=datetime_from, datetime_to=datetime_to)

    df, annotations = oanda.get_dataframe_and_annotations(response)

    display_chart(df, annotations, '{}, {}'.format(instrument.replace('_', '/'), granularity))


if __name__ == "__main__":
    main()
