# -*- coding: utf-8 -*-
#
# kdrill - Anki plugin to tag cards according to KDrill usefile
#
# Copyright (c) 2010  Frédéric Brière <fbriere@fbriere.net>
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


def getCards(deck, templates_id):
    """Fetch all cards beloning to some templates."""
    return deck.s.query(Card).\
            options(eagerload_all(Card.fact, Fact.fields, Field.fieldModel)).\
            filter(Card.cardModelId.in_(templates_id)).all()

def splitCards(deck, cards, field_name, values):
    """Split a set of cards in two: those matching the values set, and those
    that don't.
    """
    found = []
    not_found = []

    for card in cards:
        if card.fact[field_name] in values:
            found.append(card.id)
        else:
            not_found.append(card.id)

    return found, not_found

def splitDeck(deck, field, values, templates):
    """Split a deck in two: cards matching the values set, and those that
    don't.
    """
    templates_id = map(lambda t: t.id, templates)
    cards = getCards(deck, templates_id)
    return splitCards(deck, cards, field.name, values)

