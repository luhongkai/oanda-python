import csv
import re
import datetime

from data_sources.tools import GRANULARITIES_AND_VALUE_IN_SECONDS

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


def validate_data_description(data):
    if len(data) != 4:
        raise Exception('Invalid first line of CSV file - 4 fields expected')

    if not re.match(r'^[A-Z]{3}_[A-Z]{3}$', data[0]):
        raise Exception('Invalid first line of CSV file - invalid instrument (first field)')

    if data[1] not in GRANULARITIES_AND_VALUE_IN_SECONDS:
        raise Exception('Invalid first line of CSV file - invalid granularity (second field)')

    try:
        datetime.datetime.strptime(data[2], DATETIME_FORMAT)
    except ValueError:
        raise Exception(
            'Invalid first line of CSV file - invalid datetime_from '
            + '(third field, expected format \'yyyy-mm-ddThh:mm:ss\')')

    try:
        datetime.datetime.strptime(data[3], DATETIME_FORMAT)
    except ValueError:
        raise Exception(
            'Invalid first line of CSV file - invalid datetime_from '
            + '(fourth field, expected format \'yyyy-mm-ddThh:mm:ss\')')


def validate_data_header(data_header):
    expected_header = [
        'time', 'openBid', 'openAsk', 'highBid', 'highAsk', 'lowBid', 'lowAsk', 'closeBid', 'closeAsk', 'volume',
    ]

    if expected_header != data_header:
        raise Exception('Invalid second line of CSV file - invalid header (expected: {})'.format(expected_header))


def get_historical_data(csv_file):
    data = dict(candles=list(), instrument='', granularity='')

    csv_file = open(csv_file, 'r', newline='')

    reader = csv.reader(csv_file, delimiter=';')

    data_description = next(reader)
    validate_data_description(data_description)

    data_header = next(reader)
    validate_data_header(data_header)

    data['instrument'] = data_description[0]
    data['granularity'] = data_description[1]

    for data_item in reader:
        data['candles'].append({
            'time': data_item[0],
            'openBid': float(data_item[1]),
            'openAsk': float(data_item[2]),
            'highBid': float(data_item[3]),
            'highAsk': float(data_item[4]),
            'lowBid': float(data_item[5]),
            'lowAsk': float(data_item[6]),
            'closeBid': float(data_item[7]),
            'closeAsk': float(data_item[8]),
            'volume': float(data_item[9])
        })

    csv_file.close()

    return data
