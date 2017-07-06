import pandas as pd
import plotly.graph_objs as go
from dateutil import parser
from patterns import pinbar
from patterns.pinbar import PATTERN_TYPE_PINBAR


def transform_data_to_panda_dataframe_and_patterns_info(historical_data):
    items = list()
    patterns = dict(pinbar=list())

    for candle in historical_data['candles']:
        parsed_time = parser.parse(candle['time'])

        item = dict(time=parsed_time,
                    open=candle['openBid'],
                    high=candle['highBid'],
                    low=candle['lowBid'],
                    close=candle['closeBid'])

        items.append(item)

        pinbar_status = pinbar.get_pinbar_status(item['open'], item['high'], item['low'], item['close'])

        if pinbar_status['is_valid'] is True:
            patterns['pinbar'].append({
                'type': PATTERN_TYPE_PINBAR,
                'data': pinbar_status,
                'candle': candle
            })

    return pd.DataFrame(items), patterns


def get_candlesticks_and_patterns(historical_data):
    data, patterns = transform_data_to_panda_dataframe_and_patterns_info(historical_data)

    return go.Candlestick(x=data.time,
                          open=data.open,
                          high=data.high,
                          low=data.low,
                          close=data.close), patterns
