# -*- coding: utf-8 -*-
#
# kdrill - Anki plugin to (un)suspend cards according to KDrill usefile
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


import os.path

from ankiqt import mw

from PyQt4 import QtCore, QtGui

from kdrill.deck import splitDeck
from kdrill.dialog import KDrillDialog
from kdrill.usefile import parse_usefile


def processDeck(deck, usefile_name, field, templates):
    """Suspend the cards in a deck not matching the kanji set, and unsuspend
    those that do.
    """
    usefile = open(usefile_name)
    kanji_set = parse_usefile(usefile)
    usefile.close()

    unsuspend, suspend = splitDeck(deck, field, kanji_set, templates)

    deck.suspendCards(suspend)
    deck.unsuspendCards(unsuspend)

def onApplyClicked():
    """Callback for the 'Apply KDrill usefile' menu entry."""
    dialog = KDrillDialog()
    if dialog.exec_():
        mw.deck.startProgress()
        mw.deck.updateProgress(_("Applying KDrill usefile"))
        undo = _("Apply KDrill usefile")
        mw.deck.setUndoStart(undo)

        processDeck(mw.deck, dialog.usefile, dialog.field, dialog.cardModels)

        mw.deck.setUndoEnd(undo)
        mw.deck.finishProgress()

def init():
    """Hook this plugin into Anki."""
    action = QtGui.QAction(mw)
    action.setText(_("Apply KDrill usefile"))

    mw.mainWin.menuTools.addAction(action)
    mw.connect(action, QtCore.SIGNAL("triggered()"), onApplyClicked)

