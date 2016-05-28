#!/usr/bin/env python3

import re

def minutes(x):
    if isinstance(x, int):
        return x

    parsed_time = re.match('(\d+)h(\d+)?|(\d+)m', x)
    if not parsed_time:
        raise ValueError("can't interpret '{}' as a time.".format(x))

    hours = parsed_time.group(1) or 0
    minutes = parsed_time.group(2) or parsed_time.group(3) or 0

    return 60 * int(hours) + int(minutes)
