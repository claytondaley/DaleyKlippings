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

"""
Main DaleyKlippings window
"""
__ver__ = '1.3.4'

import logging
logging.basicConfig(level=logging.INFO)
# handler = logging.StreamHandler()
logger = logging.getLogger("daley_klippings")
# logger.addHandler(handler)
logger.info("Loading DaleyKlippings")

import os
import codecs
from pprint import pformat
import unicodecsv as csv
from functools import partial
from PySide.QtCore import Qt, SIGNAL, QLocale, QTime, QDir, QDateTime, QModelIndex, Signal, SLOT
from PySide.QtGui import QMainWindow, QSortFilterProxyModel, QMenu, QAction, QInputDialog, QFileDialog, QMessageBox, \
    QApplication, QIcon
from delegators import ComboBoxDelegate, LocationEditDelegate, DateEditDelegate
from settings import JsonFileStore, Settings, SettingsDialog, HEADERS
from table import TableModel, RegexExport, RegexImport, LegacyNotesHandler, CsvParser
from gui.ui_mainWin import Ui_mainWin


class MainWin(QMainWindow):
    """
    Main DaleyKlippings window class
    """
    importDefault = None
    appendDefault = None
    exportDefault = None

    def __init__(self, settings_store, columns, parent=None):
        QMainWindow.__init__(self, parent)
        self.settings_store = settings_store
        self.columns = columns

        # Initiate GUI
        self.ui = Ui_mainWin()
        self.ui.setupUi(self)
        self.ui.statusBar.addPermanentWidget(self.ui.rowIndicator)
        self.ui.tableView.horizontalHeader().setSortIndicator(-1, Qt.DescendingOrder)

        # Initiate settings
        try:
            self.settings_store.load()
            self.settings = settings_store.get()
        except (OSError, IOError):
            msg = 'Custom settings file "settings.txt"\nwas not found. We will create this file\n' \
                  'for you and start DaleyKlippings with the default settings.'
            QMessageBox.warning(None, 'File not found', msg)
            self.settings_store.save()
            # Create settings file to prevent the error from recurring
        """
        except:
            msg = 'Settings file "settings.txt" is in the\nwrong format and could not be loaded.\n' \
                  'The file is probably corrupted. Please\nrestore an old version of this file from\n' \
                  'backups or delete the file to use\ndefault settings'
            QMessageBox.warning(None, 'Settings File', msg)
            self.close()
        """

        logging.debug("Settings:\n%s" % pformat(self.settings))

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
        self.tableModel = TableModel(self.columns)
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
        for h in self.tableModel.headers:
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
        typeDelegate = ComboBoxDelegate(language=self.settings['Language'], parent=self)
        locationDelegate = LocationEditDelegate(self)
        # Try to localize the dates
        date_language = self.settings['Language']['Date Language']
        if date_language == "English (default)":
            # This is our default value, and needs to be translated into a valid language in QLocale
            date_language = "English"
        logger.info("Date Language is %s" % date_language)
        local_language = QLocale(getattr(QLocale, date_language))
        date_format = local_language.dateFormat(format=QLocale.ShortFormat)
        time_format = local_language.timeFormat()
        # Remove time zone if included
        if time_format[-1:] == "t":
            time_format = time_format[:-1]
        self.date_format = "%s %s" % (date_format, time_format)
        logger.info("Localizing date formats to %s" % self.date_format)
        dateDelegate = DateEditDelegate(self, format=self.date_format)

        self.ui.tableView.setItemDelegateForColumn(2, typeDelegate)
        self.ui.tableView.setItemDelegateForColumn(3, locationDelegate)
        self.ui.tableView.setItemDelegateForColumn(4, locationDelegate)
        self.ui.tableView.setItemDelegateForColumn(5, dateDelegate)

    def initiateToolButtons(self):
        """
        This function is called to create the toolbar and anytime settings change (to update the list of patterns
        in the dropdown.
        """
        # Clear old signals (if they exist)
        if self.importDefault is not None:
            self.ui.actionImport.triggered.disconnect(self.importDefault)
            self.ui.actionAppend.triggered.disconnect(self.appendDefault)
            self.ui.actionExport.triggered.disconnect(self.exportDefault)
            self.ui.toolButtonImport.triggered.disconnect(self.importDefault)
            self.ui.toolButtonAppend.triggered.disconnect(self.appendDefault)
            self.ui.toolButtonExport.triggered.disconnect(self.exportDefault)

        # Import (and Append) Buttons
        self.menuButtonImport = QMenu()
        self.menuButtonImport.addAction(self.ui.actionImport)
        self.menuButtonAppend = QMenu()
        self.menuButtonAppend.addAction(self.ui.actionAppend)
        self.menuButtonExport = QMenu()
        self.menuButtonExport.addAction(self.ui.actionExport)

        # Special (built-in) CSV Option
        csv_action = QAction("CSV", self.menuButtonImport)
        self.menuButtonImport.addAction(csv_action)
        csv_action.triggered.connect(self.onImportCsv)
        csv_action = QAction("CSV", self.menuButtonAppend)
        self.menuButtonAppend.addAction(csv_action)
        csv_action.triggered.connect(partial(self.onImportCsv, append=True))
        csv_action = QAction("CSV", self.menuButtonExport)
        self.menuButtonExport.addAction(csv_action)
        csv_action.triggered.connect(self.onExportCsv)

        # Separators
        self.menuButtonImport.addSeparator()
        self.menuButtonAppend.addSeparator()
        self.menuButtonExport.addSeparator()

        # Add Import Patterns from Settings
        logger.debug('Processing Import Settings: \n%s' % pformat(self.settings['Import Settings']))
        for k in sorted(self.settings['Import Settings']):
            # Don't display "deleted" items (which must remain the settings file to override the defaults file)
            if 'Deleted' in self.settings['Import Settings'][k]:
                continue
            # Import Action
            v = self.settings['Import Settings'][k]
            import_action = QAction(k, self.menuButtonImport)
            import_action.triggered.connect(partial(self.onImport, name=k, importPattern=v))
            self.menuButtonImport.addAction(import_action)

            # Append Action
            append_action = QAction(k, self.menuButtonAppend)
            append_action.triggered.connect(partial(self.onImport, name=k, importPattern=v, append=True))
            self.menuButtonAppend.addAction(append_action)

            logger.debug("Added dropdown items (import and append) for %s" % k)

            if 'Default' in v and v['Default'] == 'True':
                logging.debug("Adding %s pattern as default to Import and Append buttons" % k)
                self.importDefault = partial(self.onImport, name=k, importPattern=v)
                self.ui.actionImport.triggered.connect(self.importDefault)
                self.ui.toolButtonImport.triggered.connect(self.importDefault)
                self.appendDefault = partial(self.onImport, name=k, importPattern=v, append=True)
                self.ui.actionAppend.triggered.connect(self.appendDefault)
                self.ui.toolButtonAppend.triggered.connect(self.appendDefault)


        # Add Export Patterns from Settings
        for k in sorted(self.settings['Export Settings']):
            if 'Deleted' in self.settings['Export Settings'][k]:
                continue
            # Export Action
            v = self.settings['Export Settings'][k]
            action = QAction(k, self.menuButtonExport)
            action.triggered.connect(partial(self.onExport, name=k, exportPattern=v))
            self.menuButtonExport.addAction(action)

            if 'Default' in v and v['Default'] == 'True':
                self.exportDefault = partial(self.onExport, name=k, exportPattern=v)
                self.ui.actionExport.triggered.connect(self.exportDefault)
                self.ui.toolButtonExport.triggered.connect(self.exportDefault)

        # Add menus to UI
        self.ui.toolButtonImport.setMenu(self.menuButtonImport)
        self.ui.toolButtonAppend.setMenu(self.menuButtonAppend)
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

    def onImport(self, name, importPattern, append=False, co=None):
        """
        Slot for custom import actions triggered signals
        """
        logging.debug("Importing using importPattern:\n\n%s" % pformat(importPattern))
        summary = []
        detail = []

        try:
            name = unicode(name)
            # Default extension to all files
            extensions = [x for x in importPattern['Extension'].split(',') if x != '']
            if len(extensions) == 0:
                extensions = ['*']
            default_encoding = True

            # Load Clippings from File
            file_name = QFileDialog.getOpenFileName(self, '', '', ';;'.join(['%s (*.%s)' % (name, ext) for
                                                                             ext in extensions]))[0]
            if file_name == '':
                # This happens when we cancel the file dialog so no need to throw an error
                return
            else:
                file_name = unicode(file_name)

            message = 'Loading clippings from file %s' % QDir.dirName(QDir(file_name))
            detail.append(message)
            logger.debug("<%s> %s" % (QTime.currentTime().toString('hh:mm:ss'), message))

            try:
                logger.info("Trying to decode using %s" % importPattern['Encoding'])
                my_clippings = codecs.open(file_name, 'r', importPattern['Encoding'].split(' ')[0]).read()
            except Exception as e:
                try:
                    logger.info("Trying to decode using %s" % 'utf-16')
                    my_clippings = codecs.open(file_name, 'r', 'utf-16').read()
                    default_encoding = False
                except UnicodeError:
                    logger.info("Trying to decode using %s" % 'Windows-1252')
                    my_clippings = codecs.open(file_name, 'r', 'Windows-1252').read()
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

            parser = RegexImport(self.columns, self.settings['Language'], importPattern)
            try:
                parser.parse(my_clippings)
            except Exception as error:
                bad_encoding = QMessageBox()
                informational_text = u'The Import Pattern is invalid.\r\n\r\n' + \
                                     'Import Pattern resulted in the error:\n%s' % str(error.message)
                bad_encoding.critical(bad_encoding, u'Import Encoding', informational_text)

            candidates = len(parser.candidates)
            parsed = len(parser.parsed)
            data = parser.parsed

            message = u'%d out of %d clippings were successfully processed.' % (parsed, candidates)
            summary.append('')
            summary.append(message)
            detail.append('')
            detail.append(message)
            logger.debug("<%s> %s" % (QTime.currentTime().toString('hh:mm:ss'), message))

            if parsed == 0 and candidates > 0:
                message = u'Please verify that you selected the right file or try a different Import Pattern.' + u' ' * 50 + \
                          u'\r\n\r\nIf none of the built-in patterns work, please contact daleyklippings@claytondaley.com.' + u' ' * 50
                summary.append('')
                summary.append(message)
                logger.debug("<%s> %s" % (QTime.currentTime().toString('hh:mm:ss'), message))

            if self.settings['Notes']['Attach'] == 'True':
                matcher = LegacyNotesHandler(self.settings['Notes'], self.settings['Language'])
                matcher.match(parser.parsed)
                matched = len(parser.parsed) - len(matcher.matched)

                message = u' - We were able to match %d Note%s with a Highlight %s' % \
                          (matched, ('s' if matcher.matched > 1 else ''), u' ' * 50)
                summary.append(message)
                detail.append(message)
                logger.debug("<%s> %s" % (QTime.currentTime().toString('hh:mm:ss'), message))

                if matcher.matched > 0:
                    message = u' - As a result, fewer lines will show up in the interface.' + u' ' * 50
                    summary.append(message)

                data = matcher.matched

            if not default_encoding:
                message = u'NOTE:  The encoding selected for your import pattern did not work.  However, we were ' + \
                          u'able to import using one of our default patterns.  Please review your data and make sure ' + \
                          u'it has imported properly.  If it has not, please select a different import pattern on the ' + \
                          u'Import Tab of Settings.'
                summary.append(message)
                detail.append(message)
                logger.debug("<%s> %s" % (QTime.currentTime().toString('hh:mm:ss'), message))
            message = u'For more details, click the "Show Details" button'
            summary.append('')
            summary.append(message)
            import_complete = QMessageBox(QMessageBox.Information, u'Import Complete', (u' ' * 50 + '\r\n').join(summary))
            import_complete.addButton(QMessageBox.Ok)
            import_complete.setEscapeButton(QMessageBox.Ok)  # does not work
            import_complete.setDetailedText('\r\n'.join(detail))
            import_complete.exec_()

            self.ui.statusBar.showMessage(u''.join(summary), 3000)
        except Exception as error:
            logger.exception("Exception: %s" % error.message)
            import_error = QMessageBox()
            import_error.warning(self, u'Import Error', u'Error during import.\r\n\r\n' + error.message)
        else:
            # Set up row indicator text
            # TODO: Figure out why this isn't working
            self.ui.rowIndicator.setText('Rows: %d/%d' % (self.proxyModel.rowCount(),
                                                          self.tableModel.rowCount(None)))

            message = "Setting Table Data"
            logger.debug("<%s> %s" % (QTime.currentTime().toString('hh:mm:ss'), message))
            if append:
                self.tableModel.appendTableData(data)
            else:
                self.tableModel.setTableData(data)

    def onExport(self, name, exportPattern, co=None):
        """
        Slot for custom export actions triggered signals
        """
        try:
            name = unicode(name)
            extensions = [x for x in exportPattern['Extension'].split(',') if x != '']

            fileName = QFileDialog.getSaveFileName(
                self, '', '', ';;'.join(['%s (*.%s)' % (name, ext) for ext in extensions]))[0]
            if fileName == '':
                return

            logger.info("Exporting to file %s" % fileName)
            fileOut = codecs.open(unicode(fileName), 'w', exportPattern['Encoding'].split(' ')[0], 'replace')
            parser = RegexExport(exportPattern)
            if parser.export_(self.proxyModel):
                output = '\r\n'.join(parser.rows)
                logger.debug("... writing file:\r\n%s" % output)
                fileOut.write(output)
                status = '<%s> Data has been exported to "%s"' % (QTime.currentTime().toString('hh:mm:ss'),
                                                                  QDir.dirName(QDir(fileName)))
                logger.info(status)
                fileOut.close()

                # Pop Export Status Box
                export_complete = QMessageBox(QMessageBox.Information, u'Export Complete', u'Export Complete' + u' ' * 100)
                export_complete.setInformativeText(u'Data has been exported to "%s"' % QDir.dirName(QDir(fileName)))
                export_complete.exec_()

                self.ui.statusBar.showMessage(status, 3000)

        except Exception as error:
            export_error = QMessageBox()
            export_error.warning(self, u'Export Error', u'Error during export.\r\n\r\n' + error.message)

    def onImportCsv(self, append=False):
        try:
            # Get Import Pattern
            file_name = QFileDialog.getOpenFileName(self, '', '',
                                                    ';;'.join(['Comma Separated Value (*.csv)']))[0]
            if file_name == '':
                # This happens when we cancel the file dialog so no need to throw an error
                return

            try:
                file_name = unicode(file_name)
                csv_file = open(file_name, 'rb')
                csv_reader = csv.reader(csv_file)
            except Exception as e:
                logger.exception("Could not load CSV file for import\n%s" % e.message)
                bad_encoding = QMessageBox()
                informational_text = u'We were unable to import your file.'
                bad_encoding.critical(bad_encoding, u'Import Encoding', informational_text)
                raise e

            # TODO: Fix csv import logic
            parser = CsvParser()
            parser.import_(csv_reader=csv_reader)

            summary = "<%s> Loading clippings from file %s" % (
                QTime.currentTime().toString('hh:mm:ss'),
                QDir.dirName(QDir(file_name))
            )
            import_complete = QMessageBox(QMessageBox.Information, u'CSV Import Complete', summary)
            import_complete.addButton(QMessageBox.Ok)
            import_complete.setEscapeButton(QMessageBox.Ok)  # does not work
            import_complete.setDetailedText('\r\n'.join(parser.detail))
            import_complete.exec_()

        except Exception as error:
            logger.exception("Exception: %s" % error.message)
            import_error = QMessageBox()
            import_error.warning(self, u'Import Error', u'Error during import.\r\n\r\n' + error.message)

    def onExportCsv(self):
        filename = QFileDialog.getSaveFileName(self, '', '',
                                               ';;'.join(['Comma Separated Values (*.CSV)']))[0]
        if filename == '':
            # This happens if we cancel the dialog so we don't want to raise an error
            return

        f = open(filename, 'wb')
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        # Write header row
        writer.writerow(self.tableModel.headers)

        # This outputs only the rows visible on the screen
        for row in range(self.proxyModel.rowCount()):
            row_data = []
            for i in range(len(self.tableModel.headers)):
                item = self.proxyModel.data(self.proxyModel.index(row, i), Qt.DisplayRole)
                if item and self.tableModel.headers[i] == 'Date':
                    if u'%' in self.date_format:
                        # The % sign indicates that the pattern is a basic Python format
                        item = item.strftime(self.date_format).strip()
                    else:
                        # Otherwise, we assume a Qt Format
                        item = QDateTime(item).toString(self.date_format).strip()
                row_data.append(item)
            writer.writerow(row_data)

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
        if self.sender() == self.ui.filterCloseButton:
            self.ui.filterEdit.clear()

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
        for h in self.tableModel.headers:
            if sender != self.actionFilterHeaders[h]:
                self.actionFilterHeaders[h].setEnabled(True)
                self.actionFilterHeaders[h].setChecked(False)
        if sender != self.actionFilterAll:
            self.actionFilterAll.setEnabled(True)
            self.actionFilterAll.setChecked(False)

            self.ui.filterOptionButton.setChecked(True)
            self.proxyModel.setFilterKeyColumn(self.tableModel.headers.index(sender.text()))
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
        about.setInformativeText(u'DaleyKlippings (<a href="http://daleyklippings.claytondaley.com">' +
                                 u'homepage</a>) is a programm to view, edit and export ' +
                                 u'Kindle highlights, notes, and bookmarks, ' +
                                 u'stored in \'My Clippings.txt\' file.<br>' +
                                 u'<a href="http://daleyklippings.claytondaley.com/">' +
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
                logFile = codecs.open('log.txt', 'w', 'utf-16', 'replace')
                logger.info(u'<%s> The log is saved' % (QTime.currentTime().toString('hh:mm:ss')))
                logFile.write(log.getvalue())
                logFile.close()
            except:
                QMessageBox.critical(self, u'Error', u'Can\'t save the file')
                logger.info(u'<%s> Unsuccessful attempt to save the log' % (QTime.currentTime().toString('hh:mm:ss')))

    def onHelp(self):
        import webbrowser

        webbrowser.open_new_tab('http://daleyclippings.claytondaley.com/')

    def onSettings(self):
        settingsDialog = SettingsDialog(self.settings, self)
        # The signal is defined to carry a QString and has limited flexibility
        settingsDialog.settingsChanged.connect(self.onSettingsChanged)
        settingsDialog.show()

    def onSettingsChanged(self, settings):
        logging.info("onSettingsChanged called")
        logging.debug("... with settings %s" % pformat(settings))
        try:
            self.settings = settings
            self.settings_store.save(settings)
        except Exception as e:
            logger.exception("Settings save() resulted in exception:\n%s" % e.message)
        logging.debug("... new Setting set")
        self.initiateToolButtons()
        self.updateDelegates()

if __name__ == '__main__':
    import StringIO
    import sys

    log = StringIO.StringIO()

    logger.info(u'# %s\n# Log started on %s\n# %s' %
                ('=' * 33, QDateTime.currentDateTime().toString('dd.MM.yy, hh:mm:ss'), '=' * 33))

    app = QApplication(sys.argv)
    settingsStore = JsonFileStore(None)
    # Inject source of settings
    mainWin = MainWin(columns=HEADERS, settings_store=settingsStore)

    try:
        mainWin.show()
        # Bring window to the front to cure PyInstaller bug under Mac OS X
        if os.name == 'posix':
            mainWin.raise_()
    except Exception as e:
        logger.exception("Exception in window.show() or mainWin.raise_():\n%s" % e.message)

    sys.exit(app.exec_())
