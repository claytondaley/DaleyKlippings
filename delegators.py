#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#  DaleyKlippings
#  Copyright (C) 2012-15 Clayton Daley III
#  daleyklippings@gmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
########################################################################
import logging
from PySide.QtCore import QDateTime, Qt

logger = logging.getLogger("daley_klippings.delegators")
logger.info("Loading DaleyKlippings Delegators")

from PySide.QtGui import QStyledItemDelegate, QDateTimeEdit, QComboBox, QLineEdit


# Helper classes for date cells in the table UI
class DateEditDelegate(QStyledItemDelegate):
    """
    Date edit delegate, attempts to localize dates, defaulting to 'dd.MM.yy, hh:mm'
    ('%d.%m.%y, %H:%M' in Python notation)
    """

    def __init__(self, parent=None, format=None):
        QStyledItemDelegate.__init__(self, parent)
        if format is not None:
            self.format = format
        else:
            self.format = 'dd.MM.yy, hh:mm'

    def createEditor(self, parent, option, index):
        editor = QDateTimeEdit(parent)
        editor.setCalendarPopup(True)
        editor.setDisplayFormat(self.format)
        return editor

    def setEditorData(self, editor, index):
        editor.setDateTime(QDateTime(index.model().data(index, Qt.EditRole)))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.dateTime().toPython(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def displayText(self, value, locale):
        if u'%' in self.format:
            # The % sign indicates that the pattern is a basic Python format
            return value.strftime(self.format)
        else:
            # Otherwise, we assume a Qt Format
            return QDateTime(value).toString(self.format)


# Helper class for clippings types in the table UI
class ComboBoxDelegate(QStyledItemDelegate):
    """
    Type of the note edit delegate, QComboBox with 3 predefined values:
    Highlight, Bookmark, Note.
    """

    def __init__(self, language, parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self.language = language

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems([self.language['Highlight'], self.language['Note'], self.language['Bookmark']])
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setCurrentIndex(editor.findText(value))

    def setModelData(self, editor, model, index):
        value = editor.itemText(editor.currentIndex())
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


# Helper type for location (and page) ranges in the table UI
class LocationEditDelegate(QStyledItemDelegate):
    """
    Loctaion edit delegate, QLineEdit with mask
    """

    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        #validator = QRegExpValidator(QRegExp('([0-9]+-?)*'), editor)
        #editor.setValidator(validator)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setText(value)

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


