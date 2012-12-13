#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Table data model, proxy model, data edit delegates, parsing routine, default constants
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import codecs as co
import re
from datetime import datetime as dt

from settings import *

HEADERS = (u'Book',
           u'Author',
           u'Type',
           u'Page',
           u'Location',
           u'Date',
           u'Text')
DEFAULT_DELIMITER = '=' * 10
DEFAULT_PATTERN = ur"""
                ^\s*                           	# 
                (?P<%s>.*?)                     # Book name
                (Inactive (?P<%s>.*?))?         # Eats up Author Header
                \s*-\                           #
                (?P<%s>\w*)                     # Clipping type
                (Inactive (?P<%s>.*?))?         # Eats up Page Header
                .*(Loc.|Page)\                  #
                (?P<%s>[\d-]*)           	# Location
                .*?Added\ on\             	#
                (?P<%s>(.*)(AM|PM))             # Date & time
                \s*                            	# 
                (?P<%s>.*?)                     # Text
                \s*$ 		                #
                """ % HEADERS
DEFAULT_RE_OPTIONS = re.UNICODE | re.VERBOSE
DEFAULT_DATE_FORMAT = {'Qt' : 'dddd, MMMM dd, yyyy, hh:mm AP',
                       'Python' : '%A, %B %d, %Y, %I:%M %p'}
DEFAULT_ENCODIG = ['utf-8', 'utf-16']
DEFAULT_EXTENSION = ['txt',]

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

class ComboBoxDeligate(QStyledItemDelegate):
    """
    Type of the note edit delegate, QComboBox with 3 predefined values:
    Highlight, Bookmark, Note.
    """
    
    def __init__(self, parent = None):
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
    
    def __init__(self, parent = None):
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
        
class TableModel(QAbstractTableModel):
    """
    Table model, all the data are stored in the Clippings object tableData.
    Returns status string.
    """
    tableData = Clippings()

    def __init__(self, parent = None):
        QAbstractTableModel.__init__(self, parent)
        self.tableData = Clippings()

    def parse(self, fileName, append = False, default = True, delimiter = None, notePattern = None, dateFormat = None, encoding = None):
        """
        Parse My clippings.txt to fetch data
        """


        self.beginResetModel()

        # Clear previous data
        if not append:
            self.tableData = Clippings()
        if default:
            delimiter = DEFAULT_DELIMITER
            notePattern = DEFAULT_PATTERN
            dateFormat = DEFAULT_DATE_FORMAT
            encoding = DEFAULT_ENCODIG[0]
        status = ''

        # Load Settings
        self.settings = Settings()
        self.attachNotes = self.settings['Application Settings']['Attach Notes']['Attach Notes']
        self.notesPosition = self.settings['Application Settings']['Attach Notes']['Notes Position']
        self.delimiters = {'Before' : self.settings['Application Settings']['Attach Notes']['Delimiter Before Highlights'],
                           'After' : self.settings['Application Settings']['Attach Notes']['Delimiter After Highlights']}

        try:
            myClippings = co.open(fileName, 'r', encoding).read()
        except:
            myClippings = co.open(fileName, 'r', DEFAULT_ENCODIG[1]).read()

        clip = myClippings.split(delimiter)
        if clip[-1].strip() == '' : clip.pop(-1)
        pattern = re.compile(notePattern, DEFAULT_RE_OPTIONS)

        import_data = Clippings() # If we need to modify the original table data, set up a new Clippings
        clipNo = 0
        for c in clip:
            clipNo += 1
            try:
                #if c.strip() == '' : continue
                line = {}
                search = pattern.search(c.strip())
                emptyHeaders = 0
                for h in self.tableData.headers:
                    try:
                        # Try to convert date to shorter format string, using standard datetime function
                        # as QDateTime support only local format strings.
                        # Date converted to QDateTime object for compatibility purpose.
                        if h == 'Date':
                            try:
                                date = QDateTime(dt.strptime(search.group(h), dateFormat['Python']))
                            except:
                                date = QDateTime.fromString(search.group(h), dateFormat['Qt'])
                            line[h] = {Qt.DisplayRole : QDateTime.toString(date, 'dd.MM.yy, hh:mm'), Qt.EditRole : date}
                        else:
                            line[h] = {Qt.DisplayRole : search.group(h), Qt.EditRole : search.group(h)}
                    except:
                        # If header is not found set it empty string
                        line[h] = {Qt.DisplayRole : '', Qt.EditRole : ''}
                        emptyHeaders += 1
                        if emptyHeaders == len(self.tableData.headers):
                            raise
                # Attach note to the coressponding highlight, if it is not
                # the first entry and set in settings
                rows = len(import_data)

                #self.tableData[rows] = line
                import_data.append(line)


            except:
                # Inform about invalid note
                status += u' Warning: note %d is empty or in wrong format: \r\n%s\r\n' % (clipNo,
                                                                                          c.strip())
                continue

        status = u'<%s> From file "%s" %d out of %d notes are successfully processed\r\n%s' % (QTime.currentTime().toString('hh:mm:ss'),
                                                                                               QDir.dirName(QDir(fileName)),
                                                                                               len(import_data),
                                                                                               clipNo,
                                                                                               status)

        # The original approach did this as lines were imported.  Since Kindle now puts the note before the highlight,
        # we need to post-process the data.

        if self.attachNotes == 'True':
            skip = False # This makes it easy to skip subsequent rows
            for row in range(len(import_data)):
                if skip:
                    skip = False
                else:
                    if import_data[row][u'Type'][Qt.DisplayRole] == (self.settings['Application Settings']['Language']['Note'], 'Note')[self.settings['Application Settings']['Language']['Note'] == '']:
                        # We've found a notes row
                        # Now we need to decide if we're checking forward or backwards
                        if self.notesPosition == 'After highlights' and\
                           row > 0 and\
                           import_data[row][u'Date'][Qt.DisplayRole] == import_data[row - 1][u'Date'][Qt.DisplayRole] and\
                           import_data[row][u'Book'][Qt.DisplayRole] == import_data[row - 1][u'Book'][Qt.DisplayRole]:
                            # Edit previous row

                            highlight = '%s%s%s' % (self.delimiters['Before'],
                                                    import_data[row - 1][u'Text'][Qt.DisplayRole],
                                                    self.delimiters['After'])
                            self.tableData[len(self.tableData)-1][u'Text'][Qt.DisplayRole] = '%s%s' % (import_data[row][u'Text'][Qt.DisplayRole], highlight)
                            self.tableData[len(self.tableData)-1][u'Text'][Qt.EditRole] = self.tableData[len(self.tableData)-1][u'Text'][Qt.DisplayRole]

                        elif self.notesPosition == 'Before highlights' and\
                             import_data[row][u'Date'][Qt.DisplayRole] == import_data[row + 1][u'Date'][Qt.DisplayRole] and\
                             import_data[row][u'Book'][Qt.DisplayRole] == import_data[row + 1][u'Book'][Qt.DisplayRole]:
                            # Combine with next row, skip next row

                            highlight = '%s%s%s' % (self.delimiters['Before'],
                                                    import_data[row + 1][u'Text'][Qt.DisplayRole],
                                                    self.delimiters['After'])
                            import_data[row][u'Text'][Qt.DisplayRole] = '%s%s' % (import_data[row][u'Text'][Qt.DisplayRole], highlight)
                            import_data[row][u'Text'][Qt.EditRole] = import_data[row][u'Text'][Qt.DisplayRole]

                            self.tableData.append(import_data[row])
                            skip = True
                            # create modified row and append


                    else:
                        #self.tableData[rows] = line
                        self.tableData.append(import_data[row])
        else:
            for row in import_data:
                self.tableData.append(row)

        self.endResetModel()
        return status

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
                self.tableData[index.row()][self.tableData.headers[index.column()]][Qt.DisplayRole] = value.toDateTime().toString('dd.MM.yy, hh:mm')
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
        return Qt.ItemIsSelectable |\
               Qt.ItemIsEditable |\
               Qt.ItemIsEnabled |\
               Qt.ItemIsDragEnabled
    
    def mimeTypes(self):
        types = ['application/vnd.text.list',]
        return types
    
    def mimeData(self, indexes):
        mimeData = QMimeData()
        text = ''
        # Sort indexes, because sometimes they are given in wrong order
        indexes.sort()
        for i in range(0, len(indexes), len(self.tableData.headers)):
            if indexes[i].column() == 0:
                text += '%s\r\n- %s Loc. %s  | Added on %s\r\n\r\n%s\r\n==========\r\n' %\
                     (self.data(indexes[i], Qt.DisplayRole),
                      self.data(indexes[i+1], Qt.DisplayRole),
                      self.data(indexes[i+2], Qt.DisplayRole),
                      self.data(indexes[i+3], Qt.EditRole).toString('dddd, MMMM dd, yyyy, hh:mm AP'),
                      self.data(indexes[i+4], Qt.DisplayRole))

        mimeData.setText(text)
        return mimeData
