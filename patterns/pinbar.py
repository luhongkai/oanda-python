import const
import math

PATTERN_TYPE_PINBAR = 'pinbar'
SETTINGS = dict(
    min_big_tail_size=0,
    min_body_size=0.00001,
    max_body_size=0.00500,
    big_tail_size_ratio_min=3,
    big_tail_threshold=0,
    pip_size=0.00001,
    long_tail_vs_short_tail_min_ratio=5
)


def get_pinbar_status(open, high, low, close):
    pinbar_status = dict(is_valid=False, type=None)
    min_big_tail_size = SETTINGS['min_big_tail_size']

    if all(open == item for item in [open, high, low, close]):
        return pinbar_status

    round_to = abs(int(math.log(SETTINGS['pip_size'], 10)))

    body_size = abs(round(close - open, round_to))
    top_tail_size = round(high - max(open, close), round_to)
    bottom_tail_size = round(min(open, close) - low, round_to)

    if top_tail_size == 0:
        top_tail_size = SETTINGS['pip_size']

    if bottom_tail_size == 0:
        bottom_tail_size = SETTINGS['pip_size']

    if body_size > SETTINGS['max_body_size'] or body_size < SETTINGS['min_body_size']:
        return pinbar_status

    try:
        top_tail_size_ratio = top_tail_size / body_size
        bottom_tail_size_ratio = bottom_tail_size / body_size
        big_tail_threshold = SETTINGS['big_tail_threshold']

    except ZeroDivisionError:
        return pinbar_status

    if bottom_tail_size > min_big_tail_size and \
                    bottom_tail_size_ratio > SETTINGS['big_tail_size_ratio_min'] and \
                    bottom_tail_size > big_tail_threshold and \
                    bottom_tail_size > SETTINGS['long_tail_vs_short_tail_min_ratio'] * top_tail_size:

        pinbar_status['is_valid'] = True
        pinbar_status['type'] = const.POSITION_TYPE_LONG

    elif top_tail_size > min_big_tail_size and \
                    top_tail_size_ratio > SETTINGS['big_tail_size_ratio_min'] and \
                    top_tail_size > big_tail_threshold and \
                    top_tail_size > SETTINGS['long_tail_vs_short_tail_min_ratio'] * bottom_tail_size:

        pinbar_status['is_valid'] = True
        pinbar_status['type'] = const.POSITION_TYPE_SHORT

    # if pinbar_status['is_valid'] == True and body_size == SETTINGS['pip_size']:
    #     print('open={}, high={}, low={}, close={}, body_size='.format(open, high, low, close, body_size))

    return pinbar_status
