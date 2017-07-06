from dateutil import parser
import plotly.offline as py
import plotly.graph_objs as go
import datetime
from data_sources.oanda import oanda as oanda


def get_annotations_from_patterns_info(patterns_info):
    annotations = list()

    if 'pinbar' in patterns_info:
        for pinbar in patterns_info['pinbar']:
            annotations.append({
                'x': parser.parse(pinbar['candle']['time']),
                'showarrow': True,
                'y': pinbar['candle']['highBid'] + 0.00005, 'xref': 'x', 'yref': 'y',
                'text': '{}'.format(pinbar['data']['type'])
            })

    return annotations


def display_chart(data, patterns_info, title):
    layout = go.Layout(title=title, annotations=get_annotations_from_patterns_info(patterns_info))
    fig = go.Figure(data=[data], layout=layout)

    py.plot(fig)


def main():
    datetime_from = datetime.datetime(2017, 7, 1, 0, 0, 0)
    datetime_to = datetime.datetime(2017, 7, 6, 0, 0, 0)
    granularity = 'M15'
    instrument = 'EUR_USD'

    df, patterns_info = oanda.get_historical_data_as_dataframe_and_patterns_info(instrument=instrument,
                                                                               granularity=granularity,
                                                                               datetime_from=datetime_from,
                                                                               datetime_to=datetime_to)

    display_chart(df, patterns_info, '{}, {}'.format(instrument.replace('_', '/'), granularity))


if __name__ == "__main__":
    main()
