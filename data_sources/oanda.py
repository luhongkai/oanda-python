import oandapy
from dateutil import parser
import pandas as pd
from patterns import pinbar
import plotly.graph_objs as go
import data_sources.tools as tools
import sys


MAX_BARS_IN_ONE_REQUEST = 5000


def get_client(oanda_access_token):
    return oandapy.API(environment="practice", access_token=oanda_access_token)


def get_datetime_for_api_argument(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S.000000Z')


def get_historical_data(client, instrument, granularity, datetime_from, datetime_to):
    ranges_to_fetch = tools.get_datetime_ranges_to_fetch(datetime_from, datetime_to, granularity,
                                                         MAX_BARS_IN_ONE_REQUEST)

    final_response = dict(instrument=None, granularity=None, candles=list())

    to_complete = len(ranges_to_fetch)
    completed_items = 0
    completed_percent = 0
    print('Downloading data ({}%)'.format(completed_percent), end='\r')
    sys.stdout.flush()

    for range_data in ranges_to_fetch:
        response = client.get_history(instrument=instrument, granularity=granularity,
                                  start=get_datetime_for_api_argument(range_data['datetime_from']),
                                  end=get_datetime_for_api_argument(range_data['datetime_to']))

        if final_response['instrument'] is None and final_response['granularity'] is None:
            final_response['instrument'] = response['instrument']
            final_response['granularity'] = response['granularity']

        final_response['candles'].extend(response['candles'])

        completed_items = completed_items + 1
        completed_percent = round((completed_items / to_complete) * 100)
        print('Downloading data ({}%)'.format(completed_percent), end='\r')
        sys.stdout.flush()

    print('')
    sys.stdout.flush()

    return final_response


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
