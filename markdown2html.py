#!/usr/bin/python3
"""
markdown2html.py - A script that converts Markdown files to HTML.
Usage: ./markdown2html.py input_file.md output_file.html
"""


import os
import sys
import re
import hashlib

if len(sys.argv) == 1:
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    sys.exit(2)

ifile = sys.argv[1]
ofile = re.sub('\.(md|markdown)$', '', ifile) + '.html'

with open(ifile, 'r') as ifile:
    ifile_str = ifile.read() + '\n'

with open(ofile, 'w') as ofile:
    B = False  # Bold
    I = False  # Italic
    S = False  # Strikethrough
    c = False  # Inline code
    C = False  # Multiline code
    Q = 0
    p = False  # Paragraph
    i = 0

    while i < len(ifile_str) - 2:
        ch = ifile_str[i]
        i += 1

        if ch != '\n' and not p:
            ofile.write('<p>')
            p = True

        if ch in ('*', '_'):
            if C:
                ofile.write(ch)
                continue
            if ifile_str[i] in ('*', '_'):
                ofile.write(f'<{"/"*B}b>')
                B = not B
                i += 1
            else:
                ofile.write(f'<{"/"*I}i>')
                I = not I

        elif ch == '`':
            ch_b, ch_c = ifile_str[i], ifile_str[i + 1]
            if ch == ch_b == ch_c:
                ofile.write(f'<{"/"*C}code>')
                C = not C
                i += 2
            else:
                if C:
                    ofile.write(ch)
                    continue
                ofile.write(f'<{"/"*c}code>')
                c = not c

        elif ch == '~':
            if C:
                ofile.write(ch)
                continue
            if ifile_str[i] == '~':
                ofile.write(f'<{"/"*S}del>')
                S = not S
                i += 1

        elif ch == '[':
            if re.match('^\[.*\]\(.*(".*"|)\)$', ifile_str[i - 1:].split(')', 1)[0] + ')'):
                name = ''
                link = ''
                alt = ''
                s = ifile_str[i:].split(')', 1)[0] + ')'
                i += len(s)
                name = s.split(']')[0]
                link = s.split('(')[1].split(')')[0]
                if '"' in link:
                    alt = link.split('"')[1].split('"')[0]
                    link = link.split('"')[0].strip()
                ofile.write(f'<a href="{link}" title="{alt}">{name}</a>')

        elif ch == '\n':
            if C:
                ofile.write(ch)
                continue

            if c:
                ofile.write(f'</code>')

            if not p:
                ofile.write('<br>')
            elif ifile_str[i] == '\n':
                ofile.write('</p>\n')
                p = False
                i += 1

                if B:
                    ofile.write(f'</b>')
                    B = False
                if I:
                    ofile.write(f'</i>')
                    I = False
                if S:
                    ofile.write(f'</del>')
                    S = False
            elif not ifile_str[i]:
                if p:
                    ofile.write('</p>\n')
                else:
                    ofile.write('\n')
            else:
                ofile.write('<br>')
            ofile.write('\n')
        else:
            ofile.write(ch)

