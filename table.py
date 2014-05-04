#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#  DaleyKlippings
#  Copyright (C) 2012-13 Clayton Daley III
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
logger = logging.getLogger("daley_klippings.table")
logger.info("Loading DaleyKlippings Table Models")

"""
Table data model, proxy model, data edit delegates, parsing routine, default constants
"""
from PyQt4 import Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import re
from datetime import datetime as dt

from settings import *


class DateEditDelegate(QStyledItemDelegate):
    """
    Date edit delegate, set date format to 'dd.MM.yy, hh:mm' or 
    '%d.%m.%y, %H:%M' in Python designations
    """

    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = QDateTimeEdit(parent)
        editor.setCalendarPopup(True)
        editor.setDisplayFormat('dd.MM.yy, hh:mm')
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole).toDateTime()
        editor.setDateTime(value)

    def setModelData(self, editor, model, index):
        value = editor.dateTime().toString('dd.MM.yy, hh:mm')
        model.setData(index, editor.dateTime(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class ComboBoxDelegate(QStyledItemDelegate):
    """
    Type of the note edit delegate, QComboBox with 3 predefined values:
    Highlight, Bookmark, Note.
    """

    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.setAutoCompletion(True)
        # Load language settings
        settings = Settings()['Application Settings']['Language']
        highlight = (settings['Highlight'], 'Highlight')[settings['Highlight'] == '']
        note = (settings['Note'], 'Note')[settings['Note'] == '']
        bookmark = (settings['Bookmark'], 'Bookmark')[settings['Bookmark'] == '']

        editor.addItems([highlight, note, bookmark])
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole).toString()
        editor.setCurrentIndex(editor.findText(value))

    def setModelData(self, editor, model, index):
        value = editor.itemText(editor.currentIndex())
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


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
        value = index.model().data(index, Qt.EditRole).toString()
        editor.setText(value)

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


# Changed structure to list from dictionary to avoid problems with implementation of
# deleting rows function
class Clippings(list):
    """
    Object to store all table data. Object structure:
    - (headers)
    - [ 
      - {headers:
        - {role:
          - {item}}}]
    """

    headers = HEADERS

    def __init__(self):
        list.__init__(self)

    def import_(self, my_clippings, import_settings):
        """
        Parse My clippings.txt to fetch data
        """
        detail = ''

        delimiter = import_settings['Delimiter']

        raw_clippings = my_clippings.split(delimiter)
        if raw_clippings[-1].strip() == '':
            raw_clippings.pop(-1)
        try:
            pattern = re.compile(import_settings['Pattern'], DEFAULT_RE_OPTIONS)
        except Exception as error:
            return u'The Import Pattern is invalid.', \
                   'Import Pattern resulted in the error:\n%s' % str(error.message)

        date_format = import_settings['Date Format']
        language_settings = import_settings['Application Settings']['Language']
        date_language = language_settings['Date Language']
        note_translation = language_settings['Note']
        bookmark_translation = language_settings['Bookmark']
        highlight_translation = language_settings['Highlight']

        import_data = Clippings()
        clipNo = 0
        for raw_clipping in raw_clippings:
            clipNo += 1
            try:
                #if c.strip() == '' : continue
                clipping = pattern.search(raw_clipping.strip())
                line = {}
                emptyHeaders = 0
                for h in self.headers:
                    try:
                        # Try to convert date to shorter format string, using standard datetime function
                        # as QDateTime support only local format strings.
                        # Date converted to QDateTime object for compatibility purpose.
                        if h == 'Date':
                            logger.info("Original date is: '%s'" % clipping.group(h))
                            # Attempt to Localize Date
                            if date_language != 'English (default)':
                                logger.info("... trying to localize date")
                                try:
                                    local_language = QLocale(getattr(QLocale, import_settings['Application Settings']['Language']['Date Language']))
                                    date = local_language.toDateTime(clipping.group(h), date_format)
                                    logger.info("... date converted to: '%s'" % date.toString())
                                except Exception as e:
                                    logger.exception("... error localizing date:\n%s" % e.message)
                            else:
                                # Attempt to Standardize Date
                                if u'%' in date_format:
                                    # The % sign indicates that the pattern is a basic Python format
                                    date = QDateTime(dt.strptime(clipping.group(h), date_format))
                                else:
                                    # Otherwise, we assume a Qt Format
                                    date = QDateTime.fromString(clipping.group(h), date_format)
                            line[h] = {Qt.DisplayRole: QDateTime.toString(date, 'dd.MM.yy, hh:mm'), Qt.EditRole: date}
                        elif h == 'Note' and clipping.group('Type') == note_translation:
                            line[h] = {Qt.DisplayRole: clipping.group('Text'), Qt.EditRole: clipping.group('Text')}
                        elif h == 'Highlight' and clipping.group('Type') == highlight_translation:
                            line[h] = {Qt.DisplayRole: clipping.group('Text'), Qt.EditRole: clipping.group('Text')}
                        else:
                            line[h] = {Qt.DisplayRole: clipping.group(h), Qt.EditRole: clipping.group(h)}
                    except:
                        # If header is not found set it empty string
                        line[h] = {Qt.DisplayRole: '', Qt.EditRole: ''}
                        emptyHeaders += 1
                        if emptyHeaders == len(self.headers):
                            raise
                import_data.append(line)

            except Exception as e:
                # Inform about invalid note
                detail += u'\r\nWarning: note %d is empty or in wrong format: \r\n%s\r\n' % \
                          (clipNo, raw_clipping.strip())
                logger.exception("Clipping number %s resulted in the exception: %s" % (clipNo, e.message))
                continue

        detail = u'<%s> %d out of %d clippings were successfully processed.\r\n%s' % (
            QTime.currentTime().toString('hh:mm:ss'),
            len(import_data),
            clipNo,
            detail)

        # The original approach did this as lines were imported.  Since Kindle now puts the note before the highlight,
        # we need to post-process the data.
        attachNotes = import_settings['Application Settings']['Attach Notes']['Attach Notes']
        notesPosition = import_settings['Application Settings']['Attach Notes']['Notes Position']
        range_indicator = language_settings['Range Separator']

        matched = 0
        if attachNotes == 'True':
            skip = False  # This makes it easy to skip subsequent rows
            for row in range(len(import_data)):
                # Once we match two lines, we don't want to process the second line again.  This is especially
                # problematic in Automatic mode since we could match both forward and backwards.
                if skip:
                    skip = False
                    continue

                # If the current row is a note, we want to check and see if the next row is a matching highlight
                if import_data[row][u'Type'][Qt.DisplayRole] in [note_translation, 'Note']:
                    # We've found a notes row
                    # Automatic prefers notes before highlights so we start there
                    # If the before match fails (or if the user chooses "After highlights"), we try the after match
                    if (
                        # We're looking for notes before highlights
                        # and there is a next row to analyze
                        # and the next row is a highlight
                        # and the name of the books match
                        # and either there is no location on the highlight or the note location falls in the highlight range
                        # and either there is no page or the highlight or the note page falls in the highlight range
                        notesPosition == 'Before highlights' or notesPosition == 'Automatic (default)') and \
                        row < len(import_data) - 1 and \
                        import_data[row + 1][u'Type'][Qt.DisplayRole] == highlight_translation and \
                        import_data[row][u'Book'][Qt.DisplayRole] == \
                            import_data[row + 1][u'Book'][Qt.DisplayRole] and \
                        any(
                            (
                                int(u'-1') if import_data[row][u'Location'][Qt.DisplayRole] is None else
                                int(import_data[row][u'Location'][Qt.DisplayRole])) == s for s in (
                                    [int(u'-1')] if import_data[row + 1][u'Location'][Qt.DisplayRole] is None
                                    else self.hyphen_range(import_data[row + 1][u'Location'][Qt.DisplayRole],
                                                           range_indicator=range_indicator))
                        ) and any(
                            (
                                int(u'-1') if import_data[row][u'Page'][Qt.DisplayRole] is None else
                                int(import_data[row][u'Page'][Qt.DisplayRole]))== s for s in (
                                    [int(u'-1')] if import_data[row + 1][u'Page'][Qt.DisplayRole] is None \
                                    else self.hyphen_range(import_data[row + 1][u'Page'][Qt.DisplayRole],
                                                           range_indicator=range_indicator))
                        ):

                        import_data[row][u'Highlight'] = import_data[row + 1][u'Highlight']
                        import_data[row][u'Location'] = import_data[row + 1][u'Location']
                        self.append(import_data[row])
                        matched += 1
                        skip = True

                    elif (
                        # We're looking for notes after highlights
                        # and there is a previous row to analyze
                        # and the previous row is a highlight
                        # and the name of the books match
                        # and either there is no location on the highlight or the note location falls in the highlight range
                        # and either there is no page or the highlight or the note page falls in the highlight range
                        notesPosition == 'After highlights'
                        or notesPosition == 'Automatic (default)') and \
                        row > 0 and \
                        import_data[row - 1][u'Type'][Qt.DisplayRole] == highlight_translation and \
                        import_data[row][u'Book'][Qt.DisplayRole] == \
                            import_data[row - 1][u'Book'][Qt.DisplayRole] and \
                        any(
                            (
                                int(u'-1') if import_data[row][u'Location'][Qt.DisplayRole] is None else
                                int(import_data[row][u'Location'][Qt.DisplayRole])) == s for s in (
                                    [int(u'-1')] if import_data[row - 1][u'Location'][Qt.DisplayRole] is None else
                                    self.hyphen_range(import_data[row - 1][u'Location'][Qt.DisplayRole],
                                                      range_indicator=range_indicator))
                        ) and any(
                            (
                                int(u'-1') if import_data[row][u'Page'][Qt.DisplayRole] is None else
                                int(import_data[row][u'Page'][Qt.DisplayRole])) == s for s in (
                                    [int(u'-1')] if import_data[row - 1][u'Page'][Qt.DisplayRole] is None else
                                    self.hyphen_range(import_data[row - 1][u'Page'][Qt.DisplayRole],
                                                      range_indicator=range_indicator))
                        ):

                        # In case the auto matcher already matched and skipped the previous highlight
                        if self[len(self) - 1][u'Type'][Qt.DisplayRole] == highlight_translation:
                            # If not, edit the highlight's entry in tableData
                            self[len(self) - 1][u'Note'] = import_data[row][u'Note']
                            self[len(self) - 1][u'Type'] = import_data[row][u'Type']
                        else:
                            # If so, attach the highlight to the new note as well
                            import_data[row][u'Highlight'] = import_data[row - 1][u'Highlight']
                            self.append(import_data[row])
                        matched += 1

                    else:
                        self.append(import_data[row])

                else:
                    self.append(import_data[row])

        else:  # if attach notes flag is not on
            for row in import_data:
                self.append(row)

        # Pop Import Status Box
        summary = u'%d out of %d clippings were successfully processed%s' % \
                  (len(import_data), clipNo, u' ' * 50)
        if len(import_data) == 0 and clipNo > 0:
            summary += u'Please verify that you selected the right file or try a different Import Pattern.' + u' ' * 50 + \
                       u'\r\n\r\nIf none of the built-in patterns work, please contact daleyklippings@claytondaley.com.' + u' ' * 50
        else:
            if attachNotes == 'True':
                summary += u'\r\n - We were able to match %d Note%s with a Highlight %s' % \
                           (matched, ('s' if matched > 1 else ''), u' ' * 50)
                if matched > 0:
                    summary += u'\r\n - As a result, fewer lines will show up in the interface.' + u' ' * 50

        return summary, detail

    def hyphen_range(self, s, range_indicator='-'):
        """ Takes a range in form of "a-b" and generate a list of numbers between a and b inclusive.
        Also accepts comma separated ranges like "a-b,c-d,f" will build a list which will include
        Numbers from a to b, a to d and f """
        if s is None:
            return []
        s = u''.join(s.split())  #removes white space
        r = set()
        for x in s.split(','):
            t = x.split(range_indicator)
            if len(t) not in [1, 2]: raise SyntaxError(
                "hash_range is given its argument as %s which seems not correctly formatted." % s)
            # To support ranges like 2014-52 which really mean 2014-2052
            if len(t) == 2 and len(t[0]) > len(t[1]):
                t[1] = t[0][:(len(t[0]) - len(t[1]))] + t[1]
            r.add(int(t[0])) if len(t) == 1 else r.update(set(range(int(t[0]), int(t[1]) + 1)))
        l = list(r)
        l.sort()
        return l


class TableModel(QAbstractTableModel):
    """
    Table model, all the data are stored in the Clippings object tableData.
    Returns status string.
    """
    tableData = Clippings()

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.tableData = Clippings()

    def parse(self, my_clippings, import_settings, append=True):
        """
        Parse data in my_clippings using pattern in import_settings
        """
        self.beginResetModel()

        # Clear previous data
        if not append:
            self.reset()
        
        # Consider loading default import_settings if import_settings is None
        if import_settings is None:
            raise ValueError("Import Pattern not selected.")

        summary, detail = self.tableData.import_(my_clippings=my_clippings, import_settings=import_settings)
        self.endResetModel()
        return summary, detail

    def reset(self):
        self.tableData = Clippings()

    def rowCount(self, index):
        return len(self.tableData)

    def columnCount(self, index):
        return len(self.tableData.headers)

    def data(self, index, role):
        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.tableData[row][self.tableData.headers[column]][role]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.tableData.headers[section]
        if orientation == Qt.Vertical:
            if role == Qt.DisplayRole:
                return section + 1

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            if self.tableData.headers[index.column()] == 'Date':
                self.tableData[index.row()][self.tableData.headers[index.column()]][
                    Qt.DisplayRole] = value.toDateTime().toString('dd.MM.yy, hh:mm')
                self.tableData[index.row()][self.tableData.headers[index.column()]][role] = value.toDateTime()
            else:
                self.tableData[index.row()][self.tableData.headers[index.column()]][Qt.DisplayRole] = value.toString()
                self.tableData[index.row()][self.tableData.headers[index.column()]][role] = value.toString()

        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
        return True

    def removeRows(self, row, count, parent):
        self.beginRemoveRows(parent, row, row + count - 1)
        del self.tableData[row]
        self.endRemoveRows()
        return True

    def flags(self, index):
        return Qt.ItemIsSelectable | \
               Qt.ItemIsEditable | \
               Qt.ItemIsEnabled | \
               Qt.ItemIsDragEnabled

    def mimeTypes(self):
        types = ['application/vnd.text.list', ]
        return types

    def mimeData(self, indexes):
        mimeData = QMimeData()
        text = ''
        # Sort indexes, because sometimes they are given in wrong order
        indexes.sort()
        for i in range(0, len(indexes), len(self.tableData.headers)):
            if indexes[i].column() == 0:
                text += '%s\r\n- %s Loc. %s  | Added on %s\r\n\r\n%s\r\n==========\r\n' % \
                        (self.data(indexes[i], Qt.DisplayRole),
                         self.data(indexes[i + 1], Qt.DisplayRole),
                         self.data(indexes[i + 2], Qt.DisplayRole),
                         self.data(indexes[i + 3], Qt.EditRole).toString('dddd, MMMM dd, yyyy, hh:mm AP'),
                         self.data(indexes[i + 4], Qt.DisplayRole))

        mimeData.setText(text)
        return mimeData
