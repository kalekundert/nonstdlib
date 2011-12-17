#!/usr/bin/env python

import re


def wrap(*lines, **options):
    indent = options.get("indent", 0) * ' '
    columns = options.get("columns", 79)

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

if __name__ == "__main__":

    print wrap(
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
            columns=70, indent=4)
