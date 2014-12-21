#!/usr/bin/env python

# This module provides some tools for manipulating the position of the cursor.  
# This is useful for programs that need to update some simple pieces of 
# information (like a clock) but don't require a full-blown ncurses interface.

# This module defines a class which can be used to temporarily suppress stdout 
# and stderr, using the natural 'with-statement' syntax.  Anything written to 
# either file descriptor while it is being muffled can be accessed as a string.

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

colors = {
    'normal'        : 0,
    'black'         : 30,
    'red'           : 31,
    'green'         : 32,
    'yellow'        : 33,
    'blue'          : 34,
    'magenta'       : 35,
    'cyan'          : 36,
    'white'         : 37 }

styles = {
    'normal'        : 0,
    'bold'          : 1,
    'reverse'       : 2 }


class Muffler(object):

    class File:

        def __init__(self):
            self.string = ""

        def __str__(self):
            return self.string

        def write(self, string):
            self.string += string

        def flush(self):
            pass


    def __init__(self, **files):
        self.stdout = sys.stdout
        self.stderr = sys.stderr

        self.files = {
                'stdout' : files['stdout'] if 'stdout' in files else True,
                'stderr' : files['stderr'] if 'stderr' in files else True }

        self.file = Muffler.File()

    def __str__(self):
        return str(self.file)

    def __contains__(self, string):
        return string in str(self)

    def __enter__(self):
        if self.files['stdout']:
            sys.stdout = self.file
            
        if self.files['stderr']:
            sys.stderr = self.file

        return self

    def __exit__(self, *ignore):
        sys.stdout = self.stdout
        sys.stderr = self.stderr



def write(string):
    """ Write the given string to standard out. """
    sys.stdout.write(string)
    sys.stdout.flush()

def write_color(string, name, style='normal'):
    """ Write the given colored string to standard out. """
    write(color(string, name, style))

def update(string):
    """ Replace the existing line with the given string. """
    clear()
    write(string)
    
def update_color(string, name, style='normal'):
    """ Replace the existing line with the given colored string. """
    clear()
    write(string)

def progress(current, total):
    """ Display a simple progress report. """
    update('[%d/%d] ' % (current, total))

def progress_color(current, total, name, style='normal'):
    """ Display a simple, colored progress report. """
    update_color('[%d/%d] ' % (current, total), name, style)

def color(string, name, style='normal'):
    """ Change the color of the given string. """
    prefix = '\033[%d;%dm' % (styles[style], colors[name])
    suffix = '\033[%d;%dm' % (styles['normal'], colors['normal'])
    return prefix + string + suffix

def move(x, y):
    """ Move cursor to the given coordinates. """
    write('\033[' + str(x) + ';' + str(y) + 'H')

def move_up(lines):
    """ Move cursor up the given number of lines. """
    write('\033[' + str(lines) + 'A')

def move_down(lines):
    """ Move cursor down the given number of lines. """
    write('\033[' + str(lines) + 'B')

def move_forward(chars):
    """ Move cursor forward the given number of characters. """
    write('\033[' + str(chars) + 'C')

def move_back(chars):
    """ Move cursor backward the given number of characters. """
    write('\033[' + str(chars) + 'D')

def clear():
    """ Clear the screen and home the cursor. """
    write('\033[2K' + '\r')

def clear_eol():
    """ Clear the screen to end of line. """
    write('\033[0K')

def save():
    """ Save the cursor position. """
    write('\033[s')

def restore():
    """ Restore the cursor position. """
    write('\033[u')

def conceal():
    """ Conceal the cursor. """
    write('\033[?25l')

def reveal():
    """ Reveal the cursor. """
    write('\033[?25h')

def terminal_width():
    """ Return the width of the terminal. """
    return terminal_size()[0]

def terminal_height():
    """ Return the height of the terminal. """
    return terminal_size()[1]

def terminal_size():
    """ Return the size of the terminal as a (width, height) tuple. """
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack(
                    b'hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr


    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass

    if not cr:
        cr = env.get('LINES', 25), env.get('COLUMNS', 80)

    return int(cr[1]), int(cr[0])


if __name__ == '__main__':

    muffler = Muffler()
    greeting = "Hello world!"

    with muffler:
        print(greeting)

    assert str(muffler) == greeting + '\n'
    print("All tests passed!")

