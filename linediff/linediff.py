#!/usr/bin/python3 -u

"Compare adjacent objects in a stream (normally lines)"

from __future__ import absolute_import, division, print_function, unicode_literals

import sys


import difflib
import functools
import sys

import termcolor


@functools.lru_cache(maxsize=10000)
def lcs(xstr, ystr):

    # This is np-hard (wooh!)
    
    # From http://rosettacode.org/wiki/Longest_common_subsequence#Python
    #print repr((xstr, ystr))

    if not xstr or not ystr:
        return ""
    x, xs, y, ys = xstr[0], xstr[1:], ystr[0], ystr[1:]
    if x == y:
        return x + lcs(xs, ys)
    else:
        return max(lcs(xstr, ys), lcs(xs, ystr), key=len)

def lcs_indexes(xstr, ystr):
    return lcs_to_index(xstr, ystr, lcs(xstr, ystr))

def lcs_to_index(xstr, ystr, sub):
    if sub:
        return [(xstr.index(sub[0]), ystr.index(sub[0]))] + lcs_to_index(xstr[1:], ystr[1:], sub[1:])
    else:
        return []

def lcss(x, y):
    s = difflib.SequenceMatcher(None, x, y)
    m = s.find_longest_match(0, len(x), 0, len(y))
    return [(m.a + i, m.b + i)  for i in range(m.size)]

def clever_lcs(xstr, ystr):
    "Find a nice representation of the longest common substring of xstr and ystr"
    # Greedily consume common substrings, then find a common sequence
    substrings = lcss(xstr, ystr)
    if len(substrings) >= 2:
        min_x, min_y = substrings[0]
        max_x, max_y = substrings[-1]
        transformed_indexes = clever_lcs(xstr[max_x + 1:], ystr[max_y + 1:])
        return clever_lcs(xstr[:min_x], ystr[:min_y]) + substrings + [(x + max_x + 1, y + max_y + 1) for (x, y) in transformed_indexes]
    else:
        return lcs_indexes(xstr, ystr)

def stream_stdin():
    while True:
        line = sys.stdin.readline()
        if line == '':
            break

        yield line

def pairs(it):
    prev = None
    for x in it:
        yield (prev, x)
        prev = x

def triples(it):
    prevprev, prev = None, None
    for x in it:
        yield (prevprev, prev, x)
        prevprev, prev = prev, x

def color_indexes(indexes_for_color, string):
    result = []
    for i, x in enumerate(string):
        for color, indexes in indexes_for_color.items():
            if i in indexes:
                result.append(termcolor.colored(x, color))
                break
        else:
            result.append(x)
    return ''.join(result)


def main():
    sys.setrecursionlimit(10000) # for lcs (perhaps we should use a trampoline)
    current = None
    leftover_indexes = set()
    for prevprev, prev, current in triples(stream_stdin()):
        backward_indexes = forward_indexes = set()
        if prevprev is not None:
            # unnecessary recalculation
            backward_indexes = set([x[1] for x in clever_lcs(prevprev, prev)])

        if prev is not None:
            pairs = clever_lcs(prev, current)
            forward_indexes = set([x[0] for x in pairs])
            leftover_indexes = set([x[1] for x in pairs])

        color1_indexes, color2_indexes, color3_indexes = (
            backward_indexes - forward_indexes,
            backward_indexes & forward_indexes,
            forward_indexes - backward_indexes)


        if prev:
            print(color_indexes(dict(
                blue=color1_indexes,
                yellow=color2_indexes,
                red=color3_indexes),
                                    prev), end='')
    
    print(color_indexes(dict(yellow=leftover_indexes), current), end='')

if __name__ == '__main__':
    print(clever_lcs('melts\n', 'member\n'))
#	main()
