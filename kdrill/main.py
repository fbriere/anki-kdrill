# -*- coding: utf-8 -*-
#
# kdrill - Anki plugin to tag cards according to KDrill usefile
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


from anki.cards import Card
from anki.facts import Fact, Field

from sqlalchemy.orm import eagerload_all

from kdrill.usefile import parse_usefile


def processDeck(deck, usefile_name, field, templates):
    """Tag the cards in a deck matching the kanji set."""
    usefile = open(usefile_name)
    kanji_set = parse_usefile(usefile)
    usefile.close()

    templates_id = map(lambda t: t.id, templates)
    cards = deck.s.query(Card).\
            options(eagerload_all(Card.fact, Fact.fields, Field.fieldModel)).\
            filter(Card.cardModelId.in_(templates_id)).all()

    tag = []

    for card in cards:
        if card.fact[field.name] in kanji_set:
            tag.append(card.id)

    deck.addTags(tag, "KDrill")

