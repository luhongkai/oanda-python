import datetime

GRANULARITIES_AND_VALUE_IN_SECONDS = dict(
    S5=5, S10=10, S15=15, S30=30,
    M1=60, M2=60 * 2, M3=60 * 3, M4=60 * 4, M5=60 * 5, M10=60 * 10, M15=60 * 15, M30=60 * 30,
    H1=3600, H2=3600 * 2, H3=3600 * 3, H4=3600 * 4, H6=3600 * 6, H8=3600 * 8, H12=3600 * 12,
    D=3600 * 24, W=3600 * 24 * 7, M=3600 * 24 * 31,
)


def get_number_of_bars_from_datetime_range(datetime_from, datetime_to, granularity):
    if granularity not in GRANULARITIES_AND_VALUE_IN_SECONDS:
        raise Exception('Granularity \'{}\' is not valid'.format(granularity))

    if datetime_from >= datetime_to:
        raise Exception(
            'Invalid date range: datetime_from (\'{}\') has to by smaller than datetime_to (\'{}\')'.format(
                datetime_from, datetime_to))

    datetime_diff = datetime_to - datetime_from

    if datetime_diff.total_seconds() < GRANULARITIES_AND_VALUE_IN_SECONDS[granularity]:
        raise Exception('Timeframe for this datetime range is too small')

    bars_count = int(datetime_diff.total_seconds() / GRANULARITIES_AND_VALUE_IN_SECONDS[granularity])

    return bars_count


def get_datetime_ranges_to_fetch(datetime_from, datetime_to, granularity, maximum_number_of_bars_in_one_request):
    number_of_bars = get_number_of_bars_from_datetime_range(datetime_from, datetime_to, granularity)

    datetime_ranges = list()

    datetime_current_from = datetime_from

    while number_of_bars > 0:
        datetime_current_to = datetime_current_from + datetime.timedelta(
            seconds=GRANULARITIES_AND_VALUE_IN_SECONDS[granularity] * maximum_number_of_bars_in_one_request)

        if datetime_current_to > datetime_to:
            datetime_current_to = datetime_to

        expected_number_of_bars = get_number_of_bars_from_datetime_range(datetime_current_from,
                                                                         datetime_current_to,
                                                                         granularity)

        datetime_ranges.append(dict(datetime_from=datetime_current_from, datetime_to=datetime_current_to,
                                    number_of_bars=expected_number_of_bars))

        datetime_current_from = datetime_current_to

        number_of_bars = number_of_bars - expected_number_of_bars

    return datetime_ranges
