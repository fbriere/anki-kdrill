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


from aqt import mw

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from kdrill.ui_dialog import Ui_KDrillDialog
from kdrill.help import KDrillHelp

from operator import itemgetter
import os.path


class KDrillDialog(QDialog, Ui_KDrillDialog):
    """Main dialog window."""

    def __init__(self):
        QDialog.__init__(self, mw)
        self.setupUi(self)

        # Keep a copy of the list of models
        self._models = sorted(mw.col.models.all(), key=itemgetter("name"))

        # TODO: We could try and guess what the default model should be
        self.model = self._models[0]

        self.modelCombo.addItems([m['name'] for m in self._models])
        self.updateFieldCombo()

        self.setOkEnabled(False)

        usefile = os.path.expanduser("~/.kanjiusefile")
        if os.path.exists(usefile):
            self.usefileLine.setText(usefile)
            self.setOkEnabled(True)

        self.helpDialog = KDrillHelp()

    def updateFieldCombo(self):
        """Refresh the field combo box based on the selected model."""
        self.fieldCombo.clear()
        for field in mw.col.models.fieldNames(self.model):
            self.fieldCombo.addItem(field, field)
            if field == "Kanji":
                self.fieldCombo.setCurrentIndex(self.fieldCombo.count() - 1)

    def setOkEnabled(self, enabled):
        """Enable the Ok button once a usefile has been selected."""
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enabled)


    @pyqtSignature("")
    def on_usefileButton_clicked(self):
        """Callback for when the '...' file selector button is clicked."""
        filename = QFileDialog.getOpenFileName(self, "",
                                               self.usefileLine.text())
        if filename != "":
            self.usefileLine.setText(filename)
            self.setOkEnabled(True)

    @pyqtSignature("int")
    def on_modelCombo_activated(self, index):
        """Callback for when the model selection changes."""
        self.model = self._models[index]
        self.updateFieldCombo()

    @pyqtSignature("")
    def on_buttonBox_helpRequested(self):
        """Callback for when the 'Help' button is clicked."""
        self.helpDialog.exec_()


    @property
    def usefilename(self):
        return self.usefileLine.text()

    @property
    def field(self):
        return self.fieldCombo.itemData(self.fieldCombo.currentIndex())

