#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

def wrap(*lines, **options):
    """ Combines the lines given in the list argument into a single string 
    wrapped to fit inside an 80-character (by default) display.  Both the 
    indentation and the terminal width can be controlled using keyword 
    arguments. """

    indent = options.get('indent', 0) * ' '
    columns = options.get('columns', 79)

    input = ''.join(lines)
    words = re.split('( )+', input)

    line = indent
    lines = []

    for word in words:
        if len(line) + len(word) + 1 < columns:
            line += word
        else:
            lines.append(line)
            line = indent + word.strip()

    lines.append(line)

    return '\n'.join(lines)

def plural(count, singular, plural=None):
    if plural is None: plural = singular + 's'
    return singular if count == 1 else plural

def indent(string, indent='  '):
    return indent + string.replace('\n', '\n' + indent)

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


if __name__ == "__main__":

    print(wrap(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ',
            'lobortis posuere rutrum. Nam eu aliquam dolor. Fusce eleifend ',
            'facilisis nisi in blandit. Donec vitae turpis ipsum. In leo ',
            'justo, sollicitudin id tristique at, accumsan vitae nunc. In ',
            'dapibus, lorem sed congue porta, urna enim vulputate nunc, sit ',
            'amet luctus elit lectus vitae ipsum. Maecenas at velit velit. ',
            'Ut dignissim massa sit amet nisl pretium quis pharetra eros ',
            'pharetra. Nulla scelerisque arcu et sapien commodo ac mollis ',
            'turpis facilisis. Aenean ut justo at nibh posuere pulvinar. ',
            'Pellentesque ornare laoreet libero eget vulputate. Fusce ',
            'vehicula, metus ac commodo adipiscing, turpis eros semper ',
            'dolor, vel scelerisque purus tellus quis leo. Donec pulvinar ',
            'ullamcorper arcu, quis scelerisque orci ornare nec. Donec ',
            'vitae urna ac arcu ultricies posuere. Morbi fermentum molestie ',
            'libero, eu ultricies orci placerat eget.', 
            columns=40, indent=4))
