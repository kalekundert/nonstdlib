#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def plural(count, singular, plural=None):
    if plural is None: plural = singular + 's'
    return singular if count == 1 else plural

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

