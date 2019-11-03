#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import re

pat_ = re.compile(r'si:(?P<val>\S+)\s+(?P<unit>\S+)')

def val2tex(val):
    if 'e' in val:
        a, f = val.split('e')
        if a.strip:
            return f"{a}\\times 10^{f}" 
        else:
            return f"$10^{f}"
    return val

def val2md(val):
    if 'e' in val:
        a, f = val.split('e')
        return f'{a}×10~{f}~' if a else f'10~{f}~'
    return val

def parse(s):
    global pat_
    return pat_.finditer(s)

def fmt_tex(s):
    return s

def fmt_txt(s):
    val = val2md(s.group('val'))
    unit = s.group('unit')
    print(val, unit)
    return s

def fmt(s, fmt='text'):
    vals = parse(s)
    if fmt == 'tex':
        return [fmt_tex(v) for v in vals]
    return [fmt_txt(v) for v in vals]

def test():
    test1 = 'si:1.25e-3 A'
    ans1 = fmt(test1)
    print(test1, ans1)

if __name__ == '__main__':
    test()
