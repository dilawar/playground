#!/usr/bin/env python3

import re
import sys
import pypandoc
from pathlib import Path


def convert(infile):
    with open(infile) as f:
        txt = f.read()

    pat = re.compile(r'(---.+?---)\n(.+)', re.DOTALL)
    m = pat.match(txt)
    header = m.group(1)
    html = m.group(2)
    md = pypandoc.convert_text(html, 'markdown', format='html')
    return header + '\n' + md

def main():
    arg = Path(sys.argv[1])
    if arg.is_dir():
        files = arg.glob("*.html")
    else:
        files = [arg]

    for f in files:
        md = convert(f)
        of = f.with_suffix('.md')
        with open(of, 'w') as fh:
            fh.write(md)
            print(f'[INFO] Converted {f} to {of}')


if __name__ == "__main__":
    main()

