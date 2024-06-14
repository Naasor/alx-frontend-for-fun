#!/usr/bin/python3
"""
markdown2html.py - A script that converts Markdown files to HTML.
Usage: ./markdown2html.py input_file.md output_file.html
"""

import sys
import os
import re
import hashlib

def convert_markdown_to_html(input_file, output_file):
    with open(input_file, 'r') as read_file:
        with open(output_file, 'w') as html_file:
            unordered_list_open = False
            ordered_list_open = False
            paragraph_open = False
            lines_buffer = []
            
            for line in read_file:
                line = line.rstrip()  # Strip trailing whitespace
                
                # Bold and italic formatting
                line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
                line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)
                
                # MD5 hash transformation
                md5_matches = re.findall(r'\[\[(.+?)\]\]', line)
                for match in md5_matches:
                    md5_hashed = hashlib.md5(match.encode()).hexdigest()
                    line = line.replace(f'[[{match}]]', md5_hashed)
                
                # Remove the letter 'C' and 'c'
                remove_c_matches = re.findall(r'\(\((.+?)\)\)', line)
                for match in remove_c_matches:
                    cleaned = ''.join(ch for ch in match if ch.lower() != 'c')
                    line = line.replace(f'(({match}))', cleaned)
                
                # Heading tags
                heading_match = re.match(r'(#{1,6})\s*(.*)', line)
                if heading_match:
                    if paragraph_open:
                        html_file.write(''.join(lines_buffer))
                        html_file.write('</p>\n')
                        paragraph_open = False
                        lines_buffer = []
                    heading_level = len(heading_match.group(1))
                    content = heading_match.group(2)
                    line = f'<h{heading_level}>{content}</h{heading_level}>\n'
                    html_file.write(line)
                    continue
                
                # Unordered list
                if line.startswith('- '):
                    if paragraph_open:
                        html_file.write(''.join(lines_buffer))
                        html_file.write('</p>\n')
                        paragraph_open = False
                        lines_buffer = []
                    if not unordered_list_open:
                        html_file.write('<ul>\n')
                        unordered_list_open = True
                    line = f'    <li>{line[2:].strip()}</li>\n'
                    html_file.write(line)
                    continue
                elif unordered_list_open:
                    html_file.write('</ul>\n')
                    unordered_list_open = False
                
                # Ordered list
                if line.startswith('* '):
                    if paragraph_open:
                        html_file.write(''.join(lines_buffer))
                        html_file.write('</p>\n')
                        paragraph_open = False
                        lines_buffer = []
                    if not ordered_list_open:
                        html_file.write('<ol>\n')
                        ordered_list_open = True
                    line = f'    <li>{line[2:].strip()}</li>\n'
                    html_file.write(line)
                    continue
                elif ordered_list_open:
                    html_file.write('</ol>\n')
                    ordered_list_open = False
                
                # Paragraphs
                if line.strip() == '':
                    if paragraph_open:
                        html_file.write(''.join(lines_buffer))
                        html_file.write('</p>\n')
                        paragraph_open = False
                        lines_buffer = []
                else:
                    if not paragraph_open:
                        paragraph_open = True
                        lines_buffer.append('<p>\n')
                    else:
                        lines_buffer.append('    <br />\n')
                    lines_buffer.append(f'    {line}\n')

            if unordered_list_open:
                html_file.write('</ul>\n')
            if ordered_list_open:
                html_file.write('</ol>\n')
            if paragraph_open:
                html_file.write(''.join(lines_buffer))
                html_file.write('</p>\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    if not os.path.isfile(input_filename):
        print(f'Missing {input_filename}', file=sys.stderr)
        sys.exit(1)

    convert_markdown_to_html(input_filename, output_filename)
    sys.exit(0)
