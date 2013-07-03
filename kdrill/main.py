# -*- coding: utf-8 -*-
#
# kdrill - Anki plugin to tag kanji cards listed in KDrill usefile
#
# Copyright (c) 2012-2013  Frédéric Brière <fbriere@fbriere.net>
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


from kdrill.usefile import parse_usefile


def processDeck(col, model, field, usefile):
    """Tag all notes matching the kanji set."""
    kanji_set = parse_usefile(usefile)

    notes = [col.getNote(n) for n in col.findNotes('note:"%s"' % model['name'])]

    ids = [n.id for n in notes if n[field] in kanji_set]

    col.tags.bulkAdd(ids, "KDrill")

