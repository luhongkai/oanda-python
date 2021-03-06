import data_sources.tools as tools
import sys
from json.decoder import JSONDecodeError
from data_sources.oanda import client


MAX_BARS_IN_ONE_REQUEST = 5000


def get_datetime_for_api_argument(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S.000000Z')


def get_historical_data(instrument, granularity, datetime_from, datetime_to):
    ranges_to_fetch = tools.get_datetime_ranges_to_fetch(datetime_from, datetime_to, granularity,
                                                         MAX_BARS_IN_ONE_REQUEST)

    final_response = dict(instrument=None, granularity=None, candles=list(), datetime_ranges_with_error=list())

    to_complete = len(ranges_to_fetch)
    completed_items = 0
    write_download_status(0)

    for range_data in ranges_to_fetch:
        try:
            response = client.get_history(instrument=instrument, granularity=granularity,
                                          start=get_datetime_for_api_argument(range_data['datetime_from']),
                                          end=get_datetime_for_api_argument(range_data['datetime_to']))
        except JSONDecodeError:
            final_response['datetime_ranges_with_error'].append(
                dict(datetime_from=range_data['datetime_from'], datetime_to=range_data['datetime_to']))
            response = None

        if response is not None:
            if final_response['instrument'] is None and final_response['granularity'] is None:
                final_response['instrument'] = response['instrument']
                final_response['granularity'] = response['granularity']

            final_response['candles'].extend(response['candles'])

        completed_items = completed_items + 1
        write_download_status(round((completed_items / to_complete) * 100))

    print('')
    sys.stdout.flush()

    if len(final_response['datetime_ranges_with_error']) > 0:
        print('These datetime ranges weren\'t downloaded:')

        for item in final_response['datetime_ranges_with_error']:
            print('  --> \'{}\' - \'{}\''.format(item['datetime_from'], item['datetime_to']))

    return final_response


def write_download_status(completed_percent):
    print('Downloading data ({}%)'.format(completed_percent), end='\r')
    sys.stdout.flush()
