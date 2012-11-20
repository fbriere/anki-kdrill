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


from ankiqt import mw, ui

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from kdrill.dialog import KDrillDialog
from kdrill.main import processDeck


def onMenuEntry():
    """Callback for our menu entry."""
    dialog = KDrillDialog()
    if dialog.exec_():
        mw.deck.startProgress()
        mw.deck.updateProgress(_("Tagging cards"))

        undo = _("Tag cards from KDrill usefile")
        mw.deck.setUndoStart(undo)

        with open(dialog.usefilename) as usefile:
            processDeck(deck=mw.deck,
                        usefile=usefile,
                        model=dialog.model,
                        field=dialog.field)

        mw.deck.setUndoEnd(undo)
        mw.deck.finishProgress()

        # FIXME: Is this all we need to do?
        mw.deck.refreshSession()

def init():
    """Hook this plugin into Anki."""
    action = QAction(mw)
    action.setText(_("Tag cards from KDrill usefile"))

    mw.mainWin.menuTools.addAction(action)
    mw.connect(action, SIGNAL("triggered()"), onMenuEntry)

