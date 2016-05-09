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
import contextlib
from pprint import pprint

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


def printf(string, *args, **kwargs):
    print(string.format(*args, **kwargs))

def echo(*args, **kwargs):
    print(args, kwargs or '')

@contextlib.contextmanager
def swap_streams(stdout=None, stderr=None):
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    try:
        if stdout: sys.stdout = stdout
        if stderr: sys.stderr = stderr
        yield

    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr

@contextlib.contextmanager
def capture_output(stdout=True, stderr=True, muffle=False):

    class CapturedOutput:

        def __init__(self):
            self.stdout = ""
            self.stderr = ""

        def __contains__(self, phrase):
            return (phrase in self.stdout) or (phrase in self.stderr)

    class CapturedStream:

        def __init__(self, stream, write_callback):
            self.stream = stream
            self.write_callback = write_callback

        def write(self, string):
            if not muffle: self.stream.write(string)
            self.write_callback(string)

        def flush(self):
            self.stream.flush()


    captured_output = CapturedOutput()

    def write_to_stdout(message):
        captured_output.stdout += message

    def write_to_stderr(message):
        captured_output.stderr += message


    with swap_streams(
            stdout=CapturedStream(sys.stdout, write_to_stdout),
            stderr=CapturedStream(sys.stderr, write_to_stderr)):
        yield captured_output

@contextlib.contextmanager
def capture_stdout(muffle=False):
    with capture_output(stdout=True, stderr=False, muffle=muffle) as output:
        yield output.stdout

@contextlib.contextmanager
def capture_stderr(muffle=False):
    with capture_output(stdout=False, stderr=True, muffle=muffle) as output:
        yield output.stderr

@contextlib.contextmanager
def muffle(stdout=True, stderr=True):
    with capture_output(stdout, stderr, muffle=True):
        yield

@contextlib.contextmanager
def keep_on_one_line():
    """
    Keep all the output generated within a with-block on one line.  Whenever a 
    new line would be printed, instead reset the cursor to the beginning of the 
    line and print the new line without a line break.
    """

    class CondensedStream:

        def __init__(self):
            self.sys_stdout = sys.stdout

        def write(self, string):
            with swap_streams(self.sys_stdout):
                string = string.replace('\n', ' ')
                string = truncate_to_fit_terminal(string)
                if string.strip():
                    update(string)

        def flush(self):
            with swap_streams(self.sys_stdout):
                flush()


    with swap_streams(CondensedStream()):
        yield


def print_color(string, name, style='normal', when='auto'):
    print(color(string, name, style, when))

def write(string):
    """ Write the given string to standard out. """
    sys.stdout.write(string)
    flush()

def write_color(string, name, style='normal', when='auto'):
    """ Write the given colored string to standard out. """
    write(color(string, name, style, when))

def update(string):
    """ Replace the existing line with the given string. """
    clear()
    write(string)
    
def update_color(string, name, style='normal', when='auto'):
    """ Replace the existing line with the given colored string. """
    clear()
    write_color(string, name, style, when)

def progress(current, total):
    """ Display a simple progress report. """
    update('[%d/%d] ' % (current, total))

def progress_color(current, total, name, style='normal', when='auto'):
    """ Display a simple, colored progress report. """
    update_color('[%d/%d] ' % (current, total), name, style, when)

def color(string, name, style='normal', when='auto'):
    """ Change the color of the given string. """
    prefix = '\033[%d;%dm' % (styles[style], colors[name])
    suffix = '\033[%d;%dm' % (styles['normal'], colors['normal'])
    color_string = prefix + string + suffix

    if when == 'always':
        return color_string
    elif when == 'auto':
        return color_string if sys.stdout.isatty() else string
    elif when == 'never':
        return string
    else:
        raise ValueError("when must be one of: 'always', 'auto', 'never'")

def flush():
    """ Flush the stdout buffer to the terminal, if there is one. """
    if sys.stdout.isatty():
        sys.stdout.flush()

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

def save_cursor():
    """ Save the cursor position. """
    write('\033[s')

def restore_cursor():
    """ Restore the cursor position. """
    write('\033[u')

def conceal_cursor():
    """ Conceal the cursor. """
    write('\033[?25l')

def reveal_cursor():
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

def truncate_to_fit_terminal(string):
    width = terminal_width()
    if len(string) < width:
        return string
    else:
        return string[:width-4] + '...'


if __name__ == '__main__':
    import time

    print('counting...')

    with keep_on_one_line():
        print('1');  time.sleep(0.5)
        print('2');  time.sleep(0.5)
        print('3');  time.sleep(0.5)
        print('4');  time.sleep(0.5)
        print('5');  time.sleep(0.5)

    print('\n...done')
