#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#  DaleyKlippings
#  Copyright (C) 2012-14 Clayton Daley III
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
from pprint import pformat

logger = logging.getLogger("daley_klippings.table")
logger.info("Loading DaleyKlippings Table Models")

"""
Table data model, proxy model, data edit delegates, parsing routine, default constants
"""
import re
import itertools
import operator
from datetime import datetime as dt
from PySide.QtCore import QAbstractTableModel, QMimeData, QTime, QDateTime
from settings import *  # Includes re, PySide, pformat


HEADERS = (u'Book',
           u'Author',
           u'Type',
           u'Page',
           u'Location',
           u'Date',
           u'Highlight',
           u'Note')


class RegexImport(object):
    def __init__(self, language, import_pattern):
        self.language = language
        self.import_pattern = import_pattern

    def parse(self, my_clippings):
        """
        Parse My clippings.txt to fetch data
        """
        detail = ''

        delimiter = self.import_pattern['Delimiter']

        raw_clippings = my_clippings.split(delimiter)
        if raw_clippings[-1].strip() == '':
            raw_clippings.pop(-1)
        try:
            pattern = re.compile(self.import_pattern['Pattern'], self.DEFAULT_RE_OPTIONS)
        except Exception as error:
            return u'The Import Pattern is invalid.', \
                   'Import Pattern resulted in the error:\n%s' % str(error.message)

        date_format = self.import_pattern['Date Format']
        date_language = self.language['Date Language']
        note_translation = self.language['Note']
        bookmark_word = self.language['Bookmark']
        highlight_word = self.language['Highlight']

        import_data = Clippings()
        clipNo = 0
        for raw_clipping in raw_clippings:
            clipNo += 1
            try:
                clipping = pattern.search(raw_clipping.strip())
                line = {}
                emptyHeaders = 0
                for h in self.headers:
                    try:
                        # Try to convert date to shorter format string, using standard datetime function
                        # as QDateTime support only local format strings.
                        # Date converted to QDateTime object for compatibility purpose.
                        if h == 'Date':
                            logger.debug("Original date is: '%s'" % clipping.group(h))
                            # Attempt to Localize Date
                            if date_language != 'English (default)':
                                logger.debug("... trying to localize date")
                                try:
                                    local_language = QLocale(getattr(QLocale, date_language))
                                    date = local_language.toDateTime(clipping.group(h), date_format).toPython()
                                    logger.debug("... date converted to: '%s'" % str(date))
                                except Exception as e:
                                    logger.exception("... error localizing date:\n%s" % e.message)
                            else:
                                # Attempt to Standardize Date
                                if u'%' in date_format:
                                    # The % sign indicates that the pattern is a basic Python format
                                    date = dt.strptime(clipping.group(h), date_format)
                                else:
                                    # Otherwise, we assume a Qt Format
                                    date = QDateTime.fromString(clipping.group(h), date_format).toPython()
                            line[h] = date
                        elif h == 'Note' and clipping.group('Type') == note_translation:
                            line[h] = clipping.group('Text')
                        elif h == 'Highlight' and clipping.group('Type') == highlight_word:
                            line[h] = clipping.group('Text')
                        else:
                            line[h] = clipping.group(h)
                    except:
                        # If header is not found set it empty string
                        line[h] = ''
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


class RegexExport(object):
    DEFAULT_RE_OPTIONS = re.UNICODE | re.VERBOSE | re.DOTALL

    def __init__(self, export_pattern):
        self.export_pattern = export_pattern

    def export_(self, proxyModel):
        wildCards = re.findall(r'\?P<([^>]+)>', self.export_pattern['Body'], re.UNICODE)
        logger.info("wildCards are %s" % pformat(wildCards))

        rows = []

        rows.append(self.export_pattern['Header'])

        for row in range(self.proxyModel.rowCount()):
            bodyLine = self.export_pattern['Body']
            for i in wildCards:
                bodyLine = bodyLine.replace(u'?P<%s>' % i, self.processWildcard(self.export_pattern['Name'], i, row, self.export_pattern['Date Format']))
            rows.append(bodyLine)

        rows.append(self.export_pattern['Bottom'])

        return '\r\n'.join(rows)

    def processWildcard(self, template_name, wildcard, row, dateFormat):
        try:
            # Upgraded Text tag must be pre-processed since prefixes are only applied to unAttached notes and highlights
            if wildcard[-4:] == 'Text':
                # Consider adding code for bookmarks
                if self.processWildcard(template_name, 'Type', row, dateFormat) == 'Bookmark':
                    return u''
                elif self.processWildcard(template_name, 'Type', row, dateFormat) == 'Highlight':
                    return self.processWildcard(template_name, wildcard[:-4] + 'Highlight', row, dateFormat)
                elif self.processWildcard(template_name, 'Type', row, dateFormat) == 'Note' and \
                        self.processWildcard(template_name, 'Highlight', row, dateFormat) == '':
                    return self.processWildcard(template_name, wildcard[:-4] + 'Note', row, dateFormat)
                else:
                    response = self.settings['Export Settings'][template_name]['Notes']
                    if response == '':
                        return u'ERROR:  Please configure custom text pattern.'
                    else:
                        wildCards = re.findall(r'\?P<(.*?)>', response, re.UNICODE)
                        for i in wildCards:
                            if 'Text' in i:  # This prevents recursion
                                response = response.replace(u'?P<%s>' % i, u'')
                            else:
                                response = response.replace(u'?P<%s>' % i,
                                                            self.processWildcard(template_name, i, row, dateFormat))
                        return response

            # support for prefixes
            elif wildcard[:11] == 'EvernoteTag':
                replace_string = self.processWildcard(template_name, 'Ellipsis100CommaSafe' + wildcard[11:], row,
                                                      dateFormat)
                if len(replace_string) > 0:
                    replace_string = u'<tag>' + replace_string + u'</tag>'
                return replace_string
            elif wildcard[:11] == 'QuoteEscape':
                return re.sub(u'"', u'""', self.processWildcard(template_name, wildcard[11:], row, dateFormat))
            elif wildcard[:11] == 'CommaEscape':
                return re.sub(u',', u'\,', self.processWildcard(template_name, wildcard[11:], row, dateFormat))
            elif wildcard[:9] == 'CommaSafe':
                return re.sub(u',', u"_", self.processWildcard(template_name, wildcard[9:], row, dateFormat))
            elif wildcard[:9] == 'QuoteSafe':
                return re.sub(u'"', "'", self.processWildcard(template_name, wildcard[9:], row, dateFormat))
            elif wildcard[:7] == 'TabSafe':
                return re.sub(u'\t', "     ", self.processWildcard(template_name, wildcard[7:], row, dateFormat))
            elif wildcard[:11] == 'XmlSafeSpan':
                return u'<span title="value_' + wildcard[11:].lower() + u'">' + \
                       self.processWildcard(template_name, u'XmlSafe' + wildcard[11:], row, dateFormat) + \
                       u'</span>'
            elif wildcard[:7] == 'XmlSafe':
                return re.sub('<', '&lt;', re.sub('>',
                                                  '&gt;',
                                                  re.sub('&',
                                                         '&amp;',
                                                         self.processWildcard(
                                                             template_name,
                                                             wildcard[7:],
                                                             row,
                                                             dateFormat))
                                                  )
                              )
            elif wildcard[:4] == 'Span':
                return u'<span title="value_' + wildcard[11:].lower() + u'">' + \
                       self.processWildcard(template_name, wildcard[4:], row, dateFormat) + u'</span>'

            elif wildcard[:8] == 'Ellipsis':
                if wildcard[8:11].isdigit():
                    truncate_len = int(wildcard[8:11])
                    replace_string = self.processWildcard(template_name, wildcard[11:], row, dateFormat)
                    if len(replace_string) > truncate_len:
                        if truncate_len > 3:
                            replace_string = self.processWildcard(template_name, wildcard[11:], row, dateFormat)[
                                             :(truncate_len - 3)] + '...'
                        else:
                            replace_string = self.processWildcard(template_name, wildcard[11:], row, dateFormat)[
                                             :truncate_len]
                    if len(replace_string) > 0:
                        return replace_string
                else:
                    return ''
            elif wildcard[:8] == 'Truncate':
                if wildcard[8:11].isdigit():
                    truncate_len = int(wildcard[8:11])
                    replace_string = self.processWildcard(template_name, wildcard[11:], row, dateFormat)
                    if len(replace_string) > truncate_len > 3:
                        replace_string = self.processWildcard(template_name, wildcard[11:], row, dateFormat)[
                                         :truncate_len]
                    if len(replace_string) > 0:
                        return replace_string
                else:
                    return ''

                    # return data types
            elif wildcard == 'Date':
                #return unicode(self.proxyModel.data(self.proxyModel.index(row, HEADERS.index(wildcard)),
                #                                    Qt.EditRole).toPython().toString(dateFormat))
                item = self.proxyModel.data(self.proxyModel.index(row, HEADERS.index(wildcard)), Qt.DisplayRole)
                if u'%' in self.date_format:
                    # The % sign indicates that the pattern is a basic Python format
                    return item.strftime(self.date_format).strip()
                else:
                    # Otherwise, we assume a Qt Format
                    return QDateTime(item).toString(self.date_format).strip()
            else:
                #return unicode(self.proxyModel.data(self.proxyModel.index(row, HEADERS.index(wildcard)),
                #                                    Qt.DisplayRole).toString())
                return self.proxyModel.data(self.proxyModel.index(row, HEADERS.index(wildcard)), Qt.DisplayRole)

        except Exception as err:
            # re.sub produces spurious errors about Unicode
            # logger.exception("Error: " + err.message)
            return u''


class CsvParser(object):
    def import_(self, csv_reader):
        detail = ''
        try:
            line = csv_reader.next()
        except StopIteration:
            return "CSV Import Failed\r\n\r\nNo data found.", \
                   'When loading first row, the CSV importer returned StopIteration, indicating that no data was ' + \
                   'available.  However, the file seems to exist since we reached this point.  Make sure you ' + \
                   'selected the correct file and that the file is in the correct format.'
        headers = []
        # We assume the top line is headers.  Even if the headers aren't used, we need to know the identity of the
        # column during import so we add them anyway.
        for h in line:
            logger.info("Adding %s to headers" % h)
            headers.append(h)
        # To ensure the table responds to all the right columns, we add the remaining headers.  Our strategy later will
        # set the value of these additional headers to None
        missing_headers = 0
        for h in self.headers:
            if h not in headers:
                missing_headers += 1
                logger.info("Adding %s to headers" % h)
                detail += '%s was not included in source data so it will be initialized with empty data.\r\n' % h
                headers.append(h)
        if missing_headers == len(self.headers):
            return 'Error importing file. No valid headers found.', \
                   'The CSV Importer assumes that the first row is a list of headers.  This tells DaleyKlippings ' + \
                   'how to map the CSV columns to data.  When importing this first row, none of the columns matched ' + \
                   'the headers expected by DaleyKlippings.  Please confirm that the headers are in English (not ' + \
                   'the translated versions) and use the same capitalization as the headers in the UI.'

        # Now add the actual data, but don't rewind
        for line in csv_reader:
            logger.debug("Processing line %s" % pformat(line))
            self.append(dict(itertools.izip_longest(headers, line)))
            #self.append({(k, v) for k, v in dict(itertools.izip_longest(headers, line)) if k in self.headers})
            logger.debug("... added")

        logger.info("After import, object is %s" % pformat(self))

        return 'CSV Import Completed', detail

    def export_(self):
        pass


class NoteHandler(object):
    def __init__(self, notes, language):
        self.notes = notes
        self.language = language

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

    @classmethod
    def match(self, matches):
        notesPosition = self.notes['Position']
        range_indicator = self.language['Range Separator']

        matched = 0
        skip = False  # This makes it easy to skip subsequent rows

        # Sort Rows - A strange situation can arise if you first highlight a region and, subsequently, return and add
        # a note to the same range. The Note will be placed chronologically at the point where it was created, but the
        # highlight is not duplicated. Sorting rows by author and location will improve the odds that we are able to
        # detect and attach notes in this condition.

        for row in range(len(matches)):
            # Once we match two lines, we don't want to process the second line again.  This is especially
            # problematic in Automatic mode since we could match both forward and backwards.
            if skip:
                skip = False
                continue

            # If the current row is a note, we want to check and see if the next row is a matching highlight
            if matches[row][u'Type'] == self.language['Note']:
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
                    row < len(matches) - 1 and \
                    matches[row + 1][u'Type'] == self.language['Highlight'] and \
                    matches[row][u'Book'] == matches[row + 1][u'Book'] and \
                    any(
                        (
                            int(u'-1') if matches[row][u'Location'] is None else
                            int(matches[row][u'Location'])) == s for s in (
                                [int(u'-1')] if matches[row + 1][u'Location'] is None
                                else self.hyphen_range(matches[row + 1][u'Location'],
                                                       range_indicator=range_indicator))
                    ) and any(
                        (
                            int(u'-1') if matches[row][u'Page'] is None else
                            int(matches[row][u'Page']))== s for s in (
                                [int(u'-1')] if matches[row + 1][u'Page'] is None \
                                else self.hyphen_range(matches[row + 1][u'Page'],
                                                       range_indicator=range_indicator))
                    ):

                    matches[row][u'Highlight'] = matches[row + 1][u'Highlight']
                    matches[row][u'Location'] = matches[row + 1][u'Location']
                    self.append(matches[row])
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
                    matches[row - 1][u'Type'] == self.language['Highlight'] and \
                    matches[row][u'Book'] == \
                        matches[row - 1][u'Book'] and \
                    any(
                        (
                            int(u'-1') if matches[row][u'Location'] is None else
                            int(matches[row][u'Location'])) == s for s in (
                                [int(u'-1')] if matches[row - 1][u'Location'] is None else
                                self.hyphen_range(matches[row - 1][u'Location'],
                                                  range_indicator=range_indicator))
                    ) and any(
                        (
                            int(u'-1') if matches[row][u'Page'] is None else
                            int(matches[row][u'Page'])) == s for s in (
                                [int(u'-1')] if matches[row - 1][u'Page'] is None else
                                self.hyphen_range(matches[row - 1][u'Page'],
                                                  range_indicator=range_indicator))
                    ):

                    # In case the auto matcher already matched and skipped the previous highlight
                    if self[len(self) - 1][u'Type'] == self.language['Highlight']:
                        # If not, edit the highlight's entry in tableData
                        self[len(self) - 1][u'Note'] = matches[row][u'Note']
                        self[len(self) - 1][u'Type'] = matches[row][u'Type']
                    else:
                        # If so, attach the highlight to the new note as well
                        matches[row][u'Highlight'] = matches[row - 1][u'Highlight']
                        self.append(matches[row])
                    matched += 1

                else:
                    self.append(matches[row])

            else:
                self.append(matches[row])

        return summary, detail


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
    table_data = Clippings()

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.table_data = Clippings()

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

        summary, detail = self.table_data.import_(my_clippings=my_clippings, import_settings=import_settings)
        self.endResetModel()
        return summary, detail

    def from_csv(self, csv_reader, append=True):
        """
        Update
        """
        self.beginResetModel()

        # Clear previous data
        if not append:
            self.reset()

        summary, detail = self.table_data.import_csv(csv_reader=csv_reader)
        self.endResetModel()
        return summary, detail

    def reset(self):
        self.table_data = Clippings()

    def rowCount(self, index):
        return len(self.table_data)

    def columnCount(self, index):
        return len(self.table_data.headers)

    def data(self, index, role):
        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.table_data[row][self.table_data.headers[column]]

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.table_data.headers[section]
        if orientation == Qt.Vertical:
            if role == Qt.DisplayRole:
                return section + 1

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.table_data[index.row()][self.table_data.headers[index.column()]] = value
            """
            if self.table_data.headers[index.column()] == 'Date':
                # This is necessary because Qt uses a QVariant to get around typing issues
                self.table_data[index.row()][self.table_data.headers[index.column()]] = value.toPython()
            else:
                # This is necessary because Qt uses a QVariant to get around typing issues
                self.table_data[index.row()][self.table_data.headers[index.column()]] = value
            """

        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
        return True

    def removeRows(self, row, count, parent):
        self.beginRemoveRows(parent, row, row + count - 1)
        del self.table_data[row]
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
        for i in range(0, len(indexes), len(self.table_data.headers)):
            if indexes[i].column() == 0:
                text += '%s\r\n- %s Loc. %s  | Added on %s\r\n\r\n%s\r\n==========\r\n' % \
                        (self.data(indexes[i], Qt.DisplayRole),
                         self.data(indexes[i + 1], Qt.DisplayRole),
                         self.data(indexes[i + 2], Qt.DisplayRole),
                         self.data(indexes[i + 3], Qt.EditRole).toString('dddd, MMMM dd, yyyy, hh:mm AP'),
                         self.data(indexes[i + 4], Qt.DisplayRole))

        mimeData.setText(text)
        return mimeData
