#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Settings dialog
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import codecs as co
import simplejson as sj
import re
from os import name as osname

from gui.ui_settingsDialog import *
import table

class Settings(dict):
    
    # Structure of the settings file
    settings = {'Import Settings' : {},
                'Export Settings' : {},
                'Application Settings' : {}}
    
    importSettigs = {'Pattern' : '',
                     'Default' : '',
                     'Delimiter' : '',
                     'Date Format' : '',
                     'Encoding' : '',
                     'Extension' : ''}
    
    exportSettings = {'Default' : '',
                      'Header' : '',
                      'Body' : '',
                      'Notes' : '',
                      'Bottom' : '',
                      'Date Format' : '',
                      'Extension' : '',
                      'Encoding' : ''}
    
    applicationSettings = {'Attach Notes' : {'Attach Notes' : '',
                                             'Notes Position' : ''},
                           'Language' : {'Highlight' : '',
                                         'Note' : '',
                                         'Bookmark' : ''}}
    
    def __init__(self, parent = None):
        dict.__init__(self)
        try:
            # Load settings from file
            settingsFile = co.open('settings.txt', 'r', 'utf-8')
            self.settings = sj.loads(settingsFile.read())
            settingsFile.close()
        except:
            #QMessageBox.warning(parent, 'File not found', 'File "settings.txt" is not found')
            pass

        self.update(self.settings)

class SettingsDialog(QDialog):
    """
    Settings dialog class
    """

    encodingsList = ['ASCII (English)',
                     'BIG5 (Traditional Chinese)',
                     'BIG5HKSCS (Traditional Chinese)',
                     'CP037 (English)',
                     'CP424 (Hebrew)',
                     'CP437 (English)',
                     'CP500 (Western Europe)',
                     'CP720 (Arabic)',
                     'CP737 (Greek)',
                     'CP775 (Baltic languages)',
                     'CP850 (Western Europe)',
                     'CP852 (Central and Eastern Europe)',
                     'CP855 (Bulg., Byel., Maced., Rus., Serb.)',
                     'CP856 (Hebrew)',
                     'CP857 (Turkish)',
                     'CP858 (Western Europe)',
                     'CP860 (Portuguese)',
                     'CP861 (Icelandic)',
                     'CP862 (Hebrew)',
                     'CP863 (Canadian)',
                     'CP864 (Arabic)',
                     'CP865 (Danish, Norwegian)',
                     'CP866 (Russian)',
                     'CP869 (Greek)',
                     'CP874 (Thai)',
                     'CP875 (Greek)',
                     'CP932 (Japanese)',
                     'CP949 (Korean)',
                     'CP950 (Traditional Chinese)',
                     'CP1006 (Urdu)',
                     'CP1026 (Turkish)',
                     'CP1140 (Western Europe)',
                     'CP1250 (Central and Eastern Europe)',
                     'CP1251 (Bulg., Byel., Maced., Rus., Serb.)',
                     'CP1252 (Western Europe)',
                     'CP1253 (Greek)',
                     'CP1254 (Turkish)',
                     'CP1255 (Hebrew)',
                     'CP1256 (Arabic)',
                     'CP1257 (Baltic languages)',
                     'CP1258 (Vietnamese)',
                     'EUC-JP (Japanese)',
                     'EUC-JIS-2004 (Japanese)',
                     'EUC-JISX0213 (Japanese)',
                     'EUC-KR (Korean)',
                     'GB2312 (Simplified Chinese)',
                     'GBK (Unified Chinese)',
                     'GB18030 (Unified Chinese)',
                     'HZ (Simplified Chinese)',
                     'ISO2022-JP (Japanese)',
                     'ISO2022-JP-1 (Japanese)',
                     'ISO2022-JP-2 (Jap., Kor., Simpl.Ch., W.Eur., Greek)',
                     'ISO2022-JP-2004 (Japanese)',
                     'ISO2022-JP-3 (Japanese)',
                     'ISO2022-JP-EXT (Japanese)',
                     'ISO2022-KR (Korean)',
                     'LATIN-1 (West Europe)',
                     'ISO8859-2 (Central and Eastern Europe)',
                     'ISO8859-3 (Esperanto, Maltese)',
                     'ISO8859-4 (Baltic languages)',
                     'ISO8859-5 (Bulg., Byel., Maced., Rus., Serb.)',
                     'ISO8859-6 (Arabic)',
                     'ISO8859-7 (Greek)',
                     'ISO8859-8 (Hebrew)',
                     'ISO8859-9 (Turkish)',
                     'ISO8859-10 (Nordic languages)',
                     'ISO8859-13 (Baltic languages)',
                     'ISO8859-14 (Celtic languages)',
                     'ISO8859-15 (Western Europe)',
                     'ISO8859-16 (South-Eastern Europe)',
                     'JOHAB (Korean)',
                     'KOI8-R (Russian)',
                     'KOI8-U (Ukrainian)',
                     'MAC-CYRILLIC (Bul., Byel., Maced., Rus., Serb.)',
                     'MAC-GREEK (Greek)',
                     'MAC-ICELAND (Icelandic)',
                     'MAC-LATIN2 (Central and Eastern Europe)',
                     'MAC-ROMAN (Western Europe)',
                     'MAC-TURKISH (Turkish)',
                     'PTCP154 (Kazakh)',
                     'SHIFT-JIS (Japanese)',
                     'SHIFT-JIS-2004 (Japanese)',
                     'SHIFT-JISX0213 (Japanese)',
                     'UTF-32-BE (all languages)',
                     'UTF-32-LE (all languages)',
                     'UTF-16-BE (all languages (BMP only))',
                     'UTF-16-LE (all languages (BMP only))',
                     'UTF-7 (all languages)',
                     'UTF-8-SIG (all languages)']
    
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.settings = Settings(self)
        
        # Initiate GUI
        self.ui = Ui_settingsDialog()
        self.ui.setupUi(self)
        self.ui.cmbImportEncoding.insertSeparator(1000) # Big enough number to insert it at the end
        self.ui.cmbImportEncoding.addItems(self.encodingsList)
        self.ui.cmbExportEncoding.insertSeparator(1000)
        self.ui.cmbExportEncoding.addItems(self.encodingsList)
        
        # Initiate WhatsThis button for Mac OS X
        if osname == 'posix':
            self.actionWhatsThis = QWhatsThis.createAction(self)
            self.ui.buttonWhatsThis.setDefaultAction(self.actionWhatsThis)
        elif osname == 'nt':
            self.ui.buttonWhatsThis.setVisible(False)
        
        # Set validators
        self.extensionValidator = QRegExpValidator(QRegExp('([a-zA-Z0-9]+,?)*'), self.ui.editImportExtension)
        self.ui.editImportExtension.setValidator(self.extensionValidator)
        self.ui.editExportExtensions.setValidator(self.extensionValidator)
        
        # Initiate default Import settings
        self.ui.cmbImportPatternName.addItems(self.settings['Import Settings'].keys())
        item = self.ui.cmbImportPatternName.currentText()
        self.ui.cmbImportPatternName.emit(SIGNAL('activated(QString)'), item)
        
        # Initiate default Export settings
        self.ui.cmbExportPatternName.addItems(self.settings['Export Settings'].keys())
        item = self.ui.cmbExportPatternName.currentText()
        self.ui.cmbExportPatternName.emit(SIGNAL('activated(QString)'), item)
        
        # Initiate active Application settings
        # Attach settings
        try:
            if self.settings['Application Settings']['Attach Notes']['Attach Notes'] == 'True':
                self.ui.chbAttachNotes.setCheckState(Qt.Checked)
            else:
                self.ui.chbAttachNotes.setCheckState(Qt.Unchecked)
            self.ui.cmbNotesPosition.setCurrentIndex(self.ui.cmbNotesPosition.findText(
                self.settings['Application Settings']['Attach Notes']['Notes Position']))
        except:
            # Create empty keys in the dictionary
            self.settings['Application Settings']['Attach Notes'] = self.settings.applicationSettings['Attach Notes']
                    
        # Language settings
        try:
            self.ui.editHighlightLanguage.setText(unicode(
                self.settings['Application Settings']['Language']['Highlight']))
            self.ui.editNoteLanguge.setText(unicode(
                self.settings['Application Settings']['Language']['Note']))
            self.ui.editBookmarkLanguage.setText(unicode(
                self.settings['Application Settings']['Language']['Bookmark']))
        except:
            # Create empty keys in the dictionary
            self.settings['Application Settings']['Language'] = self.settings.applicationSettings['Language']
    
    # Begin Import Tab Slots
    def onImportPatternActivated(self, item):
        if unicode(item) == '':
            self.ui.textImportPattern.setEnabled(False)
            self.ui.textImportPattern.setPlainText('') 
            
            self.ui.chbIsDefaultImport.setEnabled(False)
            self.ui.chbIsDefaultImport.setChecked(False)
            
            self.ui.editImportDelimiter.setEnabled(False)
            self.ui.editImportDelimiter.setText('')
            
            self.ui.editImportExtension.setEnabled(False)
            self.ui.editImportExtension.setText('')
            
            self.ui.cmbImportEncoding.setEnabled(False)
            self.ui.cmbImportEncoding.setCurrentIndex(0)
            
            self.ui.editImportDateFormat.setEnabled(False)
            self.ui.editImportDateFormat.setText('')
        else:
            self.ui.textImportPattern.setEnabled(True)
            pattern = self.settings['Import Settings'][unicode(item)]['Pattern']
            self.ui.textImportPattern.setPlainText(pattern)
            
            self.ui.chbIsDefaultImport.setEnabled(True)
            # try-except to ensure compatibility with old settings files
            try:
                isDefaultImport = self.settings['Import Settings'][unicode(item)]['Default']
            except:
                self.settings['Import Settings'][unicode(item)]['Default'] = 'False'
                isDefaultImport = 'False'
            self.ui.chbIsDefaultImport.setChecked('True' == unicode(isDefaultImport))

            self.ui.editImportDelimiter.setEnabled(True)
            delimiter = self.settings['Import Settings'][unicode(item)]['Delimiter']
            self.ui.editImportDelimiter.setText(delimiter)
            
            self.ui.editImportExtension.setEnabled(True)
            extension = self.settings['Import Settings'][unicode(item)]['Extension']
            self.ui.editImportExtension.setText(extension)
            
            self.ui.cmbImportEncoding.setEnabled(True)
            encoding = self.settings['Import Settings'][unicode(item)]['Encoding']
            encodingNo = self.ui.cmbImportEncoding.findText(encoding)
            self.ui.cmbImportEncoding.setCurrentIndex(encodingNo)
            
            self.ui.editImportDateFormat.setEnabled(True)
            dateFormat = self.settings['Import Settings'][unicode(item)]['Date Format']
            self.ui.editImportDateFormat.setText(dateFormat)
    
    def onImportAddPattern(self):
        """
        Add new pattern
        """
        item = QInputDialog.getText(self, 'Add pattern', 'Input a new notes pattern name')
        if item[1] == True and unicode(item[0]).strip() != '': 
            self.ui.cmbImportPatternName.addItem(item[0])
            # Activate just added item
            self.ui.cmbImportPatternName.setCurrentIndex(self.ui.cmbImportPatternName.count() - 1)
            self.settings['Import Settings'][unicode(item[0])] = self.settings.importSettigs
            self.onImportPatternActivated(item[0])
        
    def onImportDeletePattern(self): 
        # Delete current pattern from combo box and settings dictionary
        itemNo = self.ui.cmbImportPatternName.currentIndex()
        item = self.ui.cmbImportPatternName.currentText()
        self.ui.cmbImportPatternName.removeItem(itemNo)
        del(self.settings['Import Settings'][unicode(item)])
        # Update pattern text
        item = self.ui.cmbImportPatternName.currentText()
        self.onImportPatternActivated(item)
        
    def onImportPatternChanged(self):
        item = self.ui.cmbImportPatternName.currentText()
        if unicode(item) != '':
            pattern = self.ui.textImportPattern.toPlainText()
            # Due to strange Python bug I can't use here and latter just one line:
            # self.settings['Import Settings'][unicode(item)]['Pattern'] = unicode(pattern)
            # becuse Python change value for all members with the same key
            self.settings['Import Settings'][unicode(item)] = \
                {'Pattern' : unicode(pattern),
                 'Default' : self.settings['Import Settings'][unicode(item)]['Default'],
                 'Delimiter' : self.settings['Import Settings'][unicode(item)]['Delimiter'],
                 'Encoding' : self.settings['Import Settings'][unicode(item)]['Encoding'],
                 'Date Format' : self.settings['Import Settings'][unicode(item)]['Date Format'],
                 'Extension' : self.settings['Import Settings'][unicode(item)]['Extension']}
            
    def onImportIsDefaultChanged(self, isDefaultImport):
        item = self.ui.cmbImportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Import Settings'][unicode(item)] = \
                {'Default' : unicode(isDefaultImport),
                 'Pattern' : self.settings['Import Settings'][unicode(item)]['Pattern'],
                 'Delimiter' : self.settings['Import Settings'][unicode(item)]['Delimiter'],
                 'Encoding' : self.settings['Import Settings'][unicode(item)]['Encoding'],
                 'Date Format' : self.settings['Import Settings'][unicode(item)]['Date Format'],
                 'Extension' : self.settings['Import Settings'][unicode(item)]['Extension']}
            # If new Default state is True then change Default settings of all other imports to False
            if unicode(self.settings['Import Settings'][unicode(item)]['Default']) == 'True':
                for i in self.settings['Import Settings']:
                    if unicode(i) != unicode(item):
                        self.settings['Import Settings'][unicode(i)] = \
                            {'Default' : 'False',
                             'Pattern' : self.settings['Import Settings'][unicode(i)]['Pattern'],
                             'Delimiter' : self.settings['Import Settings'][unicode(i)]['Delimiter'],
                             'Encoding' : self.settings['Import Settings'][unicode(i)]['Encoding'],
                             'Date Format' : self.settings['Import Settings'][unicode(i)]['Date Format'],
                             'Extension' : self.settings['Import Settings'][unicode(i)]['Extension']}
                                                               
            
    def onImportDelimiterChanged(self, delimiter):
        item = self.ui.cmbImportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Import Settings'][unicode(item)] = \
                {'Delimiter' : unicode(delimiter),
                 'Default' : self.settings['Import Settings'][unicode(item)]['Default'],
                 'Pattern' : self.settings['Import Settings'][unicode(item)]['Pattern'],
                 'Encoding' : self.settings['Import Settings'][unicode(item)]['Encoding'],
                 'Date Format' : self.settings['Import Settings'][unicode(item)]['Date Format'],
                 'Extension' : self.settings['Import Settings'][unicode(item)]['Extension']}
            
    def onImportExtensionChanged(self, extension):
        item = self.ui.cmbImportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Import Settings'][unicode(item)] = \
                {'Extension' : unicode(extension),
                 'Pattern' : self.settings['Import Settings'][unicode(item)]['Pattern'],
                 'Default' : self.settings['Import Settings'][unicode(item)]['Default'],
                 'Encoding' : self.settings['Import Settings'][unicode(item)]['Encoding'],
                 'Date Format' : self.settings['Import Settings'][unicode(item)]['Date Format'],
                 'Delimiter' : self.settings['Import Settings'][unicode(item)]['Delimiter']}
    
    def onImportEncodingChanged(self, encoding):
        item = self.ui.cmbImportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Import Settings'][unicode(item)] = \
                {'Encoding' : unicode(encoding),
                 'Pattern' : self.settings['Import Settings'][unicode(item)]['Pattern'],
                 'Default' : self.settings['Import Settings'][unicode(item)]['Default'],
                 'Extension' : self.settings['Import Settings'][unicode(item)]['Extension'],
                 'Date Format' : self.settings['Import Settings'][unicode(item)]['Date Format'],
                 'Delimiter' : self.settings['Import Settings'][unicode(item)]['Delimiter']}
            
    def onImportDateFormatChanged(self, dateFormat):
        item = self.ui.cmbImportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Import Settings'][unicode(item)] = \
                {'Date Format' : unicode(dateFormat),
                 'Pattern' : self.settings['Import Settings'][unicode(item)]['Pattern'],
                 'Default' : self.settings['Import Settings'][unicode(item)]['Default'],
                 'Extension' : self.settings['Import Settings'][unicode(item)]['Extension'],
                 'Encoding' : self.settings['Import Settings'][unicode(item)]['Encoding'],
                 'Delimiter' : self.settings['Import Settings'][unicode(item)]['Delimiter']}
    # End Import Tab Slots
    
    # Begin Export Tab Slots
    def onExportPatternActivated(self, item):
        if unicode(item) == '':
            self.ui.chbIsDefaultExport.setEnabled(False)
            self.ui.chbIsDefaultExport.setChecked(False)
            
            self.ui.textExportHeader.setEnabled(False)
            self.ui.textExportHeader.setPlainText('') 
            
            self.ui.textExportBody.setEnabled(False)
            self.ui.textExportBody.setPlainText('')

            self.ui.textExportNotes.setEnabled(False)
            self.ui.textExportNotes.setPlainText('')

            self.ui.textExportBottom.setEnabled(False)
            self.ui.textExportBottom.setPlainText('')
            
            self.ui.editExportDateFormat.setEnabled(False)
            self.ui.editExportDateFormat.setText('')
            
            self.ui.editExportExtensions.setEnabled(False)
            self.ui.editExportExtensions.setText('')
            
            self.ui.cmbExportEncoding.setEnabled(False)
            self.ui.cmbExportEncoding.setCurrentIndex(0)

        else:
            self.ui.chbIsDefaultExport.setEnabled(True)
            # try-except to ensure compatibility with old settings files
            try:
                isDefaultExport = self.settings['Export Settings'][unicode(item)]['Default']
            except:
                self.settings['Export Settings'][unicode(item)]['Default'] = 'False'
                isDefaultExport = 'False'
            self.ui.chbIsDefaultExport.setChecked('True' == unicode(isDefaultExport))
            
            self.ui.textExportHeader.setEnabled(True)
            header = self.settings['Export Settings'][unicode(item)]['Header']
            self.ui.textExportHeader.setPlainText(header)

            self.ui.textExportBody.setEnabled(True)
            body = self.settings['Export Settings'][unicode(item)]['Body']
            self.ui.textExportBody.setPlainText(body)

            self.ui.textExportNotes.setEnabled(True)
            notes = self.settings['Export Settings'][unicode(item)]['Notes']
            self.ui.textExportNotes.setPlainText(notes)

            self.ui.textExportBottom.setEnabled(True)
            bottom = self.settings['Export Settings'][unicode(item)]['Bottom']
            self.ui.textExportBottom.setPlainText(bottom)
            
            self.ui.editExportDateFormat.setEnabled(True)
            dateFormat = self.settings['Export Settings'][unicode(item)]['Date Format']
            self.ui.editExportDateFormat.setText(dateFormat)
            
            self.ui.editExportExtensions.setEnabled(True)
            extension = self.settings['Export Settings'][unicode(item)]['Extension']
            self.ui.editExportExtensions.setText(extension)
            
            self.ui.cmbExportEncoding.setEnabled(True)
            encoding = self.settings['Export Settings'][unicode(item)]['Encoding']
            encodingNo = self.ui.cmbExportEncoding.findText(encoding)
            self.ui.cmbExportEncoding.setCurrentIndex(encodingNo)
            
    def onExportAddPattern(self):
        """
        Add new pattern
        """
        item = QInputDialog.getText(self, 'Add pattern', 'Input new notes pattern name')
        if item[1] == True and unicode(item[0]).strip() != '': 
            self.ui.cmbExportPatternName.addItem(item[0])
            # Activate just added item
            self.ui.cmbExportPatternName.setCurrentIndex(self.ui.cmbExportPatternName.count() - 1)
            self.settings['Export Settings'][unicode(item[0])] = self.settings.exportSettings
            self.onExportPatternActivated(item[0])
            
    def onExportDeletePattern(self): 
        # Delete current pattern from combo box and settings dictionary
        itemNo = self.ui.cmbExportPatternName.currentIndex()
        item = self.ui.cmbExportPatternName.currentText()
        self.ui.cmbExportPatternName.removeItem(itemNo)
        del(self.settings['Export Settings'][unicode(item)])
        # Update pattern text
        item = self.ui.cmbExportPatternName.currentText()
        self.onExportPatternActivated(item)
    
    def onExportIsDefaultChanged(self, isDefaultExport):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Export Settings'][unicode(item)] = \
                {'Default' : unicode(isDefaultExport),
                 'Header' : self.settings['Export Settings'][unicode(item)]['Header'],
                 'Body' : self.settings['Export Settings'][unicode(item)]['Body'],
                 'Notes' : self.settings['Export Settings'][unicode(item)]['Notes'],
                 'Bottom' : self.settings['Export Settings'][unicode(item)]['Bottom'],
                 'Encoding' : self.settings['Export Settings'][unicode(item)]['Encoding'],
                 'Date Format' : self.settings['Export Settings'][unicode(item)]['Date Format'],
                 'Extension' : self.settings['Export Settings'][unicode(item)]['Extension']}
            # If new Default state is True then change Default settings of all other exports to False
            if unicode(self.settings['Export Settings'][unicode(item)]['Default']) == 'True':
                for i in self.settings['Export Settings']:
                    if unicode(i) != unicode(item):
                        self.settings['Export Settings'][unicode(i)] = \
                            {'Default' : 'False',
                             'Header' : self.settings['Export Settings'][unicode(i)]['Header'],
                             'Body' : self.settings['Export Settings'][unicode(i)]['Body'],
                             'Notes' : self.settings['Export Settings'][unicode(i)]['Notes'],
                             'Bottom' : self.settings['Export Settings'][unicode(i)]['Bottom'],
                             'Encoding' : self.settings['Export Settings'][unicode(i)]['Encoding'],
                             'Date Format' : self.settings['Export Settings'][unicode(i)]['Date Format'],
                             'Extension' : self.settings['Export Settings'][unicode(i)]['Extension']}
        
    def onExportHeaderChanged(self):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            header = self.ui.textExportHeader.toPlainText()
            self.settings['Export Settings'][unicode(item)] = \
                {'Header' : unicode(header),
                 'Default' : self.settings['Export Settings'][unicode(item)]['Default'],
                 'Body' : self.settings['Export Settings'][unicode(item)]['Body'],
                 'Notes' : self.settings['Export Settings'][unicode(item)]['Notes'],
                 'Bottom' : self.settings['Export Settings'][unicode(item)]['Bottom'],
                 'Encoding' : self.settings['Export Settings'][unicode(item)]['Encoding'],
                 'Date Format' : self.settings['Export Settings'][unicode(item)]['Date Format'],
                 'Extension' : self.settings['Export Settings'][unicode(item)]['Extension']}
            
    def onExportBodyChanged(self):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            body = self.ui.textExportBody.toPlainText()
            self.settings['Export Settings'][unicode(item)] = \
                {'Default' : self.settings['Export Settings'][unicode(item)]['Default'],
                 'Header' : self.settings['Export Settings'][unicode(item)]['Header'],
                 'Body' : unicode(body),
                 'Notes' : self.settings['Export Settings'][unicode(item)]['Notes'],
                 'Bottom' : self.settings['Export Settings'][unicode(item)]['Bottom'],
                 'Encoding' : self.settings['Export Settings'][unicode(item)]['Encoding'],
                 'Date Format' : self.settings['Export Settings'][unicode(item)]['Date Format'],
                 'Extension' : self.settings['Export Settings'][unicode(item)]['Extension']}

    def onExportNotesChanged(self):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            notes = self.ui.textExportNotes.toPlainText()
            self.settings['Export Settings'][unicode(item)] =\
                {'Default' : self.settings['Export Settings'][unicode(item)]['Default'],
                 'Header' : self.settings['Export Settings'][unicode(item)]['Header'],
                 'Body' : self.settings['Export Settings'][unicode(item)]['Body'],
                 'Notes' : unicode(notes),
                 'Bottom' : self.settings['Export Settings'][unicode(item)]['Bottom'],
                 'Encoding' : self.settings['Export Settings'][unicode(item)]['Encoding'],
                 'Date Format' : self.settings['Export Settings'][unicode(item)]['Date Format'],
                 'Extension' : self.settings['Export Settings'][unicode(item)]['Extension']}

    def onExportBottomChanged(self):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            bottom = self.ui.textExportBottom.toPlainText()
            self.settings['Export Settings'][unicode(item)] = \
                {'Default' : self.settings['Export Settings'][unicode(item)]['Default'],
                 'Header' : self.settings['Export Settings'][unicode(item)]['Header'],
                 'Body' : self.settings['Export Settings'][unicode(item)]['Body'],
                 'Notes' : self.settings['Export Settings'][unicode(item)]['Notes'],
                 'Bottom' : unicode(bottom),
                 'Encoding' : self.settings['Export Settings'][unicode(item)]['Encoding'],
                 'Date Format' : self.settings['Export Settings'][unicode(item)]['Date Format'],
                 'Extension' : self.settings['Export Settings'][unicode(item)]['Extension']}
            
    def onExportDateFormatChanged(self, dateFormat):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Export Settings'][unicode(item)] = \
                {'Default' : self.settings['Export Settings'][unicode(item)]['Default'],
                 'Header' : self.settings['Export Settings'][unicode(item)]['Header'],
                 'Body' : self.settings['Export Settings'][unicode(item)]['Body'],
                 'Notes' : self.settings['Export Settings'][unicode(item)]['Notes'],
                 'Bottom' : self.settings['Export Settings'][unicode(item)]['Bottom'],
                 'Encoding' : self.settings['Export Settings'][unicode(item)]['Encoding'],
                 'Date Format' : unicode(dateFormat),
                 'Extension' : self.settings['Export Settings'][unicode(item)]['Extension']}
    
    def onExportEncodingChanged(self, encoding):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Export Settings'][unicode(item)] = \
                {'Default' : self.settings['Export Settings'][unicode(item)]['Default'],
                 'Header' : self.settings['Export Settings'][unicode(item)]['Header'],
                 'Body' : self.settings['Export Settings'][unicode(item)]['Body'],
                 'Notes' : self.settings['Export Settings'][unicode(item)]['Notes'],
                 'Bottom' : self.settings['Export Settings'][unicode(item)]['Bottom'],
                 'Encoding' : unicode(encoding),
                 'Date Format' : self.settings['Export Settings'][unicode(item)]['Date Format'],
                 'Extension' : self.settings['Export Settings'][unicode(item)]['Extension']}
            
    def onExportExtensionChanged(self, extension):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Export Settings'][unicode(item)] = \
                {'Default' : self.settings['Export Settings'][unicode(item)]['Default'],
                 'Header' : self.settings['Export Settings'][unicode(item)]['Header'],
                 'Body' : self.settings['Export Settings'][unicode(item)]['Body'],
                 'Notes' : self.settings['Export Settings'][unicode(item)]['Notes'],
                 'Bottom' : self.settings['Export Settings'][unicode(item)]['Bottom'],
                 'Encoding' : self.settings['Export Settings'][unicode(item)]['Encoding'],
                 'Date Format' : self.settings['Export Settings'][unicode(item)]['Date Format'],
                 'Extension' : unicode(extension)}  
    #End Export Settings Slots
    
    #Begin Appliction Settings Slots
    def onApplicationAttachNotesChanged(self, state):
        # Turn off Notes Attach options if it is disabled
        self.ui.cmbNotesPosition.setEnabled(state)
        self.settings['Application Settings']['Attach Notes']['Attach Notes'] = unicode(state)

    def onApplicationAttachNotesSettingsChanged(self, text):
        sender = self.sender()
        if sender == self.ui.cmbNotesPosition:
            self.settings['Application Settings']['Attach Notes']['Notes Position'] = unicode(text)

    def onApplicationHighlightLanguageChanged(self, text):
        self.settings['Application Settings']['Language']['Highlight'] = unicode(text)
        
    def onApplicationNoteLanguageChanged(self, text):
        self.settings['Application Settings']['Language']['Note'] = unicode(text)
        
    def onApplicationBookmarkLanguageChanged(self, text):
        self.settings['Application Settings']['Language']['Bookmark'] = unicode(text)
    #End Application Settings Slots
                  
    def onButtonOK(self):
        self.onButtonApply()
        self.close()
    
    def onButtonApply(self):
        settingsFile = co.open('settings.txt', 'w', 'utf-8')
        settingsJson = sj.dumps(self.settings, indent = '\t')
        settingsFile.write(settingsJson)
        self.emit(SIGNAL('settigsChanged(QString)'), settingsJson)
        settingsFile.close()
                
    def onButtonCancel(self):
        self.close()


# Test the dialog
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    settingsDialog = SettingsDialog()
    settingsDialog.show()
    sys.exit(app.exec_())