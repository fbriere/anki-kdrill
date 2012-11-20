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

from kdrill.ui_dialog import Ui_KDrillDialog
from kdrill.help import KDrillHelp

from operator import attrgetter
import os.path


class KDrillDialog(QDialog, Ui_KDrillDialog):
    """Main dialog window."""

    def __init__(self):
        QDialog.__init__(self, mw)
        self.setupUi(self)

        # Keep a copy of the list of models
        self._models = sorted(mw.deck.models, key=attrgetter("name"))

        # TODO: We could try and guess what the default model should be
        self.model = self._models[0]

        self.modelCombo.addItems(QStringList([m.name for m in self._models]))
        self.updateFieldCombo()

        self.setOkEnabled(False)

        usefile = os.path.expanduser("~/.kanjiusefile")
        if os.path.exists(usefile):
            self.usefileLine.setText(usefile)
            self.setOkEnabled(True)

        self.helpDialog = KDrillHelp()

    def updateFieldCombo(self):
        """Refresh the field combo box based on a given model."""
        self.fieldCombo.clear()
        for field in self.model.fieldModels:
            self.fieldCombo.addItem(field.name, QVariant(field))
            if field.name == "Kanji":
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

    def accept(self):
        """Callback for when the Ok button is clicked."""
        self.usefile = self.usefileLine.text()
        self.field = self.fieldCombo.itemData(self.fieldCombo.currentIndex()).\
                toPyObject()

        QDialog.accept(self)

    def reject(self):
        """Callback for when the Cancel button is clicked."""
        QDialog.reject(self)

