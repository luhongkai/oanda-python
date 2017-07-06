import os
import datetime
import sys, getopt
import csv
from data_sources.oanda import oanda as oanda


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


def print_usage():
    print('Usage: python download_data.py -f <datetime_from> -t <datetime_to> -g <granularity> -i <instrument>'
          + ' -o <output_file>')
    print('  -> datetime_from and datetime_to are in \'yyyy-mm-ddThh:mm:ss\' format')
    print('  -> for list of available granularity '
          + 'see http://developer.oanda.com/rest-live/rates/#retrieveInstrumentHistory, '
          + 'for example use \'H1\' for hourly timeframe')
    print('  -> for instrument list, see OANDA API documentation (http://developer.oanda.com), '
          + 'for example use \'EUR_USD\'')


def get_settings(argv):
    settings = dict(
        datetime_from=None,
        datetime_to=None,
        granularity=None,
        instrument=None,
        output_file=''
    )

    opts, args = getopt.getopt(argv, "hf:t:g:i:o:")

    for opt, arg in opts:

        if opt == "-h":
            print_usage()
            exit(0)
        elif opt == '-f':
            settings['datetime_from'] = datetime.datetime.strptime(arg, DATETIME_FORMAT)
        elif opt == '-t':
            settings['datetime_to'] = datetime.datetime.strptime(arg, DATETIME_FORMAT)
        elif opt == '-g':
            settings['granularity'] = arg
        elif opt == '-i':
            settings['instrument'] = arg
        elif opt == '-o':
            settings['output_file'] = arg

    validate_settings(settings)

    return settings


def validate_settings(settings):
    if settings['datetime_from'] is None or settings['datetime_to'] is None:
        raise Exception('Missing values - datetime_from and datetime_to are required')

    if settings['granularity'] is None:
        raise Exception('Missing value - you have to specify granularity (timeframe)')

    if settings['instrument'] is None:
        raise Exception('Missing value - you have to specify instrument')

    if settings['output_file'] == '':
        raise Exception('Missing value - you have to specify output_file')


def main(argv):
    settings = get_settings(argv)

    csv_file = open(settings['output_file'], 'w', newline='')

    response = oanda.get_historical_data(instrument=settings['instrument'], granularity=settings['granularity'],
                                         datetime_from=settings['datetime_from'], datetime_to=settings['datetime_to'])

    print('Started to writing data to file...')

    csv_writer = csv.writer(csv_file, delimiter=';')
    csv_writer.writerow([
        response['instrument'],
        response['granularity'],
        settings['datetime_from'].strftime(DATETIME_FORMAT),
        settings['datetime_to'].strftime(DATETIME_FORMAT),
    ])

    csv_writer.writerow(
        ['time', 'openBid', 'openAsk', 'highBid', 'highAsk', 'lowBid', 'lowAsk', 'closeBid', 'closeAsk', 'volume'])

    for candle_data in response['candles']:
        csv_writer.writerow([
            candle_data['time'],
            candle_data['openBid'],
            candle_data['openAsk'],
            candle_data['highBid'],
            candle_data['highAsk'],
            candle_data['lowBid'],
            candle_data['lowAsk'],
            candle_data['closeBid'],
            candle_data['closeAsk'],
            candle_data['volume']
        ])

    csv_file.close()

    print('Data are saved in \'{}\' now...'.format(settings['output_file']))


if __name__ == "__main__":
    main(sys.argv[1:])
