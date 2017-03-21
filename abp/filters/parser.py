# This file is part of Adblock Plus <https://adblockplus.org/>,
# Copyright (C) 2006-2017 eyeo GmbH
#
# Adblock Plus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Adblock Plus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Adblock Plus.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import re
from collections import namedtuple

__all__ = ['parse_filterlist', 'parse_line', 'ParseError']


class ParseError(Exception):
    """Exception thrown by the parser when it encounters invalid input.

    :param error: Description of the error.
    :param text: The text which was being parsed when an error occurred.
    """

    def __init__(self, error, text):
        Exception.__init__(self, '{} in "{}"'.format(error, text))
        self.text = text
        self.error = error


def line_type(name, field_names, format_string):
    """Define a line type.

    :param name: The name of the line type to define.
    :param field_names: A sequence of field names or one space-separated
        string that contains all field names.
    :returns: Class created with `namedtuple` that has `.type` set to
        lowercased `name` and supports conversion back to string with
        `.to_string()` method.
    """
    lt = namedtuple(name, field_names)
    lt.type = name.lower()
    lt.to_string = lambda self: format_string.format(self)
    return lt


Header = line_type('Header', 'version', '[{.version}]')
EmptyLine = line_type('EmptyLine', '', '')
Comment = line_type('Comment', 'text', '! {.text}')
Metadata = line_type('Metadata', 'key value', '! {0.key}: {0.value}')
Filter = line_type('Filter', 'expression', '{.expression}')
Include = line_type('Include', 'target', '%include {0.target}%')


METADATA_REGEXP = re.compile(r'!\s*(\w+)\s*:\s*(.*)')
METADATA_KEYS = {'Homepage', 'Title', 'Expires', 'Checksum', 'Redirect',
                 'Version'}
INCLUDE_REGEXP = re.compile(r'%include\s+(.+)%')
HEADER_REGEXP = re.compile(r'\[(Adblock(?:\s*Plus\s*[\d\.]+?)?)\]', flags=re.I)


def _parse_comment(text):
    match = METADATA_REGEXP.match(text)
    if match and match.group(1) in METADATA_KEYS:
        return Metadata(match.group(1), match.group(2))
    return Comment(text[1:].strip())


def _parse_header(text):
    match = HEADER_REGEXP.match(text)
    if not match:
        raise ParseError('Malformed header', text)
    return Header(match.group(1))


def _parse_instruction(text):
    match = INCLUDE_REGEXP.match(text)
    if not match:
        raise ParseError('Unrecognized instruction', text)
    return Include(match.group(1))


def parse_line(line_text):
    """Parse one line of a filter list.

    :param line_text: Line of a filter list (must be a unicode string).
    :returns: Parsed line object (see `line_type`).
    :raises ParseError: If the line can't be successfully parsed.
    """
    content = line_text.strip()

    if content == '':
        line = EmptyLine()
    elif content.startswith('!'):
        line = _parse_comment(content)
    elif content.startswith('%') and content.endswith('%'):
        line = _parse_instruction(content)
    elif content.startswith('[') and content.endswith(']'):
        line = _parse_header(content)
    else:
        line = Filter(content)

    assert line.to_string().replace(' ', '') == content.replace(' ', '')
    return line


def parse_filterlist(lines):
    """Parse filter list from an iterable.

    :param lines: List of strings or file or other iterable.
    :returns: Iterator over parsed lines.
    :raises ParseError: Can be thrown during iteration for invalid lines.
    """
    for line in lines:
        yield parse_line(line)
