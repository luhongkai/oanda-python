import oandapy
import os
import plotly.offline as py
import plotly.graph_objs as go
from dateutil import parser
import pandas as pd


def display_chart(data, title):

    layout = go.Layout(title=title, annotations=data['annotations'])
    fig = go.Figure(data=[data['data']], layout=layout)

    py.plot(fig)


def oanda_candles_to_pytly_chart_item(oanda_response):
    data = convert_oanda_request_to_panda_dataframe_and_annotations(oanda_response)

    return dict(data=go.Candlestick(x=data['data'].time,
                          open=data['data'].open,
                          high=data['data'].high,
                          low=data['data'].low,
                          close=data['data'].close), annotations=data['annotations'])


def convert_oanda_request_to_panda_dataframe_and_annotations(oanda_response):
    items = list()
    annotations = list()

    for candle in oanda_response['candles']:
        parsed_time = parser.parse(candle['time'])

        item = dict(time=parsed_time,
                    open=candle['openBid'],
                    high=candle['highBid'],
                    low=candle['lowBid'],
                    close=candle['closeBid'])

        items.append(item)

        if candle['time'] in ['2017-07-05T03:00:00.000000Z', '2017-07-05T03:45:00.000000Z']:
            annotations.append({
                'x': parsed_time,
                'showarrow': True,
                'y': candle['highBid'], 'xref': 'x', 'yref': 'y',
                'text': 'My first annotation :)'
            })

    return dict(data=pd.DataFrame(items), annotations=annotations)


def is_pinbar(open, high, low, close):
    if open > close:
        # PinBar to short
        body_size = open - close
        top_tail_size = high - open
        bottom_tail_size = close - low

    return False


def main():
    oanda_access_token = os.environ.get('OANDA_API_ACCESS_TOKEN')
    oanda = oandapy.API(environment="practice", access_token=oanda_access_token)

    how_many_hours_back = 12
    bars_in_hour = 4
    bars_count = int(bars_in_hour * how_many_hours_back)

    response = oanda.get_history(instrument='EUR_USD', granularity='M5', count=bars_count)

    display_chart(oanda_candles_to_pytly_chart_item(response), 'EUR/USD, 15min')


if __name__ == "__main__":
    main()
