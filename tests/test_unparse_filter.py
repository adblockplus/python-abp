# This file is part of Adblock Plus <https://adblockplus.org/>,
# Copyright (C) 2006-present eyeo GmbH
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

"""Tests for abp.filters.blocks."""

from __future__ import unicode_literals

import os

import pytest

from abp.filters.parser import unparse_filter, parse_filterlist

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture()
def fl_lines():
    with open(os.path.join(DATA_PATH, "filterlist.txt")) as f:
        return list(parse_filterlist(f))


def test_unparse_filter(fl_lines):
    for line in fl_lines:
        if line.type == "filter":
            unparsed = unparse_filter(line)
            assert unparsed == line.text
