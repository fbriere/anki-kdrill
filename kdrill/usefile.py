# -*- coding: utf-8 -*-
#
# kdrill - Anki plugin to tag kanji cards listed in KDrill usefile
#
# Copyright (c) 2010-2013  Frédéric Brière <fbriere@fbriere.net>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


def parse_usefile(file):
    """Parse a KDrill usefile, and return the corresponing set of kanji."""
    def parse_line(s):
        """Parse a single usefile line and return the corresponding kanji."""
        # Convert an ASCII JIS string ("3b7a") to an EUC-JP number (0xbbfa)
        euc_val = int(s, 16) + 0x8080
        # Convert that number to an EUC-JP string (0xbb 0xfa)
        euc_str = chr(euc_val >> 8) + chr(euc_val & 0xff)
        # Finally convert that to a Unicode string
        return unicode(euc_str, "euc-jp")

    kanji_set = set()
    for line in file:
        kanji_set.add(parse_line(line))
    return kanji_set

