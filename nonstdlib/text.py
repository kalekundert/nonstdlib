#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

class plural:
    """
    The format string has three sections, separated by '/'.  The first section 
    is always printed, the second (optional) section is printed if the number 
    is singular, and the third section is printed if the number is plural.  Any 
    '?' in the format string are replaced with the actual number.

    >>> "{:? thing/s}".format(plural(1))
    1 thing
    >>> "{:? thing/s}".format(plural(2))
    2 things

    >>> "{:/a cactus/? cacti}".format(plural(1))
    a cactus
    >>> "{:/a cactus/? cacti}".format(plural(2))
    2 cacti

    From Veedrac on Stack Overflow: 
    http://stackoverflow.com/questions/21872366/plural-string-formatting

    """
    def __init__(self, value):
        self.value = value

    def __format__(self, formatter):
        from collections.abc import Sized

        x = self.value
        number = len(x) if isinstance(x, Sized) else self.value
        formatter = formatter.replace("?", str(number))
        always, _, suffixes = formatter.partition("/")
        singular, _, plural = suffixes.rpartition("/")

        return "{}{}".format(always, singular if number == 1 else plural)

def title(str):
    print(str)
    print('━' * len(str))

def section(str):
    print(str)
    print('─' * len(str))

def oxford_comma(items, conj='and'):
    if len(items) == 2:
        return '{0[0]} {1} {0[1]}'.format(items, conj)

    result = ''
    for i, item in enumerate(items):
        if i == len(items) - 1:
            result += '{}'.format(item)
        elif i == len(items) - 2:
            result += '{}, {} '.format(item, conj)
        else:
            result += '{}, '.format(item)
    return result

def pretty_range(x):
    blocks = []
    current_seq = []

    def make_blocks(seq):
        if len(seq) == 0:
            return []
        elif len(seq) == 1:
            return [str(seq[0])]
        elif len(seq) == 2:
            return [str(seq[0]), str(seq[1])]
        else:
            return ['{}-{}'.format(seq[0], seq[-1])]

    for i in sorted(x):
        if current_seq and i != current_seq[-1] + 1:
            blocks += make_blocks(current_seq)
            current_seq = []
        current_seq.append(i)

    blocks += make_blocks(current_seq)
    return ','.join(blocks)

def indices_from_str(
        x,
        cast=int,
        range=lambda a, b: range(a, b+1),
        block_delim=',', range_delim='-'):

    blocks = x.split(block_delim)
    indices = []

    for block in blocks:
        block = block.strip()

        if not block:
            continue

        if range_delim and range_delim in block:
            begin, end = block.split(range_delim)
            indices += range(cast(begin), cast(end))

        else:
            indices.append(cast(block))

    return indices



