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
logger = logging.getLogger("daley_klippings.settings")
logger.info("Loading DaleyKlippings Settings Models")

"""
Settings dialog
"""

import re
import os
import codecs as co
import simplejson as sj
from copy import deepcopy
from pprint import pformat
from PySide.QtGui import *
from PySide.QtCore import *
from gui.ui_settingsDialog import *
from appdirs import AppDirs

HEADERS = (u'Book',
           u'Author',
           u'Type',
           u'Page',
           u'Location',
           u'Date',
           u'Highlight',
           u'Note')
DEFAULT_DELIMITER = '=' * 10
DEFAULT_PATTERN = ur"""
                ^\s*                           	#
                (?P<%s>.*?)                     # Book name
                (Inactive (?P<%s>.*?))?         # Eats up Author Header
                \s*-\                           #
                (?P<%s>\w*)                     # Clipping type
                (Inactive (?P<%s>.*?))?         # Eats up Page Header
                .*(Loc.|Page)\                  #
                (?P<%s>[\d-]*)           	    # Location
                .*?Added\ on\             	    #
                (?P<%s>(.*)(AM|PM))             # Date & time
                \s*                            	#
                (Inactive (?P<%s>.*?))?         # Eats up Highlight Header
                (Inactive (?P<%s>.*?))?         # Eats up Note Header
                \s*$ 		                    #
                """ % HEADERS
DEFAULT_RE_OPTIONS = re.UNICODE | re.VERBOSE | re.DOTALL
DEFAULT_DATE_FORMAT = {'Qt': 'dddd, MMMM dd, yyyy, hh:mm AP',
                       'Python': '%A, %B %d, %Y, %I:%M %p'}
DEFAULT_ENCODING = ['utf-8', 'utf-16']
DEFAULT_EXTENSION = ['txt', ]


class Settings(dict):
    # Structure of the settings file
    settings = {'Import Settings': {},
                'Export Settings': {},
                'Application Settings': {}}

    importSettings = {'Pattern': '',
                      'Default': '',
                      'Delimiter': '',
                      'Date Format': '',
                      'Encoding': '',
                      'Extension': ''}

    exportSettings = {'Default': '',
                      'Header': '',
                      'Body': '',
                      'Notes': '',
                      'Bottom': '',
                      'Date Format': '',
                      'Extension': '',
                      'Encoding': ''}

    applicationSettings = {'Attach Notes':
                           {
                               'Attach Notes': 'True',
                               'Notes Position': 'Automatic (default)'
                           },
                           'Language': {
                               'Highlight': '',
                               'Note': '',
                               'Bookmark': '',
                               'Range Separator': '',
                               'Date Language': 'English (default)'
                           }}

    @classmethod
    def from_json(cls, json):
        self = cls.__new__(cls)
        dict.__init__(self)
        self.update(sj.loads(unicode(json)))
        return self

    def __init__(self, parent=None):
        dict.__init__(self)

        if os.path.exists('portable.txt'):
            # Portable installation so we want to use the local directory and no additional processing is necessary
            self.settings_dir = ''
        else:
            # Not a portable installation so we need to correctly handle user folders
            # Start by getting the folder for the user's application data
            dirs = AppDirs("DaleyKlippings", "Eviduction")
            self.settings_dir = dirs.user_data_dir + os.sep
            # If the daleyklippings folder does not exist in the user's application data, create it
            if not os.path.exists(self.settings_dir):
                os.makedirs(self.settings_dir)
            # If the settings file is not in the user data folder but is found in the program folder, move it
            if not os.path.exists(self.settings_dir + 'settings.txt') and os.path.exists('settings.txt'):
                logger.info("Migrating 'settings.txt' file from the DaleyKlippings folder to user's application data.")
                import shutil
                shutil.copyfile('settings.txt', self.settings_dir + 'settings.txt')

        # Try to open (and apply) the default settings file
        try:
            defaultsFile = co.open('defaults.txt', 'r', 'utf-8')
        except:
            msg = 'Default settings file "defaults.txt"\nis could not be opened.  We will\n' \
                  'attempt to proceed using only the\n"settings.txt" file or built-in\n' \
                  'defaults but you should attempt to\nfix this situation.'
            QMessageBox.warning(parent, 'File not found', msg)
        else:
            try:
                defaults = sj.loads(defaultsFile.read())
            except:
                defaults = {}
                msg = 'Default settings file "defaults.txt"\nis in the wrong format and\ncould not be loaded.\n' \
                      'The file is probably corrupted.  We will\n attempt to proceed using only the\n' \
                      '"settings.txt" file or built-in\ndefaults but you should attempt to\nfix this situation.'
                QMessageBox.warning(parent, 'Default Settings File', msg)
            finally:
                defaultsFile.close()

        self.defaults = deepcopy(defaults)
        self.update(defaults)
        # Providing minimal data structure if defaults did not
        if 'Import Settings' not in self:
            self['Import Settings'] = {}
        if 'Export Settings' not in self:
            self['Export Settings'] = {}
        if 'Application Settings' not in self:
            self['Application Settings'] = {}
        # Must provide default settings for these since this could be the only way they get values
        if 'Attach Notes' not in self['Application Settings']:
            self['Application Settings']['Attach Notes'] = self.applicationSettings['Attach Notes']
        if 'Language' not in self['Application Settings']:
            self['Application Settings']['Language'] = self.applicationSettings['Language']

        # Try to open (and apply) the custom settings file
        try:
            settingsFile = co.open(self.settings_dir + 'settings.txt', 'r', 'utf-8')
        except:
            msg = 'Custom settings file "settings.txt"\nwas not found. We will create this file\n' \
                  'for you and start DaleyKlippings with the default settings.'
            QMessageBox.warning(parent, 'File not found', msg)
            # Create settings file to prevent the error from recurring
            self.save()
        else:
            try:
                settings = sj.loads(settingsFile.read())
            except:
                settings = {}
                msg = 'Settings file "settings.txt" is in the\nwrong format and could not be loaded.\n' \
                      'The file is probably corrupted. Please\nrestore an old version of this file from\n' \
                      'backups or delete the file to use\ndefault settings'
                QMessageBox.warning(parent, 'Settings File', msg)
            else:
                # Apply custom settings (if they exist)
                self['Import Settings'].update(settings['Import Settings'])
                self['Export Settings'].update(settings['Export Settings'])
                self['Application Settings']['Attach Notes'].update(settings['Application Settings']['Attach Notes'])
                self['Application Settings']['Language'].update(settings['Application Settings']['Language'])
            finally:
                settingsFile.close()

    def getImportSettings(self, name=None):
        """
        Returns the requested import profile from the settings, with empty values filled by defaults
        """
        if name is None:
            settings = deepcopy(self.importSettings)
        else:
            settings = deepcopy(self['Import Settings'][name])

        # Check for empty/non-existent values and set to defaults
        if settings['Delimiter'] == '':
            settings['Delimiter'] = DEFAULT_DELIMITER
        if settings['Date Format'] == '':
            settings['Date Format'] = DEFAULT_DATE_FORMAT['Qt']
        if settings['Encoding'] == '':
            settings['Encoding'] = DEFAULT_ENCODING[0]  # UTF-8
        if settings['Extension'] == '':
            settings['Extension'] = DEFAULT_EXTENSION[0]

        # Add application-wide settings
        settings['Application Settings'] = self['Application Settings']

        # Check for empty/non-existent values and set to defaults
        if settings['Application Settings']['Language']['Range Separator'] == '':
            settings['Application Settings']['Language']['Range Separator'] = '-'
        if settings['Application Settings']['Language']['Highlight'] == '':
            settings['Application Settings']['Language']['Highlight'] = 'Highlight'
        if settings['Application Settings']['Language']['Bookmark'] == '':
            settings['Application Settings']['Language']['Bookmark'] = 'Bookmark'
        if settings['Application Settings']['Language']['Note'] == '':
            settings['Application Settings']['Language']['Note'] = 'Note'
        return settings

    def get_custom(self, defaults=None):
        logger.info("Starting diff...")
        if defaults is None and self.defaults is None:
            logger.info("... defaults not found, returning self")
            return self
        elif defaults is None:
            logger.info("... getting defaults from object, with type %s" % type(self.defaults))
            defaults = deepcopy(self.defaults)

        diff = deepcopy(self)
        logger.info("Parsing Import Settings to find duplicates with default.")
        for key, value in diff['Import Settings'].items():
            if key in defaults['Import Settings'] and defaults['Import Settings'][key] == value:
                logger.debug("Import Pattern '%s' duplicates defaults" % key)
                del diff['Import Settings'][key]
        logger.info("Parsing Export Settings to find duplicates with default.")
        for key, value in diff['Export Settings'].items():
            if key in defaults['Export Settings'] and defaults['Export Settings'][key] == value:
                logger.debug("Import Pattern '%s' duplicates defaults" % key)
                del diff['Export Settings'][key]

        logger.info("Diff complete...")
        return diff

    def save(self):
        logger.info("Staring save...")
        diff = self.get_custom()
        settingsJson = sj.dumps(diff, indent='\t')
        settingsFile = co.open(self.settings_dir + 'settings.bak', 'w', 'utf-8')
        settingsFile.write(settingsJson)
        settingsFile.close()
        settingsFile = co.open(self.settings_dir + 'settings.txt', 'w', 'utf-8')
        settingsFile.write(settingsJson)
        settingsFile.close()
        logger.info("Save complete, returning JSON of settings...")
        return sj.dumps(self, indent='\t')


class SettingsDialog(QDialog):
    """
    Settings dialog class
    """

    ENCODINGS_LIST = [
        'ASCII (English)',
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
        'UTF-8-SIG (all languages)',
        'Windows-1252'
    ]

    QLOCALE_LANGUAGE_LIST = [
        'Abkhazian',
        'Afan',
        'Afar',
        'Afrikaans',
        'Albanian',
        'Amharic',
        'Arabic',
        'Armenian',
        'Assamese',
        'Aymara',
        'Azerbaijani',
        'Bashkir',
        'Basque',
        'Bengali',
        'Bhutani',
        'Bihari',
        'Bislama',
        'Bosnian',
        'Breton',
        'Bulgarian',
        'Burmese',
        'Byelorussian',
        'Cambodian',
        'Catalan',
        'Chinese',
        'Cornish',
        'Corsican',
        'Croatian',
        'Czech',
        'Danish',
        'Divehi',
        'Dutch',
        'English',
        'Esperanto',
        'Estonian',
        'Faroese',
        'FijiLanguage',
        'Finnish',
        'French',
        'Frisian',
        'Gaelic',
        'Galician',
        'Georgian',
        'German',
        'Greek',
        'Greenlandic',
        'Guarani',
        'Gujarati',
        'Hausa',
        'Hebrew',
        'Hindi',
        'Hungarian',
        'Icelandic',
        'Indonesian',
        'Interlingua',
        'Interlingue',
        'Inuktitut',
        'Inupiak',
        'Irish',
        'Italian',
        'Japanese',
        'Javanese',
        'Kannada',
        'Kashmiri',
        'Kazakh',
        'Kinyarwanda',
        'Kirghiz',
        'Korean',
        'Kurdish',
        'Kurundi',
        'Laothian',
        'Latin',
        'Latvian',
        'Lingala',
        'Lithuanian',
        'Macedonian',
        'Malagasy',
        'Malay',
        'Malayalam',
        'Maltese',
        'Manx',
        'Maori',
        'Marathi',
        'Moldavian',
        'Mongolian',
        'NauruLanguage',
        'Nepali',
        'Norwegian',
        'NorwegianBokmal',
        'NorwegianNynorsk',
        'Occitan',
        'Oriya',
        'Pashto',
        'Persian',
        'Polish',
        'Portuguese',
        'Punjabi',
        'Quechua',
        'RhaetoRomance',
        'Romanian',
        'Russian',
        'Samoan',
        'Sangho',
        'Sanskrit',
        'Serbian',
        'SerboCroatian',
        'Sesotho',
        'Setswana',
        'Shona',
        'Sindhi',
        'Singhalese',
        'Siswati',
        'Slovak',
        'Slovenian',
        'Somali',
        'Spanish',
        'Sundanese',
        'Swahili',
        'Swedish',
        'Tagalog',
        'Tajik',
        'Tamil',
        'Tatar',
        'Telugu',
        'Thai',
        'Tibetan',
        'Tigrinya',
        'TongaLanguage',
        'Tsonga',
        'Turkish',
        'Turkmen',
        'Twi',
        'Uigur',
        'Ukrainian',
        'Urdu',
        'Uzbek',
        'Vietnamese',
        'Volapuk',
        'Welsh',
        'Wolof',
        'Xhosa',
        'Yiddish',
        'Yoruba',
        'Zhuang',
        'Zulu',
        'Bosnian',
        'Divehi',
        'Manx',
        'Cornish',
        'Akan',
        'Konkani',
        'Ga',
        'Igbo',
        'Kamba',
        'Syriac',
        'Blin',
        'Geez',
        'Koro',
        'Sidamo',
        'Atsam',
        'Tigre',
        'Jju',
        'Friulian',
        'Venda',
        'Ewe',
        'Walamo',
        'Hawaiian',
        'Tyap',
        'Chewa',
        'Filipino',
        'SwissGerman',
        'SichuanYi',
        'Kpelle',
        'LowGerman',
        'SouthNdebele',
        'NorthernSotho',
        'NorthernSami',
        'Taroko',
        'Gusii',
        'Taita',
        'Fulah',
        'Kikuyu',
        'Samburu',
        'Sena',
        'NorthNdebele',
        'Rombo',
        'Tachelhit',
        'Kabyle',
        'Nyankole',
        'Bena',
        'Vunjo',
        'Bambara',
        'Embu',
        'Cherokee',
        'Morisyen',
        'Makonde',
        'Langi',
        'Ganda',
        'Bemba',
        'Kabuverdianu',
        'Meru',
        'Kalenjin',
        'Nama',
        'Machame',
        'Colognian',
        'Masai',
        'Soga',
        'Luyia',
        'Asu',
        'Teso',
        'Saho',
        'KoyraChiini',
        'Rwa',
        'Luo',
        'Chiga',
        'CentralMoroccoTamazight',
        'KoyraboroSenni',
        'Shambala'
    ]

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.settings = Settings(self)

        # Initiate GUI
        self.ui = Ui_settingsDialog()
        self.ui.setupUi(self)
        self.ui.cmbImportEncoding.insertSeparator(1000)  # Big enough number to insert it at the end
        self.ui.cmbImportEncoding.addItems(self.ENCODINGS_LIST)
        self.ui.cmbExportEncoding.insertSeparator(1000)
        self.ui.cmbExportEncoding.addItems(self.ENCODINGS_LIST)

        # Initiate WhatsThis button for Mac OS X
        if os.name == 'posix':
            self.actionWhatsThis = QWhatsThis.createAction(self)
            self.ui.buttonWhatsThis.setDefaultAction(self.actionWhatsThis)
        elif os.name == 'nt':
            self.ui.buttonWhatsThis.setVisible(False)

        # Set validators
        self.extensionValidator = QRegExpValidator(QRegExp('([a-zA-Z0-9]+,?)*'), self.ui.editImportExtension)
        self.ui.editImportExtension.setValidator(self.extensionValidator)
        self.ui.editExportExtensions.setValidator(self.extensionValidator)

        # Initiate default Import settings
        self.ui.cmbImportPatternName.addItems(
            # Exclude Deleted items
            sorted([k for k, v in self.settings['Import Settings'].items() if 'Deleted' not in v]))
        item = self.ui.cmbImportPatternName.currentText()
        self.ui.cmbImportPatternName.emit(SIGNAL('activated(QString)'), item)

        # Initiate default Export settings
        self.ui.cmbExportPatternName.addItems(
            # Exclude Deleted items
            sorted([k for k, v in self.settings['Export Settings'].items() if 'Deleted' not in v]))
        item = self.ui.cmbExportPatternName.currentText()
        self.ui.cmbExportPatternName.emit(SIGNAL('activated(QString)'), item)

        logger.info("Applying Application Settings")
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

        # Set Language Settings
        logger.info("Applying Language Settings")
        if 'Language' not in self.settings['Application Settings']:
            logger.info("... language not in settings, setting entire language config to default")
            self.settings['Application Settings']['Language'] = self.settings.applicationSettings['Language']
        else:
            logger.info("... language in settings, updating UI")
            # Date Language Options
            self.ui.cmbDateLanguage.insertSeparator(1000)
            self.ui.cmbDateLanguage.addItems(sorted(self.QLOCALE_LANGUAGE_LIST))
            # Set Date Language Options
            if 'Date Language' in self.settings['Application Settings']['Language']:
                logger.info("... date language in settings, applying")
                lang = self.settings['Application Settings']['Language']['Date Language']
                logger.info("lang is '%s'" % lang)
                langNo = self.ui.cmbDateLanguage.findText(lang)
                logger.info("langNo is %d" % langNo)
                self.ui.cmbDateLanguage.setCurrentIndex(langNo)
            else:
                logger.info("... date language not in settings, setting to default")
                self.settings['Application Settings']['Language']['Date Language'] = \
                    self.settings.applicationSettings['Language']['Date Language']

            # Additional Language Options
            # Iteration ensures that we don't overwrite existing settings when a new field is added
            language_settings = [
                (self.ui.editHighlightLanguage, 'Highlight'),
                (self.ui.editNoteLanguge, 'Note'),
                (self.ui.editBookmarkLanguage, 'Bookmark'),
                (self.ui.editRangeSeparator, 'Range Separator'),
            ]
            for ui_element, settings_key in language_settings:
                logger.info("Setting UI for %s" % settings_key)
                try:
                    ui_element.setText(unicode(self.settings['Application Settings']['Language'][settings_key]))
                except:
                    # Create empty keys in the dictionary
                    self.settings['Application Settings']['Language'][settings_key] = \
                        self.settings.applicationSettings['Language'][settings_key]

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
            self.settings['Import Settings'][unicode(item[0])] = self.settings.importSettings
            self.onImportPatternActivated(item[0])

    def onImportDeletePattern(self):
        # Delete current pattern from combo box and settings dictionary
        itemNo = self.ui.cmbImportPatternName.currentIndex()
        item = self.ui.cmbImportPatternName.currentText()
        self.ui.cmbImportPatternName.removeItem(itemNo)
        self.settings['Import Settings'][unicode(item)]['Deleted'] = "True"
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
            self.settings['Import Settings'][unicode(item)]['Pattern'] = unicode(pattern)

    def onImportIsDefaultChanged(self, isDefaultImport):
        item = self.ui.cmbImportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Import Settings'][unicode(item)]['Default'] = unicode(isDefaultImport)
            # If new Default state is True then change Default settings of all other imports to False
            if unicode(self.settings['Import Settings'][unicode(item)]['Default']) == 'True':
                for i in self.settings['Import Settings']:
                    if unicode(i) != unicode(item):
                        self.settings['Import Settings'][unicode(i)]['Default'] = 'False'

    def onImportDelimiterChanged(self, delimiter):
        item = self.ui.cmbImportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Import Settings'][unicode(item)]['Delimiter'] = unicode(delimiter)

    def onImportExtensionChanged(self, extension):
        item = self.ui.cmbImportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Import Settings'][unicode(item)]['Extension'] = unicode(extension)

    def onImportEncodingChanged(self, encoding):
        item = self.ui.cmbImportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Import Settings'][unicode(item)]['Encoding'] = unicode(encoding)

    def onImportDateFormatChanged(self, dateFormat):
        item = self.ui.cmbImportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Import Settings'][unicode(item)]['Date Format'] = unicode(dateFormat)
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
        self.settings['Export Settings'][unicode(item)]['Deleted'] = "True"
        # Update pattern text
        item = self.ui.cmbExportPatternName.currentText()
        self.onExportPatternActivated(item)

    def onExportIsDefaultChanged(self, isDefaultExport):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Export Settings'][unicode(item)]['Default'] = unicode(isDefaultExport)
            # If new Default state is True then change Default settings of all other exports to False
            if unicode(self.settings['Export Settings'][unicode(item)]['Default']) == 'True':
                for i in self.settings['Export Settings']:
                    if unicode(i) != unicode(item):
                        self.settings['Export Settings'][unicode(i)]['Default'] = 'False'

    def onExportHeaderChanged(self):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            header = self.ui.textExportHeader.toPlainText()
            self.settings['Export Settings'][unicode(item)]['Header'] = unicode(header)

    def onExportBodyChanged(self):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            body = self.ui.textExportBody.toPlainText()
            self.settings['Export Settings'][unicode(item)]['Body'] = unicode(body)

    def onExportNotesChanged(self):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            notes = self.ui.textExportNotes.toPlainText()
            self.settings['Export Settings'][unicode(item)]['Notes'] = unicode(notes)

    def onExportBottomChanged(self):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            bottom = self.ui.textExportBottom.toPlainText()
            self.settings['Export Settings'][unicode(item)]['Bottom'] = unicode(bottom)

    def onExportDateFormatChanged(self, dateFormat):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Export Settings'][unicode(item)]['Date Format'] = unicode(dateFormat)

    def onExportEncodingChanged(self, encoding):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Export Settings'][unicode(item)]['Encoding'] = unicode(encoding)

    def onExportExtensionChanged(self, extension):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            self.settings['Export Settings'][unicode(item)]['Extension'] = unicode(extension)
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

    def onApplicationDateLanguageChanged(self, language):
        self.settings['Application Settings']['Language']['Date Language'] = unicode(language)

    def onApplicationRangeSeparatorChanged(self, text):
        self.settings['Application Settings']['Language']['Range Separator'] = unicode(text)

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
        settingsJson = self.settings.save()
        logger.info("Emitting settingsChanged")
        self.emit(SIGNAL('settingsChanged(QString)'), settingsJson)

    def onButtonCancel(self):
        self.close()


# Test the dialog
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    settingsDialog = SettingsDialog()
    settingsDialog.show()
    sys.exit(app.exec_())