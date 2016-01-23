# encoding: utf-8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import itertools

# I really think that an 'infinity' constant should be built into the language, 
# just like '0' or 'None'.  But it isn't, so I have to define it here instead.

infinity = inf = float("inf")

def span(start, stop, steps=50):
    step = (stop - start) / (steps - 1)
    return (start + i * step for i in range(steps))

def clamp(value, lowest, highest):
    if lowest > highest:
        lowest, highest = highest, lowest
    return min(max(value, lowest), highest)


def partition_list(iterable, chunks):
    return list(yield_partitioned(iterable, chunks))

def bin_list(iterable, count=2):
    return list(yield_binned(iterable, count))

def flatten_list(iterable):
    return list(yield_flattened(iterable))

def yield_partitioned(iterable, chunks):
    start, end = 0, 0
    list_size = len(iterable)
    chunk_size = int(list_size / chunks + 0.5)

    for index in range(chunks - 1):
        start = index * chunk_size
        end = start + chunk_size
        yield iterable[start:end]

    yield iterable[end:]

def yield_binned(iterable, count=2):

    views = itertools.tee(iterable, count)

    for index, view in enumerate(views):
        for x in range(index):
            next(view, None)

    return itertools.izip(*views)

def yield_flattened(iterable):

    for item in iterable:
        if not is_iterable(item):
            yield item

        else:
            for subitem in flatten(iterable):
                yield subitem

def is_iterable(obj):
    try: iter(obj)
    except: return False
    return isinstance(obj, basestring)

def weighted_choice(choices, weights):
    total = sum(w for w in weights)
    threshold = random.uniform(0, total)
    weight_sum = 0

    for choice, weight in zip(choices, weights):
        weight_sum += weight
        if weight_sum > threshold:
            return choice

    # Barring some sort of floating point error, we should never get this far.  
    # But if we do, returning the last choice is clearly the right action.

    return choices[-1]


