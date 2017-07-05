import const


def get_pinbar_status(open, high, low, close):
    pinbar_status = dict(is_valid=False, type=None)
    min_big_tail_size = 0.0002

    if all(open == item for item in [open, high, low, close]):
        return pinbar_status

    body_size = abs(round(close - open, 5))
    top_tail_size = round(high - max(open, close), 5)
    bottom_tail_size = round(min(open, close) - low, 5)

    if top_tail_size == 0:
        top_tail_size = 0.00001

    if bottom_tail_size == 0:
        bottom_tail_size = 0.00001

    if body_size == 0:
        body_size = 0.00001

    try:
        top_tail_size_ratio = top_tail_size / min(top_tail_size, bottom_tail_size)
        bottom_tail_size_ratio = bottom_tail_size / min(top_tail_size, bottom_tail_size)
        long_tail_treshold = body_size * 10

    except ZeroDivisionError:
        return pinbar_status

    if bottom_tail_size > min_big_tail_size and bottom_tail_size_ratio > 3 and bottom_tail_size > long_tail_treshold:
        pinbar_status['is_valid'] = True
        pinbar_status['type'] = const.POSITION_TYPE_LONG
    elif top_tail_size > min_big_tail_size and top_tail_size_ratio > 3 and top_tail_size > long_tail_treshold:
        pinbar_status['is_valid'] = True
        pinbar_status['type'] = const.POSITION_TYPE_SHORT

    return pinbar_status
