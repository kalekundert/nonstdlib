# encoding: latin-1

from __future__ import division

import math
import itertools

# Mathematical Functions {{{1

def span(start, stop, count=50):
    from numpy import linspace
    return list(linspace(start, stop, num=count))

def clamp(value, lowest, highest):

    if lowest > highest:
        lowest, highest = highest, lowest

    return min(max(value, lowest), highest)

# Iteration Functions {{{1

def partition_list(iterable, chunks):
    return list(yield_partitioned(iterable, chunks))

def flatten_list(iterable):
    return list(yield_flattened(iterable))

def bin_list(iterable, count=2):
    return list(yield_binned(iterable, count))

def yield_partitioned(iterable, chunks):

    start, end = 0, 0

    list_size = len(iterable)
    chunk_size = int(list_size / chunks + 0.5)

    for index in range(chunks - 1):
        start = index * chunk_size
        end = start + chunk_size

        yield iterable[start:end]

    yield iterable[end:]

def yield_flattened(iterable):

    for item in iterable:
        if not is_iterable(item):
            yield item

        else:
            for subitem in flatten(iterable):
                yield subitem

def yield_binned(iterable, count=2):

    views = itertools.tee(iterable, count)

    for index, view in enumerate(views):
        for x in range(index):
            next(view, None)

    return itertools.izip(*views)

def is_iterable(obj):
    try: iter(obj)
    except: return False
    return isinstance(obj, basestring)

# }}}1
