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


import os.path

from ankiqt import mw, ui

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from kdrill.ui_dialog import Ui_KDrillDialog
from kdrill.help import KDrillHelp


class KDrillDialog(QDialog, Ui_KDrillDialog):
    """'Apply KDrill usefile' dialog window."""

    def __init__(self):
        QDialog.__init__(self, mw)
        self.setupUi(self)

        # Add this missing widget
        self.modelChooser = ui.modelchooser.ModelChooser(self, mw, mw.deck,
                                                         self.modelChanged)
        self.modelWidget.setLayout(self.modelChooser)

        self.enableOk(0)

        usefile = os.path.expanduser("~/.kanjiusefile")
        if os.path.exists(usefile):
            self.usefileLine.setText(usefile)
            self.enableOk()

        self.modelChanged(mw.deck.currentModel)

        self.helpDialog = KDrillHelp()

    def enableOk(self, enabled=1):
        """Enable the Ok button once a usefile has been selected."""
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enabled)

    @pyqtSignature("")
    def on_usefileButton_clicked(self):
        """Callback for when the '...' file selector button is clicked."""
        filename = QFileDialog.getOpenFileName(self, "",
                                               self.usefileLine.text())
        if filename != "":
            self.usefileLine.setText(filename)
            self.enableOk()

    def modelChanged(self, model):
        """Callback for when the model selection has changed."""
        self.fieldCombo.clear()
        for field in model.fieldModels:
            self.fieldCombo.addItem(field.name, QVariant(field))
            if field.name == "Kanji":
                self.fieldCombo.setCurrentIndex(self.fieldCombo.count() - 1)

    @pyqtSignature("")
    def on_buttonBox_helpRequested(self):
        """Callback for when the 'Help' button is clicked."""
        self.helpDialog.showHelp()
        self.helpDialog.exec_()

    def accept(self):
        """Callback for when the Ok button is clicked."""
        self.usefile = self.usefileLine.text()
        self.model = mw.deck.currentModel
        self.field = self.fieldCombo.itemData(self.fieldCombo.currentIndex()).\
                toPyObject()
        self.cardModels = [ c for c in mw.deck.currentModel.cardModels
                           if c.active ]

        self.modelChooser.deinit()
        QDialog.accept(self)

    def reject(self):
        """Callback for when the Cancel button is clicked."""
        self.modelChooser.deinit()
        QDialog.reject(self)

