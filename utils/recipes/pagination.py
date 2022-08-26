import math


def make_pagination_range(total_range, limit_page, current_page):
    midlle_range = math.ceil(limit_page / 2)
    start_range = current_page - midlle_range
    stop_range = current_page + midlle_range
    total_pages = len(total_range)

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range -= abs(total_pages - stop_range)

    pagination = total_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'total_range': total_range,
        'limit_page': limit_page,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > midlle_range,
        'last_page_out_of_range': stop_range < total_pages
    }


