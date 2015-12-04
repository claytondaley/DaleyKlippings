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
from pprint import pformat

logger = logging.getLogger("daley_klippings.settings")
logger.info("Loading DaleyKlippings Settings Models")

"""
Settings dialog
"""

import os
import codecs
from copy import deepcopy
import simplejson as sj
from appdirs import AppDirs
from PySide.QtCore import QRegExp, SIGNAL, Qt, Signal
from PySide.QtGui import QDialog, QWhatsThis, QRegExpValidator, QInputDialog, QApplication
from gui.ui_settingsDialog import Ui_settingsDialog


HEADERS = (u'Book',
           u'Author',
           u'Type',
           u'Page',
           u'Location',
           u'Date',
           u'Highlight',
           u'Note')


class ImportPattern(dict):
    VERSION = '1.0'
    DEFAULTS = {
        'Version': VERSION,
        'Pattern': ur"""
# --== SAMPLE PATTERN ==--
# Import notes, highlights, and bookmarks from "My Clippings.txt"
# Note that VERBOSE and UNICODE options are always on

^\s*                                  #
(?P<Book>.*?)                         # Book name
(\s*\((?P<Author>[^\()]*)\))?         # Author name (optional)
\s*-\ Your\                           #
(?P<Type>(Highlight|Note|Bookmarks))  # Clipping type
(\ on\ Page\                          #
(?P<Page>[\d-]*)\ \|)?                # Page (optional)
(.*(Location|Loc.)\                   #
(?P<Location>[\d-]*))?                # Location (optional)
.*?Added\ on\                         #
(?P<Date>(.*)([0-9:]{5})\ (AM|PM))    # Date & time
\s*                                   #
(?P<Text>.*?)                         # Text
\s*$                                  #""",
        'Default': 'False',
        'Delimiter': '=' * 10,
        'Date Format': 'dddd, MMMM dd, yyyy, hh:mm AP',
        'Encoding': 'UTF-8 (all languages)',
        'Extension': 'txt'
    }
    SAMPLE_DATE_FORMATS = {'Qt': 'dddd, MMMM dd, yyyy, hh:mm AP',
                           'Python': '%A, %B %d, %Y, %I:%M %p'}

    def __init__(self, settings=None):
        dict.__init__(self)
        self.update(self.DEFAULTS)
        if settings is not None:
            settings = deepcopy(settings)
            if 'Version' not in settings or settings['Version'] != self.VERSION:
                self.upgrade(settings)
            self.update(settings)

    def upgrade(self, settings):
        if 'Version' not in settings:
            settings['Version'] = '1.0'
        # Mutable, but returned for convenience
        return settings

    def delete(self):
        self['Deleted'] = 'True'
        self['Default'] = 'False'


class ExportPattern(dict):
    VERSION = '1.0'
    DEFAULTS = {
        'Version': VERSION,
        'Default': 'False',
        'Header': '',
        'Body': '',
        'Notes': '',
        'Bottom': '',
        'Date Format': 'yyyy-MM-dd HH:mm',
        'Extension': 'txt',
        'Encoding': 'UTF-8 (all languages)'
    }

    def __init__(self, settings=None):
        dict.__init__(self)
        self.update(self.DEFAULTS)
        if settings is not None:
            if 'Version' not in settings or settings['Version'] != self.VERSION:
                self.upgrade(settings)
            self.update(settings)

    def upgrade(self, settings):
        if 'Version' not in settings:
            settings['Version'] = '1.0'
        # Mutable, but returned for convenience
        return settings

    def delete(self):
        self['Deleted'] = 'True'
        self['Default'] = 'False'


class Settings(dict):
    VERSION = '1.0'
    ENGLISH = {
        'Highlight': 'Highlight',
        'Note': 'Note',
        'Bookmark': 'Bookmark',
        'Range Separator': '-',
        'Date Language': 'English (default)'
    }
    DEFAULTS = {
        'Version': VERSION,
        'Import Settings': {'Sample Pattern': ImportPattern()},
        'Export Settings': {'Sample Pattern': ExportPattern()},
        'Notes': {
            'Attach': 'True',
            'Position': 'Automatic (default)'
        },
        'Language': ENGLISH
    }

    def __init__(self, defaults=None):
        dict.__init__(self)
        # Ensure base structure is present
        dict.update(self, deepcopy(self.DEFAULTS))
        # If defaults aren't provided, use embedded defaults
        if defaults is not None:
            # Upgrade defaults to the current version
            if 'Version' not in defaults or defaults['Version'] != self.VERSION:
                self.upgrade(defaults)
            # Apply defaults to settings
            self.update(defaults)

    def upgrade(self, settings):
        # Upgrade settings that are
        if 'Version' not in self:
            logging.info("Upgrading settings from unversioned file.")
            settings['Notes'] = settings['Application Settings']['Attach Notes']
            del(settings['Application Settings']['Attach Notes'])
            settings['Notes']['Attach'] = settings['Notes']['Attach Notes']
            del(settings['Notes']['Attach Notes'])
            settings['Notes']['Position'] = settings['Notes']['Notes Position']
            del(settings['Notes']['Notes Position'])
            if 'Language' not in settings['Application Settings']:
                settings['Language'] = self.ENGLISH
            else:
                settings['Language'] = settings['Application Settings']['Language']
                del(settings['Application Settings']['Language'])
            del(settings['Application Settings'])
            for k, v in settings['Import Settings'].iteritems():
                if 'Default' not in v:
                    v['Default'] = 'False'
            for k, v in settings['Export Settings'].iteritems():
                if 'Default' not in v:
                    v['Default'] = 'False'
            settings['Version'] = '1.0'
        # Mutable, but returned for convenience
        return settings

    def getImportSettings(self, name=None):
        """
        Returns the requested import profile from the settings, with empty values filled by defaults
        """
        return self['ImportSettings'][name]

    def update(self, settings):
        settings = deepcopy(settings)
        for k, v in settings['Import Settings'].iteritems():
            self['Import Settings'][k] = ImportPattern(v)
        del settings['Import Settings']
        for k, v in settings['Export Settings'].iteritems():
            self['Export Settings'][k] = ExportPattern(v)
        del settings['Export Settings']
        dict.update(self, settings)
        del settings

    def addImportPattern(self, name):
        self['Import Settings'][name] = ImportPattern()

    def addExportPattern(self, name):
        self['Export Settings'][name] = ExportPattern()

    def removeImportPattern(self, name):
        self['Import Settings'][name].delete()

    def removeExportPattern(self, name):
        self['Export Settings'][name].delete()

    def setImportDefault(self, name, enabled):
        if enabled:
            # If we're enabling a default, we must ensure all other defaults are false
            for k, v in self['Import Settings'].iteritems():
                self['Import Settings'][k]['Default'] = 'False'
        self['Import Settings'][name]['Default'] = unicode(enabled)

    def setExportDefault(self, name, enabled):
        if enabled:
            # If we're enabling a default, we must ensure all other defaults are false
            for k, v in self['Export Settings'].iteritems():
                self['Export Settings'][k]['Default'] = 'False'
        self['Export Settings'][name]['Default'] = unicode(enabled)


class JsonFileStore(object):
    """
    Class that knows how to get and store a settings object as a Json File
    """
    def __init__(self, ui):
        self.ui = ui

        # Determine settings storage location
        if os.path.exists('portable.txt'):
            # Portable installation so we want to use the local directory and no additional processing is necessary
            self.settings_dir = os.path.dirname(__file__)
        else:
            # Not a portable installation so we need to correctly handle user folders
            # Start by getting the folder for the user's application data
            dirs = AppDirs("DaleyKlippings", "Eviduction")
            self.settings_dir = dirs.user_data_dir
            # If the daleyklippings folder does not exist in the user's application data, create it
            if not os.path.exists(self.settings_dir):
                os.makedirs(self.settings_dir)

    def load(self):
        # Default to object defaults
        self.defaults = Settings.DEFAULTS
        self.settings = Settings.DEFAULTS

        # Try loading dynamic defaults file
        try:
            defaultsFile = codecs.open(os.path.join(os.path.dirname(__file__), 'defaults.txt'), 'r', 'utf-8')
            defaults = sj.loads(defaultsFile.read())
            defaultsFile.close()
        except:
            pass
        else:
            self.defaults = defaults

        # Create settings object using defaults
        self.settings = Settings(self.defaults)

        # Find settings file, if it exists
        if os.path.exists(os.path.join(self.settings_dir, 'settings.txt')):
            settingsFile = os.path.join(self.settings_dir, 'settings.txt')
        elif os.path.exists('settings.txt'):
            logger.info("Migrating 'settings.txt' file from the DaleyKlippings folder to user's application data.")
            settingsFile = os.path.join(os.path.dirname(__file__), 'settings.txt')
        else:
            return

        # Try to open (and apply) the custom settings file
        settingsFile = codecs.open(settingsFile, 'r', 'utf-8')
        loaded = sj.loads(settingsFile.read())
        self.settings.update(loaded)
        settingsFile.close()
        return

    def get(self):
        return self.settings

    def diff(self, settings):
        logger.info("Starting diff() of Settings")
        if self.defaults is None:
            logger.info("... defaults not found, returning all settings")
            return self

        diff = deepcopy(settings)
        logger.info("Parsing Import Settings to find duplicates with default.")
        for k, v in diff['Import Settings'].items():
            if k in self.defaults['Import Settings'] and self.defaults['Import Settings'][k] == v:
                logger.debug("Import Pattern '%s' duplicates default" % k)
                del diff['Import Settings'][k]
        logger.info("Parsing Export Settings to find duplicates with default.")
        for k, v in diff['Export Settings'].items():
            if k in self.defaults['Export Settings'] and self.defaults['Export Settings'][k] == v:
                logger.debug("Export Pattern '%s' duplicates default" % k)
                del diff['Export Settings'][k]

        logger.info("Completed diff() of Settings")
        return diff

    def save(self, settings):
        logger.info("Staring save()")
        diff = self.diff(settings)
        logger.info("... writing backup settings file")
        settingsJson = sj.dumps(diff, indent='\t')
        settingsFile = codecs.open(os.path.join(self.settings_dir, 'settings.bak'), 'w', 'utf-8')
        settingsFile.write(settingsJson)
        settingsFile.close()
        logger.info("... writing settings file")
        settingsFile = codecs.open(os.path.join(self.settings_dir, 'settings.txt'), 'w', 'utf-8')
        settingsFile.write(settingsJson)
        settingsFile.close()
        logger.info("Finished save()")


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

    settingsChanged = Signal(dict)

    def __init__(self, settings, parent=None):
        QDialog.__init__(self, parent)

        # Need to make a local copy so we don't mutate the global settings dictionary when we cancel
        self.settings = deepcopy(settings)

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

        logger.info("Building Import Pattern Menu")
        # Initiate default Import settings
        index = 0
        self.ui.cmbImportPatternName.setCurrentIndex(index)
        for k in sorted(self.settings['Import Settings'].keys(), key=lambda s: s.lower()):
            # Exclude Deleted items
            if 'Deleted' in self.settings['Import Settings'][k]:
                logger.info("... skipping deleted pattern %s" % k)
            logger.info("... adding %s" % k)
            self.ui.cmbImportPatternName.addItem(k)
            if 'Default' in self.settings['Import Settings'][k] and self.settings['Import Settings'][k]['Default'] == 'True':
                self.ui.cmbImportPatternName.setCurrentIndex(index)
                self.ui.cmbImportPatternName.emit(SIGNAL('activated(QString)'), k)
            index += 1

        logger.info("Building Export Pattern Menu")
        # Initiate default Export settings
        index = 0
        self.ui.cmbExportPatternName.setCurrentIndex(index)
        for k in sorted(self.settings['Export Settings'].keys(), key=lambda s: s.lower()):
            # Exclude Deleted items
            if 'Deleted' in self.settings['Export Settings'][k]:
                logger.info("... skipping deleted pattern %s" % k)
            logger.info("... adding %s" % k)
            self.ui.cmbExportPatternName.addItem(k)
            if 'Default' in self.settings['Export Settings'][k] and self.settings['Export Settings'][k]['Default'] == 'True':
                self.ui.cmbExportPatternName.setCurrentIndex(index)
                self.ui.cmbExportPatternName.emit(SIGNAL('activated(QString)'), k)
            index += 1

        logger.info("Applying Application Settings")
        # Initiate active Application settings
        # Attach settings
        if self.settings['Notes']['Attach'] == 'True':
            self.ui.chbAttachNotes.setCheckState(Qt.Checked)
        else:
            self.ui.chbAttachNotes.setCheckState(Qt.Unchecked)
        self.ui.cmbNotesPosition.setCurrentIndex(self.ui.cmbNotesPosition.findText(self.settings['Notes']['Position']))

        # Set Language Settings
        logger.info("Applying Language Settings")
        # Date Language Options
        self.ui.cmbDateLanguage.insertSeparator(1000)
        self.ui.cmbDateLanguage.addItems(sorted(self.QLOCALE_LANGUAGE_LIST, key=lambda s: s.lower()))
        # Set Date Language Options
        lang = self.settings['Language']['Date Language']
        logger.info("lang is '%s'" % lang)
        langNo = self.ui.cmbDateLanguage.findText(lang)
        logger.info("langNo is %d" % langNo)
        self.ui.cmbDateLanguage.setCurrentIndex(langNo)

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
            ui_element.setText(unicode(self.settings['Language'][settings_key]))

    # Begin Import Tab Slots
    def onImportPatternActivated(self, item):
        if unicode(item) == '':
            # No pattern so disable the dialog
            self.ui.cmbImportPatternName.setEnabled(False)

            self.ui.chbIsDefaultImport.setEnabled(False)
            self.ui.chbIsDefaultImport.setChecked(False)

            self.ui.buttonImportDeletePattern.setEnabled(False)

            self.ui.editImportDelimiter.setEnabled(False)
            self.ui.editImportDelimiter.setText('')

            self.ui.textImportPattern.setEnabled(False)
            self.ui.textImportPattern.setPlainText('')

            self.ui.editImportDateFormat.setEnabled(False)
            self.ui.editImportDateFormat.setText('')

            self.ui.editImportExtension.setEnabled(False)
            self.ui.editImportExtension.setText('')

            self.ui.cmbImportEncoding.setEnabled(False)
            self.ui.cmbImportEncoding.setCurrentIndex(0)
        else:
            self.ui.cmbImportPatternName.setEnabled(True)

            self.ui.chbIsDefaultImport.setEnabled(True)
            isDefaultImport = self.settings['Import Settings'][unicode(item)]['Default']
            self.ui.chbIsDefaultImport.setChecked('True' == unicode(isDefaultImport))

            self.ui.buttonImportDeletePattern.setEnabled(True)

            self.ui.editImportDelimiter.setEnabled(True)
            delimiter = self.settings['Import Settings'][unicode(item)]['Delimiter']
            self.ui.editImportDelimiter.setText(delimiter)

            self.ui.textImportPattern.setEnabled(True)
            pattern = self.settings['Import Settings'][unicode(item)]['Pattern']
            self.ui.textImportPattern.setPlainText(pattern)

            self.ui.editImportDateFormat.setEnabled(True)
            dateFormat = self.settings['Import Settings'][unicode(item)]['Date Format']
            self.ui.editImportDateFormat.setText(dateFormat)

            self.ui.editImportExtension.setEnabled(True)
            extension = self.settings['Import Settings'][unicode(item)]['Extension']
            self.ui.editImportExtension.setText(extension)

            self.ui.cmbImportEncoding.setEnabled(True)
            encoding = self.settings['Import Settings'][unicode(item)]['Encoding']
            encodingNo = self.ui.cmbImportEncoding.findText(encoding)
            self.ui.cmbImportEncoding.setCurrentIndex(encodingNo)

    def onImportAddPattern(self):
        """
        Add new pattern
        """
        item = QInputDialog.getText(self, 'Add pattern', 'Input a new notes pattern name')
        # If not Cancelled
        if item[1] and unicode(item[0]).strip() != '':
            self.ui.cmbImportPatternName.addItem(item[0])
            # Activate just added item
            self.ui.cmbImportPatternName.setCurrentIndex(self.ui.cmbImportPatternName.count() - 1)
            self.settings.addImportPattern(unicode(item[0]))
            self.onImportPatternActivated(item[0])

    def onImportDeletePattern(self):
        # Delete current pattern from combo box and settings dictionary
        itemNo = self.ui.cmbImportPatternName.currentIndex()
        item = self.ui.cmbImportPatternName.currentText()
        self.ui.cmbImportPatternName.removeItem(itemNo)
        self.settings.removeImportPattern(unicode(item))
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
            self.settings.setImportDefault(unicode(item), u'True' == unicode(isDefaultImport))

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
        # Don't send signals to change settings
        self.blockSignals(True)

        if unicode(item) == '':
            self.ui.cmbExportPatternName.setEnabled(False)

            self.ui.chbIsDefaultExport.setEnabled(False)
            self.ui.chbIsDefaultExport.setChecked(False)

            self.ui.buttonExportDeletePattern.setEnabled(False)

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
            self.ui.cmbExportPatternName.setEnabled(True)

            self.ui.chbIsDefaultExport.setEnabled(True)
            isDefaultExport = self.settings['Export Settings'][unicode(item)]['Default']
            self.ui.chbIsDefaultExport.setChecked('True' == unicode(isDefaultExport))

            self.ui.buttonExportDeletePattern.setEnabled(True)

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

        self.blockSignals(False)

    def onExportAddPattern(self):
        """
        Add new pattern
        """
        item = QInputDialog.getText(self, 'Add pattern', 'Input new notes pattern name')
        # If not Cancelled
        if item[1] and unicode(item[0]).strip() != '':
            self.ui.cmbExportPatternName.addItem(item[0])
            # Activate just added item
            self.ui.cmbExportPatternName.setCurrentIndex(self.ui.cmbExportPatternName.count() - 1)
            self.settings.addExportPattern(unicode(item[0]))
            self.onExportPatternActivated(item[0])

    def onExportDeletePattern(self):
        # Delete current pattern from combo box and settings dictionary
        itemNo = self.ui.cmbExportPatternName.currentIndex()
        item = self.ui.cmbExportPatternName.currentText()
        self.ui.cmbExportPatternName.removeItem(itemNo)
        self.settings.removeExportPattern(unicode(item))
        # Update pattern text
        item = self.ui.cmbExportPatternName.currentText()
        self.onExportPatternActivated(item)

    def onExportIsDefaultChanged(self, isDefaultExport):
        item = self.ui.cmbExportPatternName.currentText()
        if unicode(item) != '':
            self.settings.setExportDefault(unicode(item), u'True' == unicode(isDefaultExport))

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

    #Begin Application Settings Slots
    def onApplicationAttachNotesChanged(self, state):
        # Turn off Notes Attach options if it is disabled
        self.ui.cmbNotesPosition.setEnabled(state)
        self.settings['Notes']['Attach'] = unicode(state)
        logger.info("Notes/Attach updated to %s" % self.settings['Notes']['Attach'])

    def onApplicationAttachNotesSettingsChanged(self, text):
        self.settings['Notes']['Position'] = unicode(text)
        logger.info("Notes/Position updated to %s" % self.settings['Notes']['Position'])

    def onApplicationDateLanguageChanged(self, language):
        self.settings['Language']['Date Language'] = unicode(language)
        logger.info("Language/Date Language updated to %s" % self.settings['Language']['Date Language'])

    def onApplicationRangeSeparatorChanged(self, text):
        self.settings['Language']['Range Separator'] = unicode(text)
        logger.info("Language/Range Separator updated to %s" % self.settings['Language']['Range Separator'])

    def onApplicationHighlightLanguageChanged(self, text):
        self.settings['Language']['Highlight'] = unicode(text)
        logger.info("Language/Highlight updated to %s" % self.settings['Language']['Highlight'])

    def onApplicationNoteLanguageChanged(self, text):
        self.settings['Language']['Note'] = unicode(text)
        logger.info("Language/Note updated to %s" % self.settings['Language']['Note'])

    def onApplicationBookmarkLanguageChanged(self, text):
        self.settings['Language']['Bookmark'] = unicode(text)
        logger.info("Language/Bookmark updated to %s" % self.settings['Language']['Bookmark'])
    #End Application Settings Slots

    def onButtonOK(self):
        self.onButtonApply()
        self.close()

    def onButtonApply(self):
        logger.info("Emitting settingsChanged")
        logger.debug("... with settings %s" % pformat(self.settings))
        # The signal is defined to carry a QString and has limited flexibility
        self.settingsChanged.emit(self.settings)

    def onButtonCancel(self):
        self.close()


# Test the dialog
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    settingsDialog = SettingsDialog()
    settingsDialog.show()
    sys.exit(app.exec_())