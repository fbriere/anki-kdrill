# -*- coding: utf-8 -*-
#
# kdrill - Anki add-on to tag kanji cards listed in KDrill usefile
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


from aqt import mw
from aqt.qt import *
import aqt.utils

from kdrill.dialog import KDrillDialog
from kdrill.main import tag_notes


def onMenuEntry():
    """Callback for our menu entry."""
    dialog = KDrillDialog()
    if dialog.exec_():
        mw.progress.start(immediate=True)
        mw.progress.update(_("Tagging kanji cards"))

        mw.checkpoint(_("Tag kanji cards listed in KDrill usefile"))

        with open(dialog.usefilename) as usefile:
            tagged, kanji = tag_notes(mw.col, dialog.field, usefile)

        mw.progress.finish()

        # FIXME: Do we need to do something?
        #mw.deck.refreshSession()

        aqt.utils.showInfo("Tagged %u notes (based on %u kanji)." % (
            len(tagged),
            len(kanji)))

def init():
    """Hook this add-on into Anki."""
    action = QAction(_("Tag kanji cards listed in KDrill usefile"), mw)

    mw.connect(action, SIGNAL("triggered()"), onMenuEntry)
    mw.form.menuTools.addAction(action)

