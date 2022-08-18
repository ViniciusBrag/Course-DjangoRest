import math


def make_pagination_range(total_range, limit_page, current_page):
    midlle_range = math.ceil(limit_page / 2)
    start_range = current_page - midlle_range
    stop_range = current_page + midlle_range

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    return total_range[start_range:stop_range]
