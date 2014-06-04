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

"""
Main DaleyKlippings window
"""
import unicodecsv as csv

__ver__ = '1.3.1'
## Features: 
## - default import & export patterns
## - language settings for highlight, note & bookmark terms

import logging
logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler()
logger = logging.getLogger("daley_klippings")
logger.addHandler(handler)
logger.info("Loading DaleyKlippings")

import inspect
from pprint import pformat

from gui.ui_mainWin import *
from table import *
from settings import *


class MainWin(QMainWindow):
    """
    Main DaleyKlippings window class
    """

    # HACKY BUT FAST WAY TO DEBUG
    """
    def __getattribute__(self, item):
        returned = QMainWindow.__getattribute__(self, item)
        if inspect.isfunction(returned) or inspect.ismethod(returned):
            logger.debug("Call %s on instance of class %s" % (
                str(returned),
                QMainWindow.__getattribute__(QMainWindow.__getattribute__(self, '__class__'), '__name__')))
        return returned
    """

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # Initiate settings
        self.settings = Settings()

        # Initiate GUI
        self.ui = Ui_mainWin()
        self.ui.setupUi(self)
        self.ui.statusBar.addPermanentWidget(self.ui.rowIndicator)
        self.ui.tableView.horizontalHeader().setSortIndicator(-1, Qt.DescendingOrder)

        # Temporary options (next version)
        self.ui.actionHelp.setVisible(False)

        # Initiate toolbar
        self.initiateToolButtons()
        self.ui.toolBar.insertWidget(self.ui.actionFilter, self.ui.toolButtonImport)
        self.ui.toolBar.insertWidget(self.ui.actionFilter, self.ui.toolButtonAppend)
        self.ui.toolBar.insertWidget(self.ui.actionFilter, self.ui.toolButtonExport)
        self.ui.toolBar.insertSeparator(self.ui.actionFilter)

        # Screen filter line
        self.ui.filterCloseButton.setVisible(False)
        self.ui.filterOptionButton.setVisible(False)
        self.ui.filterEdit.setVisible(False)
        self.ui.filterCaseBox.setVisible(False)
        self.ui.filterLine.setVisible(False)

        # Initiate data model
        self.tableModel = TableModel()
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.tableModel)
        self.proxyModel.setSortRole(Qt.EditRole)
        self.proxyModel.setDynamicSortFilter(True)
        self.ui.tableView.setModel(self.proxyModel)

        self.proxyModel.setFilterCaseSensitivity(Qt.CaseSensitivity(False))
        self.proxyModel.setFilterKeyColumn(-1)

        # Initiate table context menu
        self.ui.tableView.addAction(self.ui.actionDeleteRow)
        self.ui.tableView.addAction(self.ui.actionResizeRowsToContents)
        self.ui.tableView.addAction(self.ui.actionResizeRows)

        # Initiate filterOptionButton menu
        self.menuFilterOption = QMenu()
        self.actionFilterAll = QAction('All columns', self)
        self.actionFilterAll.setCheckable(True)
        self.actionFilterAll.setChecked(True)
        self.actionFilterAll.setEnabled(False)
        self.menuFilterOption.addAction(self.actionFilterAll)
        self.connect(self.actionFilterAll, SIGNAL('triggered(bool)'), self.onFilterOptionTriggered)
        self.menuFilterOption.addSeparator()
        self.actionFilterHeaders = {}
        for h in self.tableModel.table_data.headers:
            self.actionFilterHeaders[h] = QAction(h, self)
            self.actionFilterHeaders[h].setCheckable(True)
            self.menuFilterOption.addAction(self.actionFilterHeaders[h])
            self.connect(self.actionFilterHeaders[h], SIGNAL('triggered(bool)'), self.onFilterOptionTriggered)
        self.ui.filterOptionButton.setMenu(self.menuFilterOption)

        self.updateDelegates()

        # Scroll table to the current cell after sorting
        self.connect(self.proxyModel, SIGNAL('layoutChanged()'), self.onLayoutChanged)

    def updateDelegates(self):
        # Initiate delegates
        typeDelegate = ComboBoxDelegate(self)
        locationDelegate = LocationEditDelegate(self)
        # Try to localize the dates
        date_language = self.settings['Application Settings']['Language']['Date Language']
        if date_language == "English (default)":
            # This is a default value not available in QLocale
            date_language = "English"
        logger.info("Date Language is %s" % date_language)
        local_language = QLocale(getattr(QLocale, date_language))
        date_format = local_language.dateFormat(format=QLocale.ShortFormat)
        time_format = local_language.timeFormat()
        # Remove time zone if included
        if time_format[-1:] == "t":
            time_format = time_format[:-1]
        logger.info("Localizing date formats to %s %s" % (date_format, time_format))
        dateDelegate = DateEditDelegate(self, format="%s %s" % (date_format, time_format))

        self.ui.tableView.setItemDelegateForColumn(2, typeDelegate)
        self.ui.tableView.setItemDelegateForColumn(3, locationDelegate)
        self.ui.tableView.setItemDelegateForColumn(4, locationDelegate)
        self.ui.tableView.setItemDelegateForColumn(5, dateDelegate)

    def initiateToolButtons(self):
        """
        This function is called to create the toolbar and anytime settings change (to update the list of patterns
        in the dropdown.
        """
        # Import Button
        self.menuButtonImport = QMenu()
        self.menuButtonImport.addAction(self.ui.actionImport)
        # Special (built-in) CSV Option
        csv_action = QAction("CSV", self.menuButtonImport)
        self.menuButtonImport.addAction(csv_action)
        self.connect(csv_action, SIGNAL('triggered(bool)'), self.onImportCsv)
        # Add Actions from Settings
        self.menuButtonImport.addSeparator()
        self.customImportActions = []
        for i in sorted(self.settings['Import Settings'].keys()):
            if 'Deleted' in self.settings['Import Settings'][i]:
                continue
            self.customImportActions.append(QAction(i, self.menuButtonImport))
            logger.debug("Added dropdown item %s (import)" % self.customImportActions[-1].text())
            self.connect(self.customImportActions[-1], SIGNAL('triggered(bool)'), self.onImportCustom)
        self.menuButtonImport.addActions(self.customImportActions)
        self.ui.toolButtonImport.setMenu(self.menuButtonImport)

        # Append Button
        self.menuButtonAppend = QMenu()
        self.menuButtonAppend.addAction(self.ui.actionAppend)
        # Special (built-in) CSV Option
        csv_action = QAction("CSV", self.menuButtonAppend)
        self.connect(csv_action, SIGNAL('triggered(bool)'), self.onImportCsv)
        self.menuButtonAppend.addAction(csv_action)
        # Add Actions from Settings
        self.menuButtonAppend.addSeparator()
        self.customAppendActions = []
        for i in sorted(self.settings['Import Settings'].keys()):
            if 'Deleted' in self.settings['Import Settings'][i]:
                continue
            logger.debug('Added dropdown item %s (append)' % i)
            self.customAppendActions.append(QAction(i, self.menuButtonAppend))
            self.connect(self.customAppendActions[-1], SIGNAL('triggered(bool)'), self.onImportCustom)
        self.menuButtonAppend.addActions(self.customAppendActions)
        self.ui.toolButtonAppend.setMenu(self.menuButtonAppend)

        # Export Button
        self.menuButtonExport = QMenu()
        self.menuButtonExport.addAction(self.ui.actionExport)
        # Special (built-in) CSV Option
        csv_action = QAction("CSV", self.menuButtonExport)
        self.connect(csv_action, SIGNAL('triggered(bool)'), self.onExportCsv)
        self.menuButtonExport.addAction(csv_action)
        # Add Actions from Settings
        self.menuButtonExport.addSeparator()
        self.customExportActions = []
        for i in sorted(self.settings['Export Settings'].keys()):
            if 'Deleted' in self.settings['Export Settings'][i]:
                continue
            self.customExportActions.append(QAction(i, self))
            self.connect(self.customExportActions[-1], SIGNAL('triggered(bool)'), self.onExportCustom)
        self.menuButtonExport.addActions(self.customExportActions)
        self.ui.toolButtonExport.setMenu(self.menuButtonExport)

    def onDeleteRow(self):
        """
        Delete row in the table
        """
        selection = self.ui.tableView.selectionModel()
        indexes = selection.selectedRows()
        # Sort indexes in back order because the model is changed after the first
        # item is deleted. So to keep relevant indexes of the selected rows it is
        # needed to delete rows starting from the last selected row in the table
        indexes.sort(reverse=True)

        for i in indexes:
            self.proxyModel.removeRows(i.row(), 1, QModelIndex())

        # Set up row indicator text
        self.ui.rowIndicator.setText('Rows: %s/%s' % (self.proxyModel.rowCount(),
                                                      self.tableModel.rowCount(None)))

    def onResizeRowsToContents(self):
        self.ui.tableView.resizeRowsToContents()

    def onResizeRows(self):
        height = QInputDialog.getInteger(self, 'Rows height', 'Input a new rows height (min = 20 pts)', value=30,
                                         min=20, max=1000)
        if height[1]:
            for i in range(self.proxyModel.rowCount()):
                self.ui.tableView.setRowHeight(i, height[0])

    def onLayoutChanged(self):
        self.ui.tableView.scrollTo(self.ui.tableView.currentIndex())

    def onImport(self):
        """
        Slot for importAction and appendAction signals
        """

        # Look for user defined default import action and use it to import data
        for i in self.settings['Import Settings']:
            # try-except to ensure compatibility with old settings files (no Default key)
            try:
                if self.settings['Import Settings'][unicode(i)]['Default'] == 'True':
                    sender = self.sender()
                    if sender == self.ui.actionImport:
                        for a in self.customImportActions:
                            #print a.text()
                            if a.text() == unicode(i):
                                a.emit(SIGNAL('triggered(bool)'), True)
                                return
                    if sender == self.ui.actionAppend:
                        for a in self.customAppendActions:
                            if a.text() == unicode(i):
                                a.emit(SIGNAL('triggered(bool)'), True)
                                return
            except:
                print 'No Default key in %s' % unicode(i)

        # No default found, show error box instead
        no_pattern = QMessageBox()
        no_pattern.critical(self, u'Import Pattern',
                            u'Default import pattern not defined.\nPlease configure one under Settings.')

    def onImportCustom(self):
        """
        Slot for custom import actions triggered signals
        """
        try:
            # Get Import Pattern
            sender = self.sender()
            logger.debug(str(sender.parent()))
            if sender.parent() == self.menuButtonImport:
                actions = self.customImportActions
                append = False
            elif sender.parent() == self.menuButtonAppend:
                actions = self.customAppendActions
                append = True

            for i in actions:
                if sender == i:
                    pattern_name = unicode(i.text())
                    pattern_settings = self.settings.getImportSettings(pattern_name)
                    break

            default_encoding = True

            # Load Clippings from File
            file_name = QFileDialog.getOpenFileName(self, '', '',
                                                    ';;'.join(['%s (*.%s)' % (pattern_name, ext) for
                                                               ext in pattern_settings['Extension'].split(',')]))[0]
            if file_name == '':
                # This happens when we cancel the file dialog so no need to throw an error
                return
            else:
                file_name = unicode(file_name)

            try:
                logger.info("Trying to decode using %s" % pattern_settings['Encoding'])
                my_clippings = co.open(file_name, 'r', pattern_settings['Encoding'].split(' ')[0]).read()
            except Exception as e:
                try:
                    logger.info("Trying to decode using %s" % DEFAULT_ENCODING[1])
                    my_clippings = co.open(file_name, 'r', DEFAULT_ENCODING[1]).read()
                    default_encoding = False
                except UnicodeError:
                    logger.info("Trying to decode using %s" % 'Windows-1252')
                    my_clippings = co.open(file_name, 'r', 'Windows-1252').read()
                    default_encoding = False
                except Exception as error:
                    logger.exception("Clippings File load resulted in exception\n%s" % error.message)
                    bad_encoding = QMessageBox()
                    informational_text = u'We were unable to import your file using either (1) the encoding ' \
                                         u'selected on the import pattern or (2) several default encodings.  ' \
                                         u'Please configure a different encoding for your Import Pattern.  This ' \
                                         u'can be changed by going to Settings, choosing the Import tab, selecting ' \
                                         u'the import pattern you use from the main drop-down, and selecting a ' \
                                         u'different encoding from the Encoding drop-down in the lower right. Many ' \
                                         u'patterns will work, but will garble or remove characters like quote ' \
                                         u'and apostrophe.  Please review the results of the import to ensure ' \
                                         u'that you have selected the correct encoding.  Make sure you click OK ' \
                                         u'or Accept to lock in the new selection.'
                    bad_encoding.critical(bad_encoding, u'Import Encoding', informational_text)
                    raise e

            summary, detail = self.tableModel.parse(my_clippings, pattern_settings, append)
            summary = "<%s> Loading clippings from file %s\r\n\r\n%s" % (
                QTime.currentTime().toString('hh:mm:ss'),
                QDir.dirName(QDir(file_name)),
                summary
            )

            if not default_encoding:
                summary += u'\r\n\r\nNOTE:  The encoding selected for your import pattern did not work.  However, we were ' \
                           u'able to import using one of our default patterns.  Please review your data and make sure ' \
                           u'it has imported properly.  If it has not, please select a different import pattern on the ' \
                           u'Import Tab of Settings.'
            summary += u'\r\n\r\nFor more details, click the "Show Details" button' + u' ' * 50
            import_complete = QMessageBox(QMessageBox.Information, u'Import Complete', summary)
            import_complete.addButton(QMessageBox.Ok)
            import_complete.setEscapeButton(QMessageBox.Ok)  # does not work
            import_complete.setDetailedText(detail)
            import_complete.exec_()

            logger.debug(summary)
            self.ui.statusBar.showMessage(summary, 3000)

            # Set up row indicator text
            self.ui.rowIndicator.setText('Rows: %s/%s' % (self.proxyModel.rowCount(),
                                                          self.tableModel.rowCount(None)))
        except Exception as error:
            logger.exception("Exception: %s" % error.message)
            import_error = QMessageBox()
            import_error.warning(self, u'Import Error', u'Error during import.\r\n\r\n' + error.message)

    def onExport(self):
        """
        Slot for exportAction signal
        """

        # Look for user defined default export action and use it to export data
        for i in self.settings['Export Settings']:
            # try-except to ensure compatibility with old settings files (no Default key)
            try:
                if self.settings['Export Settings'][unicode(i)]['Default'] == 'True':
                    for a in self.customExportActions:
                        #print a.text()
                        if a.text() == unicode(i):
                            a.emit(SIGNAL('triggered(bool)'), True)
                            return
            except:
                print 'No Default key in %s' % unicode(i)

        # No default found, show error box instead
        no_pattern = QMessageBox()
        no_pattern.critical(self, u'Export Pattern',
                            u'Default export pattern not defined.\nPlease configure one under Settings.')

    def onExportCustom(self):
        """
        Slot for custom export actions triggered signals
        """
        try:
            sender = self.sender()
            for i in self.customExportActions:
                if sender == i:
                    name = unicode(i.text())
                    header = self.settings['Export Settings'][name]['Header']
                    body = self.settings['Export Settings'][name]['Body']
                    bottom = self.settings['Export Settings'][name]['Bottom']
                    dateFormat = self.settings['Export Settings'][name]['Date Format']
                    if dateFormat == '':
                        dateFormat = 'dd.MM.yy, hh:mm'
                    encoding = self.settings['Export Settings'][name]['Encoding'].split(' ')[0]
                    if encoding == '':
                        encoding = DEFAULT_ENCODING[0]  # UTF-8
                    extension = self.settings['Export Settings'][name]['Extension'].split(',')
                    if extension[0] == '':
                        extension = DEFAULT_EXTENSION
                    break
            fileName = QFileDialog.getSaveFileName(self, '', '',
                                                   ';;'.join(['%s (*.%s)' % (name, ext) for ext in extension]))
            if fileName == '':
                return

            wildCards = re.findall(r'\?P<(.*?)>', body, re.UNICODE)

            fileOut = co.open(unicode(fileName), 'w', encoding, 'replace')
            fileOut.write(header)

            for row in range(self.proxyModel.rowCount()):
                bodyLine = body
                for i in wildCards:
                    bodyLine = bodyLine.replace(u'?P<%s>' % i, self.processWildcard(name, i, row, dateFormat))
                fileOut.write(bodyLine)

            fileOut.write(bottom)
            fileOut.close()

            status = '<%s> Data has been exported to "%s"' % (QTime.currentTime().toString('hh:mm:ss'),
                                                              QDir.dirName(QDir(fileName)))

            # Pop Export Status Box
            export_complete = QMessageBox(QMessageBox.Information, u'Export Complete', u'Export Complete' + u' ' * 100)
            export_complete.setInformativeText(u'Data has been exported to "%s"' % QDir.dirName(QDir(fileName)))
            export_complete.exec_()

            print status
            self.ui.statusBar.showMessage(status, 3000)

        except Exception as error:
            export_error = QMessageBox()
            export_error.warning(self, u'Export Error', u'Error during export.\r\n\r\n' + error.message)

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
                return re.sub("<", "&lt;", re.sub(">", "&gt;", re.sub("&", "&amp;",
                                                                      self.processWildcard(template_name, wildcard[7:],
                                                                                           row, dateFormat))))
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
                return unicode(self.proxyModel.data(self.proxyModel.index(row, HEADERS.index(wildcard)),
                                                    Qt.EditRole).toPython().toString(dateFormat))
            else:
                return unicode(self.proxyModel.data(self.proxyModel.index(row, HEADERS.index(wildcard)),
                                                    Qt.DisplayRole).toString())
        except:
            return u''

    def onImportCsv(self):
        try:
            # Get Import Pattern
            sender = self.sender()
            logger.debug(str(sender.parent()))
            if sender.parent() == self.menuButtonImport:
                append = False
            elif sender.parent() == self.menuButtonAppend:
                append = True

            file_name = QFileDialog.getOpenFileName(self, '', '',
                                                    ';;'.join(['Comma Separated Value (*.csv)']))[0]
            if file_name == '':
                # This happens when we cancel the file dialog so no need to throw an error
                return
            else:
                file_name = unicode(file_name)

            try:
                csv_file = open(file_name, 'rb')
                csv_reader = csv.reader(csv_file)
            except Exception as e:
                logger.exception("Could not load CSV file for import\n%s" % e.message)
                bad_encoding = QMessageBox()
                informational_text = u'We were unable to import your file.'
                bad_encoding.critical(bad_encoding, u'Import Encoding', informational_text)
                raise e

            summary, detail = self.tableModel.from_csv(csv_reader, append=append)
            summary = "<%s> Loading clippings from file %s\r\n\r\n%s" % (
                QTime.currentTime().toString('hh:mm:ss'),
                QDir.dirName(QDir(file_name)),
                summary
            )
            import_complete = QMessageBox(QMessageBox.Information, u'CSV Import Complete', summary)
            import_complete.addButton(QMessageBox.Ok)
            import_complete.setEscapeButton(QMessageBox.Ok)  # does not work
            import_complete.setDetailedText(detail)
            import_complete.exec_()

        except Exception as error:
            logger.exception("Exception: %s" % error.message)
            import_error = QMessageBox()
            import_error.warning(self, u'Import Error', u'Error during import.\r\n\r\n' + error.message)

    def onExportCsv(self):
        filename = QFileDialog.getSaveFileName(self, '', '',
                                               ';;'.join(['Comma Separated Values (*.CSV)']))
        if filename == '':
            # This happens if we cancel the dialog so we don't want to raise an error
            return

        f = open(filename, 'wb')
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(self.tableModel.table_data.headers)

        # This outputs only the rows visible on the screen
        for row in range(self.proxyModel.rowCount()):
            writer.writerow([
                unicode(self.proxyModel.data(self.proxyModel.index(row, i), Qt.DisplayRole).toString())
                for i in range(len(self.tableModel.table_data.headers))
            ])

        f.close()

    def onFilter(self):
        """
        Slot for filterAction signal
        """
        self.ui.filterCloseButton.setVisible(not self.ui.filterCloseButton.isVisible())
        self.ui.filterOptionButton.setVisible(not self.ui.filterOptionButton.isVisible())
        self.ui.filterEdit.setVisible(not self.ui.filterEdit.isVisible())
        self.ui.filterCaseBox.setVisible(not self.ui.filterCaseBox.isVisible())
        self.ui.filterLine.setVisible(not self.ui.filterLine.isVisible())

        self.ui.filterEdit.setFocus()
        # Move the lines somewhere:


        # Clear filter
        if self.sender() == self.ui.filterCloseButton: self.ui.filterEdit.clear()

    def onFilterInput(self, filterText):
        """
        Slot for filterInput textChanged(QString) signal
        """
        self.proxyModel.setFilterWildcard(filterText)

        # Set up row indicator text
        self.ui.rowIndicator.setText('Rows: %s/%s' % (self.proxyModel.rowCount(), self.tableModel.rowCount(None)))
        if self.proxyModel.rowCount() == 0 and self.tableModel.rowCount(None) != 0:
            self.ui.filterEdit.setStyleSheet('background-color: qlineargradient(spread:pad, ' + \
                                             'x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 88, 88, 255), ' + \
                                             'stop:1 rgba(255, 255, 255, 255));;')
        else:
            self.ui.filterEdit.setStyleSheet("background-color: rgb(255, 255, 255);")

    def onFilterCaseState(self, state):
        self.proxyModel.setFilterCaseSensitivity(bool(state))
        self.onFilterInput(self.ui.filterEdit.text())

    def onFilterOptionTriggered(self, state):
        sender = self.sender()
        for h in self.tableModel.table_data.headers:
            if sender != self.actionFilterHeaders[h]:
                self.actionFilterHeaders[h].setEnabled(True)
                self.actionFilterHeaders[h].setChecked(False)
        if sender != self.actionFilterAll:
            self.actionFilterAll.setEnabled(True)
            self.actionFilterAll.setChecked(False)

            self.ui.filterOptionButton.setChecked(True)
            self.proxyModel.setFilterKeyColumn(self.tableModel.table_data.headers.index(sender.text()))
        else:
            self.ui.filterOptionButton.setChecked(False)
            self.proxyModel.setFilterKeyColumn(-1)
        sender.setEnabled(False)
        self.onFilterInput(self.ui.filterEdit.text())

    def onAbout(self):
        about = QMessageBox(self)
        about.setTextFormat(Qt.RichText)
        about.setStandardButtons(QMessageBox.Ok | QMessageBox.Save)

        about.setWindowTitle(u'About...')
        about.setWindowIcon(QIcon(u':/icons/Bloomy/infoabout.png'))
        about.setText(u'<b>DaleyKlippings (ver. %s) — Kindle clippings viewer</b>' % __ver__)
        about.setInformativeText(u'DaleyKlippings (<a href="https://daleyklippings.claytondaley.com">' +
                                 u'homepage</a>) is a programm to view, edit and export ' +
                                 u'Kindle highlights, notes, and bookmarks, ' +
                                 u'stored in \'My Clippings.txt\' file.<br>' +
                                 u'<a href="https://daleyklippings.claytondaley.com/">' +
                                 u'Author</a>: Clayton Daley, <i>daleyklippings@claytondaley.com</i><br><br>' +
                                 u'Derived from: Klippings v0.1.5<br>' +
                                 u'Author: thearr, <i>hmi@ya.ru</i><br>' +
                                 u'under open source license.<br><br>' +
                                 u'<a href="http://miloszwl.deviantart.com/">' +
                                 u'Icons</a>: Milosz Wlazlo, <i>miloszwl@miloszwl.com</i><br>')

        about.setDetailedText(log.getvalue())
        button = about.exec_()

        if button == QMessageBox.Save:
            try:
                logFile = co.open('log.txt', 'w', 'utf-16', 'replace')
                print u'<%s> The log is saved' % (QTime.currentTime().toString('hh:mm:ss'))
                logFile.write(log.getvalue())
                logFile.close()
            except:
                QMessageBox.critical(self, u'Error', u'Can\'t save the file')
                print u'<%s> Unsuccessful attempt to save the log' % (QTime.currentTime().toString('hh:mm:ss'))

    def onHelp(self):
        import webbrowser

        webbrowser.open_new_tab('https://daleyclippings.claytondaley.com/klippings/')

    def onSettings(self):
        settingsDialog = SettingsDialog(self)
        self.connect(settingsDialog, SIGNAL('settingsChanged(QString)'), self.onSettingsChanged)
        settingsDialog.show()

    def onSettingsChanged(self, settingsJson):
        logging.debug("onSettingsChanged called")
        try:
            logging.debug("Updating settings to %s" % str(settingsJson))
            self.settings = Settings.from_json(settingsJson)
        except Exception as e:
            logger.exception("Settings.from_json resulted in exception:\n%s" % e.message)
        logging.debug("... new Setting set")
        self.initiateToolButtons()
        self.updateDelegates()

if __name__ == '__main__':
    import StringIO
    import sys

#    log = StringIO.StringIO()
#    sys.stdout = log
#    sys.stderr = log
    print u'# Log started on %s\n# %s' % (QDateTime.currentDateTime().toString('dd.MM.yy, hh:mm:ss'), '=' * 30)

    app = QApplication(sys.argv)
    mainWin = MainWin()
    try:
        logger.info("Showing main window")
        mainWin.show()
        mainWin.raise_()
        logger.info("Main window show completed")
    except Exception as e:
        logger.exception("Exception in window.show():\n%s" % e.message)
    # Bring window to the front to cure PyInstaller bug under Mac OS X
    if osname == 'posix':
        mainWin.raise_()
    sys.exit(app.exec_())
