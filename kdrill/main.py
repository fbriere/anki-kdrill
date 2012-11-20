# -*- coding: utf-8 -*-
#
# kdrill - Anki plugin to tag kanji cards listed in KDrill usefile
#
# Copyright (c) 2012  Frédéric Brière <fbriere@fbriere.net>
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


from anki.facts import Fact

from sqlalchemy.orm import subqueryload

from kdrill.usefile import parse_usefile


def processDeck(deck, model, field, usefile):
    """Tag the facts in a deck matching the kanji set."""
    kanji_set = parse_usefile(usefile)

    facts = deck.s.query(Fact).\
            options(subqueryload(Fact.fields)).\
            filter(Fact.modelId == model.id).\
            all()

    ids = [f.id for f in facts if f[field.name] in kanji_set]

    deck.addTags(ids, "KDrill")

