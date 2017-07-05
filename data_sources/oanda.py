import oandapy
from dateutil import parser
import pandas as pd
from patterns import pinbar
import plotly.graph_objs as go


def get_client(oanda_access_token):
    return oandapy.API(environment="practice", access_token=oanda_access_token)


def get_historical_data(client, instrument, granularity, count):
    return client.get_history(instrument=instrument, granularity=granularity, count=count)


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

        pinbar_status = pinbar.get_pinbar_status(item['open'], item['high'], item['low'], item['close'])

        if pinbar_status['is_valid'] is True:
            annotations.append({
                'x': parsed_time,
                'showarrow': True,
                'y': candle['highBid'] + 0.00005, 'xref': 'x', 'yref': 'y',
                'text': '{}'.format(pinbar_status['type'])
            })

    return pd.DataFrame(items), annotations


def get_dataframe_and_annotations(oanda_response):
    data, annotations = convert_oanda_request_to_panda_dataframe_and_annotations(oanda_response)

    return go.Candlestick(x=data.time,
                          open=data.open,
                          high=data.high,
                          low=data.low,
                          close=data.close), annotations
