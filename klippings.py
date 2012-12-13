#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main Klippings window
"""

__ver__ = '0.1.5'
## Features: 
## - default import & export patterns
## - language settings for highlight, note & bookmark terms

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import codecs as co

from gui.ui_mainWin import *
from table import *
from settings import *

class MainWin(QMainWindow):
    """
    Main Klippings window class
    """
    def __init__(self, parent = None):
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
        
        self.proxyModel.setFilterCaseSensitivity(False)
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
        for h in self.tableModel.tableData.headers:
            self.actionFilterHeaders[h] = QAction(h, self)
            self.actionFilterHeaders[h].setCheckable(True)
            self.menuFilterOption.addAction(self.actionFilterHeaders[h])
            self.connect(self.actionFilterHeaders[h], SIGNAL('triggered(bool)'), self.onFilterOptionTriggered)
        self.ui.filterOptionButton.setMenu(self.menuFilterOption)            
        
        # Initiate delegates
        typeDelegate = ComboBoxDeligate(self)
        locationDelegate = LocationEditDelegate(self)
        dateDelegate = DateEditDelegate(self)
        self.ui.tableView.setItemDelegateForColumn(1, typeDelegate)
        self.ui.tableView.setItemDelegateForColumn(2, locationDelegate)
        self.ui.tableView.setItemDelegateForColumn(5, dateDelegate)
        
        # Scroll table to the current cell after sorting
        self.connect(self.proxyModel, SIGNAL('layoutChanged()'), self.onLayoutChanged)
        
    def initiateToolButtons(self):
        # Import Button
        self.menuButtonImport = QMenu()
        self.menuButtonImport.addAction(self.ui.actionImport)
        self.menuButtonImport.addSeparator()
        self.customImportActions = []
        for i in self.settings['Import Settings'].keys():
            self.customImportActions.append(QAction(i, self.menuButtonImport))
            #print self.customImportActions[-1].text()
            self.connect(self.customImportActions[-1], SIGNAL('triggered(bool)'), self.onImportCustom)
        self.menuButtonImport.addActions(self.customImportActions)
        self.ui.toolButtonImport.setMenu(self.menuButtonImport)

        # Append Button
        self.menuButtonAppend = QMenu()
        self.menuButtonAppend.addAction(self.ui.actionAppend)
        self.menuButtonAppend.addSeparator()
        self.customAppendActions = []
        for i in self.settings['Import Settings'].keys():
            #print '%s (append)' % i
            self.customAppendActions.append(QAction(i, self.menuButtonAppend))
            self.connect(self.customAppendActions[-1], SIGNAL('triggered(bool)'), self.onImportCustom)
        self.menuButtonAppend.addActions(self.customAppendActions)
        self.ui.toolButtonAppend.setMenu(self.menuButtonAppend)
        
        # Export Button
        self.menuButtonExport = QMenu()
        self.menuButtonExport.addAction(self.ui.actionExport)
        self.menuButtonExport.addSeparator()
        self.customExportActions = []
        for i in self.settings['Export Settings'].keys():
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
        indexes.sort(reverse = True)

        for i in indexes:
            self.proxyModel.removeRows(i.row(), 1, QModelIndex())
            
        # Set up row indicator text
        self.ui.rowIndicator.setText('Rows: %s/%s' % (self.proxyModel.rowCount(), 
                                                      self.tableModel.rowCount(None)))

    def onResizeRowsToContents(self):
        self.ui.tableView.resizeRowsToContents()
        
    def onResizeRows(self):
        height = QInputDialog.getInteger(self, 'Rows height', 'Input a new rows height (min = 20 pts)', value = 30, min = 20, max = 1000)
        if height[1] == True:
            for i in range(self.proxyModel.rowCount()):
                self.ui.tableView.setRowHeight(i, height[0])
        
    def onLayoutChanged(self):
        self.ui.tableView.scrollTo(self.ui.tableView.currentIndex())
        
    def onImport(self):
        """
        Slot for importAction and appendAction signals
        """
        
        # Look for user defind default import action and use it to import data
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
        
        # Use App defaul import procedure otherwise
        # Set My clippings.txt file
        fileName = QFileDialog.getOpenFileName(self, '', '', "'My clippings.txt' file (*.txt)")
        if fileName == '' : return
        
        sender = self.sender()
        if sender == self.ui.actionImport:
            status = self.tableModel.parse(unicode(fileName), False)
        elif sender == self.ui.actionAppend:
            status = self.tableModel.parse(unicode(fileName), True)
                    
        print status
        self.ui.statusBar.showMessage(status, 3000)
            
        # Set up row indicator text
        self.ui.rowIndicator.setText('Rows: %s/%s' % (self.proxyModel.rowCount(), 
                                                      self.tableModel.rowCount(None)))
        
    def onImportCustom(self):
        """
        Slot for custom import actions triggered signals
        """
        sender = self.sender()
        #print sender.parent()
        if sender.parent() == self.menuButtonImport:
            actions = self.customImportActions
            append = False
        elif sender.parent() == self.menuButtonAppend:
            actions = self.customAppendActions
            append = True

        for i in actions:
            if sender == i:
                name = unicode(i.text())
                delimeter = self.settings['Import Settings'][name]['Delimiter']
                if delimeter == '' : delimeter = '\r\n'
                pattern = self.settings['Import Settings'][name]['Pattern']
                dateFormat = {'Qt' : self.settings['Import Settings'][name]['Date Format'],
                              'Python' : None}
                if dateFormat['Qt'] == '' : dateFormat = DEFAULT_DATE_FORMAT
                encoding = self.settings['Import Settings'][name]['Encoding'].split(' ')[0]
                if encoding == '' : encoding = DEFAULT_ENCODIG[0] #UTF-8
                extension = self.settings['Import Settings'][name]['Extension'].split(',')
                if extension[0] == '' : extension = DEFAULT_EXTENSION
                break
        fileName = QFileDialog.getOpenFileName(self, '', '', ';;'.join(['%s (*.%s)' % (name, ext) for ext in extension]))
        if fileName == '' : return

        status = self.tableModel.parse(unicode(fileName), append, False, delimeter, pattern, dateFormat, encoding)
        
        print status
        self.ui.statusBar.showMessage(status, 3000)
        
        # Set up row indicator text
        self.ui.rowIndicator.setText('Rows: %s/%s' % (self.proxyModel.rowCount(), 
                                                      self.tableModel.rowCount(None)))

    def onExport(self):
        """
        Slot for exportAction signal
        """
        
        # Look for user defind default import action and use it to import data
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

        
        # Use App default import procedure otherwise
        fileName = QFileDialog.getSaveFileNameAndFilter(self, '', '', "'My clippings.txt', UTF-8 (*.txt);;" +\
                                                                      'Tab separated values, UTF-16LE (*.csv)')
        if fileName[1] == 'My clippings txt, UTF-8 (*.txt)':
            self.saveTxt(unicode(fileName[0]))
        #elif fileName[1] == 'CSV, UTF-16LE (*.csv)':
            #self.saveCsvComma(unicode(fileName[0]))
        elif fileName[1] == 'Tab separated values, UTF-16LE (*.csv)':
            self.saveCsvTab(unicode(fileName[0]))
            
    def onExportCustom(self):
        """
        Slot for custom export actions triggered signals
        """
        sender = self.sender()
        for i in self.customExportActions:
            if sender == i:
                name = unicode(i.text())
                header = self.settings['Export Settings'][name]['Header']
                body = self.settings['Export Settings'][name]['Body']
                bottom = self.settings['Export Settings'][name]['Bottom']
                dateFormat = self.settings['Export Settings'][name]['Date Format']
                if dateFormat == '' : dateFormat = 'dd.MM.yy, hh:mm'
                encoding = self.settings['Export Settings'][name]['Encoding'].split(' ')[0]
                if encoding == '' : encoding = DEFAULT_ENCODIG[0] #UTF-8
                extension = self.settings['Export Settings'][name]['Extension'].split(',')
                if extension[0] == '' : extension = DEFAULT_EXTENSION
                break
        fileName = QFileDialog.getSaveFileName(self, '', '', ';;'.join(['%s (*.%s)' % (name, ext) for ext in extension]))
        if fileName == '' : return

        wildCards = re.findall(r'\?P<(.*?)>', body, re.UNICODE)
        
        fileOut = co.open(unicode(fileName), 'w', encoding, 'replace')
        fileOut.write(header)

        for row in range(self.proxyModel.rowCount()):
            # Proxy model model stores all the data in QVariant format,
            # so additional conversion to string is required
            #fileOut.write(body %\
                 #({HEADERS[0] : self.proxyModel.data(self.proxyModel.index(row, 0), Qt.DisplayRole).toString(),
                   #HEADERS[1] : self.proxyModel.data(self.proxyModel.index(row, 1), Qt.DisplayRole).toString(),
                   #HEADERS[2] : self.proxyModel.data(self.proxyModel.index(row, 2), Qt.DisplayRole).toString(),
                   #HEADERS[3] : self.proxyModel.data(self.proxyModel.index(row, 3), 
                                                     #Qt.EditRole).toDateTime().toString(dateFormat),
                   #HEADERS[4] : self.proxyModel.data(self.proxyModel.index(row, 4), Qt.DisplayRole).toString()}))
            
            # The top code is replaced to work when not enought variables to replace
            bodyLine = body
            for i in wildCards:
                if i == 'Date':
                    bodyLine = bodyLine.replace(u'?P<%s>' % i, unicode(self.proxyModel.data(self.proxyModel.index(row, HEADERS.index(i)), Qt.EditRole).toDateTime().toString(dateFormat)))
                elif i == 'XmlSafeText':
                    bodyLine = bodyLine.replace(u'?P<%s>' % i, re.sub("<(?!br/)","&lt;", re.sub("(?<!br/)>","&gt;",re.sub("&","&amp;",unicode(self.proxyModel.data(self.proxyModel.index(row, HEADERS.index('Text')), Qt.DisplayRole).toString()))))) # .translate({u',':u'_',u'<':u'&lt;',u'>':u'&gt;',u'&':u'&amp;'})
                elif i == 'EvernoteTagBook':
                    # replace_string = unicode(self.proxyModel.data(self.proxyModel.index(row, HEADERS.index('Book')), Qt.DisplayRole).toString()).translate(dict.fromkeys(map(ord, ','), None))
                    replace_string = unicode(self.proxyModel.data(self.proxyModel.index(row, HEADERS.index('Book')), Qt.DisplayRole).toString()).translate(dict((ord(char), u'_') for char in u','))
                    if len(replace_string) > 100:
                        replace_string = replace_string[:97] + '...'
                    if len(replace_string) > 0:
                        replace_string = u'<tag>' + replace_string + u'</tag>'
                    bodyLine = bodyLine.replace(u'?P<%s>' % i, replace_string)
                elif i == 'EvernoteTagAuthor':
                    # replace_string = unicode(self.proxyModel.data(self.proxyModel.index(row, HEADERS.index('Author')), Qt.DisplayRole).toString()).translate(dict.fromkeys(map(ord, ','), None))
                    replace_string = unicode(self.proxyModel.data(self.proxyModel.index(row, HEADERS.index('Author')), Qt.DisplayRole).toString()).translate(dict((ord(char), u'_') for char in u','))
                    if len(replace_string) > 100:
                        replace_string = replace_string[:97] + '...'
                    if len(replace_string) > 0:
                        replace_string = u'<tag>' + replace_string + u'</tag>'
                    bodyLine = bodyLine.replace(u'?P<%s>' % i, replace_string)
                else:
                    bodyLine = bodyLine.replace(u'?P<%s>' % i, unicode(self.proxyModel.data(self.proxyModel.index(row, HEADERS.index(i)), Qt.DisplayRole).toString()))
            fileOut.write(bodyLine)
        
        fileOut.write(bottom)
        fileOut.close()
        
        status = '<%s> Data are exported to "%s"' % (QTime.currentTime().toString('hh:mm:ss'), 
                                                   QDir.dirName(QDir(fileName)))
        print status
        self.ui.statusBar.showMessage(status, 3000)
            
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
            self.ui.filterEdit.setStyleSheet('background-color: qlineargradient(spread:pad, ' +\
                                             'x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 88, 88, 255), ' +\
                                             'stop:1 rgba(255, 255, 255, 255));;')
        else:
            self.ui.filterEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        
    def onFilterCaseState(self, state):
        self.proxyModel.setFilterCaseSensitivity(bool(state))
        self.onFilterInput(self.ui.filterEdit.text())
        
    def onFilterOptionTriggered(self, state):
        sender = self.sender()
        for h in self.tableModel.tableData.headers:
            if sender != self.actionFilterHeaders[h]:
                self.actionFilterHeaders[h].setEnabled(True)
                self.actionFilterHeaders[h].setChecked(False)
        if sender != self.actionFilterAll:
            self.actionFilterAll.setEnabled(True)
            self.actionFilterAll.setChecked(False)
            
            self.ui.filterOptionButton.setChecked(True)
            self.proxyModel.setFilterKeyColumn(self.tableModel.tableData.headers.index(sender.text()))
        else:
            self.ui.filterOptionButton.setChecked(False)
            self.proxyModel.setFilterKeyColumn(-1)
        sender.setEnabled(False)
        self.onFilterInput(self.ui.filterEdit.text())

            
    def saveTxt(self, fileName):
        """
        Save file in My clippings.txt format
        """
        fileOut = co.open(fileName, 'w', 'utf-8', 'replace')
        for row in range(self.proxyModel.rowCount()):
            # Proxy model model stores all the data in QVariant format,
            # so additional conversion to string is required
            fileOut.write(unicode('%s\r\n- %s Loc. %s  | Added on %s\r\n\r\n%s\r\n==========\r\n' %\
                 (self.proxyModel.data(self.proxyModel.index(row, 0), Qt.DisplayRole).toString(),
                  self.proxyModel.data(self.proxyModel.index(row, 2), Qt.DisplayRole).toString(),
                  self.proxyModel.data(self.proxyModel.index(row, 4), Qt.DisplayRole).toString(),
                  self.proxyModel.data(self.proxyModel.index(row, 5),
                                       Qt.EditRole).toDateTime().toString('dddd, MMMM dd, yyyy, hh:mm AP'),
                  self.proxyModel.data(self.proxyModel.index(row, 6), Qt.DisplayRole).toString())))
        fileOut.close()
        
        status = '<%s> Data are exported to "%s"' % (QTime.currentTime().toString('hh:mm:ss'), 
                                            QDir.dirName(QDir(fileName)))
        print status
        self.ui.statusBar.showMessage(status, 3000)
        
    def saveCsvTab(self, fileName):
        """
        Save file in .csv format
        """
        fileOut = co.open(fileName, 'w', 'utf-16', 'replace')
        # Write headers
        fileOut.write('"%s"\t"%s"\t"%s"\t"%s"\t"%s"\r\n' % self.tableModel.tableData.headers)
        for row in range(self.proxyModel.rowCount()):
            # Proxy model model stores all the data in QVariant format,
            # so additional conversion to string is required
            fileOut.write(unicode('%s\t%s\t%s\t%s\t%s\r\n' %\
                (self.proxyModel.data(self.proxyModel.index(row, 0), Qt.DisplayRole).toString(),
                 self.proxyModel.data(self.proxyModel.index(row, 2), Qt.DisplayRole).toString(),
                 self.proxyModel.data(self.proxyModel.index(row, 4), Qt.DisplayRole).toString(),
                 self.proxyModel.data(self.proxyModel.index(row, 5), Qt.DisplayRole).toString(),
                 self.proxyModel.data(self.proxyModel.index(row, 6), Qt.DisplayRole).toString())))
        fileOut.close()
        status = '<%s> Data are exported to "%s"' % (QTime.currentTime().toString('hh:mm:ss'), 
                                            QDir.dirName(QDir(fileName)))
        print status
        self.ui.statusBar.showMessage(status, 3000)
    
    #def saveCsvComma(self, fileName):
        #"""
        #Save file in .csv format with \t delimiter
        #"""
        #fileOut = co.open(fileName, 'w', 'utf-16', 'replace')
        ## Write headers
        #fileOut.write('"%s","%s","%s","%s","%s"\r\n' % self.tableModel.tableData.headers)
        #for row in range(self.proxyModel.rowCount()):
            ## Proxy model model stores all the data in QVariant format,
            ## so additional conversion to string is required
            #fileOut.write(unicode('"%s","%s","%s","%s","%s"\r\n' %\
                #(self.proxyModel.data(self.proxyModel.index(row, 0), Qt.DisplayRole).toString(),
                 #self.proxyModel.data(self.proxyModel.index(row, 1), Qt.DisplayRole).toString(),
                 #self.proxyModel.data(self.proxyModel.index(row, 2), Qt.DisplayRole).toString(),
                 #self.proxyModel.data(self.proxyModel.index(row, 3), Qt.DisplayRole).toString(),
                 #self.proxyModel.data(self.proxyModel.index(row, 4), Qt.DisplayRole).toString())))
        #fileOut.close()
        #status = '<%s> Data are exported to "%s"' % (QTime.currentTime().toString('hh:mm:ss'), 
                                            #QDir.dirName(QDir(fileName)))
        #print status
        #self.ui.statusBar.showMessage(status, 3000)

    def onAbout(self):
        about = QMessageBox(self)
        about.setTextFormat(Qt.RichText)
        about.setStandardButtons(QMessageBox.Ok | QMessageBox.Save)
        
        about.setWindowTitle(u'About...')
        about.setWindowIcon(QIcon(u':/icons/Bloomy/infoabout.png'))
        about.setText(u'<b>Klippings (ver. %s) — Kindle clippings viewer</b>' % __ver__)
        about.setInformativeText(u'Klippings (<a href="https://sites.google.com/site/kindlethearr/klippings/">' +
                                 u'homepage</a>) is a programm to view, edit and export ' +
                                 u'Kindle highlights, notes, and bookmarks, ' + 
                                 u'stored in \'My Clippings.txt\' file.<br><br><br>' + 
                                 u'<a href="https://sites.google.com/site/kindlethearr/">' +
                                 u'Author</a>: thearr, <i>hmi@ya.ru</i><br>' +
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
        webbrowser.open_new_tab('https://sites.google.com/site/kindlethearr/klippings/')
        
    def onSettings(self):
        settingsDialog = SettingsDialog(self)
        self.connect(settingsDialog, SIGNAL('settigsChanged(QString)'), self.onSettingsChanged)
        settingsDialog.show()
        
    def onSettingsChanged(self, settings):
        self.settings = sj.loads(unicode(settings))
        self.initiateToolButtons()        
                                                                 
if __name__ == '__main__':
    import sys
    import StringIO

    log = StringIO.StringIO()
    sys.stdout = log
    sys.stderr = log
    print u'# Log started on %s\n# %s' % (QDateTime.currentDateTime().toString('dd.MM.yy, hh:mm:ss'), '=' * 30)

    app = QApplication(sys.argv)
    mainWin = MainWin()
    mainWin.show()
    # Bring window to the front to cure PyInstaller bug under Mac OS X
    if osname == 'posix':
        mainWin.raise_()
    sys.exit(app.exec_())
    