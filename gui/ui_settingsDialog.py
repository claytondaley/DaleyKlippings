# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsDialog.ui'
#
# Created: Tue Jun 03 21:34:57 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_settingsDialog(object):
    def setupUi(self, settingsDialog):
        settingsDialog.setObjectName("settingsDialog")
        settingsDialog.resize(1009, 768)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/Bloomy/configure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        settingsDialog.setWindowIcon(icon)
        settingsDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        settingsDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(settingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabsSettings = QtGui.QTabWidget(settingsDialog)
        self.tabsSettings.setEnabled(True)
        self.tabsSettings.setObjectName("tabsSettings")
        self.tabApplication = QtGui.QWidget()
        self.tabApplication.setObjectName("tabApplication")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tabApplication)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupNotesAttachments = QtGui.QGroupBox(self.tabApplication)
        self.groupNotesAttachments.setObjectName("groupNotesAttachments")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupNotesAttachments)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.chbAttachNotes = QtGui.QCheckBox(self.groupNotesAttachments)
        self.chbAttachNotes.setChecked(True)
        self.chbAttachNotes.setObjectName("chbAttachNotes")
        self.verticalLayout_3.addWidget(self.chbAttachNotes)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.labelNotesPosition = QtGui.QLabel(self.groupNotesAttachments)
        self.labelNotesPosition.setObjectName("labelNotesPosition")
        self.gridLayout_3.addWidget(self.labelNotesPosition, 0, 0, 1, 1)
        self.cmbNotesPosition = QtGui.QComboBox(self.groupNotesAttachments)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbNotesPosition.sizePolicy().hasHeightForWidth())
        self.cmbNotesPosition.setSizePolicy(sizePolicy)
        self.cmbNotesPosition.setObjectName("cmbNotesPosition")
        self.cmbNotesPosition.addItem("")
        self.cmbNotesPosition.addItem("")
        self.cmbNotesPosition.addItem("")
        self.gridLayout_3.addWidget(self.cmbNotesPosition, 0, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.verticalLayout_5.addWidget(self.groupNotesAttachments)
        self.groupLanguage = QtGui.QGroupBox(self.tabApplication)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupLanguage.sizePolicy().hasHeightForWidth())
        self.groupLanguage.setSizePolicy(sizePolicy)
        self.groupLanguage.setObjectName("groupLanguage")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.groupLanguage)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.labelDateLanguage = QtGui.QLabel(self.groupLanguage)
        self.labelDateLanguage.setObjectName("labelDateLanguage")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelDateLanguage)
        self.cmbDateLanguage = QtGui.QComboBox(self.groupLanguage)
        self.cmbDateLanguage.setObjectName("cmbDateLanguage")
        self.cmbDateLanguage.addItem("")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmbDateLanguage)
        self.editRangeSeparator = QtGui.QLineEdit(self.groupLanguage)
        self.editRangeSeparator.setObjectName("editRangeSeparator")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.editRangeSeparator)
        self.labelHighlightLanguage = QtGui.QLabel(self.groupLanguage)
        self.labelHighlightLanguage.setObjectName("labelHighlightLanguage")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelHighlightLanguage)
        self.editHighlightLanguage = QtGui.QLineEdit(self.groupLanguage)
        self.editHighlightLanguage.setObjectName("editHighlightLanguage")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.editHighlightLanguage)
        self.labelNoteLanguge = QtGui.QLabel(self.groupLanguage)
        self.labelNoteLanguge.setObjectName("labelNoteLanguge")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelNoteLanguge)
        self.editNoteLanguge = QtGui.QLineEdit(self.groupLanguage)
        self.editNoteLanguge.setObjectName("editNoteLanguge")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.editNoteLanguge)
        self.labelBookmarkLanguage = QtGui.QLabel(self.groupLanguage)
        self.labelBookmarkLanguage.setObjectName("labelBookmarkLanguage")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelBookmarkLanguage)
        self.editBookmarkLanguage = QtGui.QLineEdit(self.groupLanguage)
        self.editBookmarkLanguage.setObjectName("editBookmarkLanguage")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.editBookmarkLanguage)
        self.labelRangeSeparator = QtGui.QLabel(self.groupLanguage)
        self.labelRangeSeparator.setObjectName("labelRangeSeparator")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelRangeSeparator)
        self.verticalLayout_6.addLayout(self.formLayout)
        self.verticalLayout_5.addWidget(self.groupLanguage)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.tabsSettings.addTab(self.tabApplication, "")
        self.tabImport = QtGui.QWidget()
        self.tabImport.setObjectName("tabImport")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabImport)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelImportPatternName = QtGui.QLabel(self.tabImport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelImportPatternName.sizePolicy().hasHeightForWidth())
        self.labelImportPatternName.setSizePolicy(sizePolicy)
        self.labelImportPatternName.setObjectName("labelImportPatternName")
        self.horizontalLayout_2.addWidget(self.labelImportPatternName)
        self.cmbImportPatternName = QtGui.QComboBox(self.tabImport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbImportPatternName.sizePolicy().hasHeightForWidth())
        self.cmbImportPatternName.setSizePolicy(sizePolicy)
        self.cmbImportPatternName.setObjectName("cmbImportPatternName")
        self.horizontalLayout_2.addWidget(self.cmbImportPatternName)
        self.chbIsDefaultImport = QtGui.QCheckBox(self.tabImport)
        self.chbIsDefaultImport.setObjectName("chbIsDefaultImport")
        self.horizontalLayout_2.addWidget(self.chbIsDefaultImport)
        self.buttonImportAddPattern = QtGui.QPushButton(self.tabImport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonImportAddPattern.sizePolicy().hasHeightForWidth())
        self.buttonImportAddPattern.setSizePolicy(sizePolicy)
        self.buttonImportAddPattern.setObjectName("buttonImportAddPattern")
        self.horizontalLayout_2.addWidget(self.buttonImportAddPattern)
        self.buttonImportDeletePattern = QtGui.QPushButton(self.tabImport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonImportDeletePattern.sizePolicy().hasHeightForWidth())
        self.buttonImportDeletePattern.setSizePolicy(sizePolicy)
        self.buttonImportDeletePattern.setObjectName("buttonImportDeletePattern")
        self.horizontalLayout_2.addWidget(self.buttonImportDeletePattern)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.boxImportPattern = QtGui.QGroupBox(self.tabImport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boxImportPattern.sizePolicy().hasHeightForWidth())
        self.boxImportPattern.setSizePolicy(sizePolicy)
        self.boxImportPattern.setObjectName("boxImportPattern")
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.boxImportPattern)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelImportDelimiter = QtGui.QLabel(self.boxImportPattern)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelImportDelimiter.sizePolicy().hasHeightForWidth())
        self.labelImportDelimiter.setSizePolicy(sizePolicy)
        self.labelImportDelimiter.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelImportDelimiter.setObjectName("labelImportDelimiter")
        self.gridLayout.addWidget(self.labelImportDelimiter, 0, 0, 1, 1)
        self.editImportDelimiter = QtGui.QLineEdit(self.boxImportPattern)
        self.editImportDelimiter.setPlaceholderText("==========")
        self.editImportDelimiter.setObjectName("editImportDelimiter")
        self.gridLayout.addWidget(self.editImportDelimiter, 0, 1, 1, 1)
        self.labelImportPattern = QtGui.QLabel(self.boxImportPattern)
        self.labelImportPattern.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelImportPattern.setObjectName("labelImportPattern")
        self.gridLayout.addWidget(self.labelImportPattern, 1, 0, 1, 1)
        self.textImportPattern = QtGui.QPlainTextEdit(self.boxImportPattern)
        self.textImportPattern.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.textImportPattern.setObjectName("textImportPattern")
        self.gridLayout.addWidget(self.textImportPattern, 1, 1, 1, 1)
        self.labelImportDateFormat = QtGui.QLabel(self.boxImportPattern)
        self.labelImportDateFormat.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelImportDateFormat.setObjectName("labelImportDateFormat")
        self.gridLayout.addWidget(self.labelImportDateFormat, 2, 0, 1, 1)
        self.editImportDateFormat = QtGui.QLineEdit(self.boxImportPattern)
        self.editImportDateFormat.setPlaceholderText("dddd, MMMM dd, yyyy, hh:mm AP")
        self.editImportDateFormat.setObjectName("editImportDateFormat")
        self.gridLayout.addWidget(self.editImportDateFormat, 2, 1, 1, 1)
        self.horizontalLayout_8.addLayout(self.gridLayout)
        self.verticalLayout_2.addWidget(self.boxImportPattern)
        self.boxImportFileSettings = QtGui.QGroupBox(self.tabImport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boxImportFileSettings.sizePolicy().hasHeightForWidth())
        self.boxImportFileSettings.setSizePolicy(sizePolicy)
        self.boxImportFileSettings.setObjectName("boxImportFileSettings")
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.boxImportFileSettings)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.labelImportExtension = QtGui.QLabel(self.boxImportFileSettings)
        self.labelImportExtension.setObjectName("labelImportExtension")
        self.horizontalLayout_5.addWidget(self.labelImportExtension)
        self.editImportExtension = QtGui.QLineEdit(self.boxImportFileSettings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editImportExtension.sizePolicy().hasHeightForWidth())
        self.editImportExtension.setSizePolicy(sizePolicy)
        self.editImportExtension.setPlaceholderText("txt")
        self.editImportExtension.setObjectName("editImportExtension")
        self.horizontalLayout_5.addWidget(self.editImportExtension)
        self.labeImportlEncoding = QtGui.QLabel(self.boxImportFileSettings)
        self.labeImportlEncoding.setObjectName("labeImportlEncoding")
        self.horizontalLayout_5.addWidget(self.labeImportlEncoding)
        self.cmbImportEncoding = QtGui.QComboBox(self.boxImportFileSettings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbImportEncoding.sizePolicy().hasHeightForWidth())
        self.cmbImportEncoding.setSizePolicy(sizePolicy)
        self.cmbImportEncoding.setObjectName("cmbImportEncoding")
        self.cmbImportEncoding.addItem("")
        self.cmbImportEncoding.setItemText(0, "UTF-8 (all languages)")
        self.cmbImportEncoding.addItem("")
        self.cmbImportEncoding.setItemText(1, "UTF-16 (all languages)")
        self.cmbImportEncoding.addItem("")
        self.cmbImportEncoding.setItemText(2, "UTF-32 (all languages)")
        self.horizontalLayout_5.addWidget(self.cmbImportEncoding)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addWidget(self.boxImportFileSettings)
        self.tabsSettings.addTab(self.tabImport, "")
        self.tabExport = QtGui.QWidget()
        self.tabExport.setObjectName("tabExport")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tabExport)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelExportPatternName = QtGui.QLabel(self.tabExport)
        self.labelExportPatternName.setObjectName("labelExportPatternName")
        self.horizontalLayout_4.addWidget(self.labelExportPatternName)
        self.cmbExportPatternName = QtGui.QComboBox(self.tabExport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbExportPatternName.sizePolicy().hasHeightForWidth())
        self.cmbExportPatternName.setSizePolicy(sizePolicy)
        self.cmbExportPatternName.setObjectName("cmbExportPatternName")
        self.horizontalLayout_4.addWidget(self.cmbExportPatternName)
        self.chbIsDefaultExport = QtGui.QCheckBox(self.tabExport)
        self.chbIsDefaultExport.setObjectName("chbIsDefaultExport")
        self.horizontalLayout_4.addWidget(self.chbIsDefaultExport)
        self.buttonExportAddPattern = QtGui.QPushButton(self.tabExport)
        self.buttonExportAddPattern.setObjectName("buttonExportAddPattern")
        self.horizontalLayout_4.addWidget(self.buttonExportAddPattern)
        self.buttonExportDeletePattern = QtGui.QPushButton(self.tabExport)
        self.buttonExportDeletePattern.setObjectName("buttonExportDeletePattern")
        self.horizontalLayout_4.addWidget(self.buttonExportDeletePattern)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.boxExportPattern = QtGui.QGroupBox(self.tabExport)
        self.boxExportPattern.setObjectName("boxExportPattern")
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.boxExportPattern)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelExportHeader = QtGui.QLabel(self.boxExportPattern)
        self.labelExportHeader.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelExportHeader.setObjectName("labelExportHeader")
        self.gridLayout_2.addWidget(self.labelExportHeader, 0, 0, 1, 1)
        self.textExportHeader = QtGui.QPlainTextEdit(self.boxExportPattern)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.textExportHeader.sizePolicy().hasHeightForWidth())
        self.textExportHeader.setSizePolicy(sizePolicy)
        self.textExportHeader.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.textExportHeader.setObjectName("textExportHeader")
        self.gridLayout_2.addWidget(self.textExportHeader, 0, 1, 1, 1)
        self.labelExportBody = QtGui.QLabel(self.boxExportPattern)
        self.labelExportBody.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelExportBody.setObjectName("labelExportBody")
        self.gridLayout_2.addWidget(self.labelExportBody, 1, 0, 1, 1)
        self.textExportBody = QtGui.QPlainTextEdit(self.boxExportPattern)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textExportBody.sizePolicy().hasHeightForWidth())
        self.textExportBody.setSizePolicy(sizePolicy)
        self.textExportBody.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.textExportBody.setObjectName("textExportBody")
        self.gridLayout_2.addWidget(self.textExportBody, 1, 1, 1, 1)
        self.labelExportBottom = QtGui.QLabel(self.boxExportPattern)
        self.labelExportBottom.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelExportBottom.setObjectName("labelExportBottom")
        self.gridLayout_2.addWidget(self.labelExportBottom, 3, 0, 1, 1)
        self.textExportBottom = QtGui.QPlainTextEdit(self.boxExportPattern)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.textExportBottom.sizePolicy().hasHeightForWidth())
        self.textExportBottom.setSizePolicy(sizePolicy)
        self.textExportBottom.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.textExportBottom.setObjectName("textExportBottom")
        self.gridLayout_2.addWidget(self.textExportBottom, 3, 1, 1, 1)
        self.labelExportDateFormat = QtGui.QLabel(self.boxExportPattern)
        self.labelExportDateFormat.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelExportDateFormat.setObjectName("labelExportDateFormat")
        self.gridLayout_2.addWidget(self.labelExportDateFormat, 4, 0, 1, 1)
        self.editExportDateFormat = QtGui.QLineEdit(self.boxExportPattern)
        self.editExportDateFormat.setPlaceholderText("dd.MM.yy, hh:mm")
        self.editExportDateFormat.setObjectName("editExportDateFormat")
        self.gridLayout_2.addWidget(self.editExportDateFormat, 4, 1, 1, 1)
        self.labelExportNotes = QtGui.QLabel(self.boxExportPattern)
        self.labelExportNotes.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelExportNotes.setObjectName("labelExportNotes")
        self.gridLayout_2.addWidget(self.labelExportNotes, 2, 0, 1, 1)
        self.textExportNotes = QtGui.QPlainTextEdit(self.boxExportPattern)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.textExportNotes.sizePolicy().hasHeightForWidth())
        self.textExportNotes.setSizePolicy(sizePolicy)
        self.textExportNotes.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.textExportNotes.setObjectName("textExportNotes")
        self.gridLayout_2.addWidget(self.textExportNotes, 2, 1, 1, 1)
        self.horizontalLayout_10.addLayout(self.gridLayout_2)
        self.verticalLayout_4.addWidget(self.boxExportPattern)
        self.boxExportFileSettings = QtGui.QGroupBox(self.tabExport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boxExportFileSettings.sizePolicy().hasHeightForWidth())
        self.boxExportFileSettings.setSizePolicy(sizePolicy)
        self.boxExportFileSettings.setObjectName("boxExportFileSettings")
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.boxExportFileSettings)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.labelExtension = QtGui.QLabel(self.boxExportFileSettings)
        self.labelExtension.setObjectName("labelExtension")
        self.horizontalLayout_7.addWidget(self.labelExtension)
        self.editExportExtensions = QtGui.QLineEdit(self.boxExportFileSettings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editExportExtensions.sizePolicy().hasHeightForWidth())
        self.editExportExtensions.setSizePolicy(sizePolicy)
        self.editExportExtensions.setPlaceholderText("txt")
        self.editExportExtensions.setObjectName("editExportExtensions")
        self.horizontalLayout_7.addWidget(self.editExportExtensions)
        self.labelExportEncoding = QtGui.QLabel(self.boxExportFileSettings)
        self.labelExportEncoding.setObjectName("labelExportEncoding")
        self.horizontalLayout_7.addWidget(self.labelExportEncoding)
        self.cmbExportEncoding = QtGui.QComboBox(self.boxExportFileSettings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbExportEncoding.sizePolicy().hasHeightForWidth())
        self.cmbExportEncoding.setSizePolicy(sizePolicy)
        self.cmbExportEncoding.setObjectName("cmbExportEncoding")
        self.cmbExportEncoding.addItem("")
        self.cmbExportEncoding.addItem("")
        self.cmbExportEncoding.addItem("")
        self.horizontalLayout_7.addWidget(self.cmbExportEncoding)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_7)
        self.verticalLayout_4.addWidget(self.boxExportFileSettings)
        self.tabsSettings.addTab(self.tabExport, "")
        self.verticalLayout.addWidget(self.tabsSettings)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonWhatsThis = QtGui.QToolButton(settingsDialog)
        self.buttonWhatsThis.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.buttonWhatsThis.setAutoRaise(True)
        self.buttonWhatsThis.setObjectName("buttonWhatsThis")
        self.horizontalLayout.addWidget(self.buttonWhatsThis)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonOK = QtGui.QPushButton(settingsDialog)
        self.buttonOK.setObjectName("buttonOK")
        self.horizontalLayout.addWidget(self.buttonOK)
        self.buttonApply = QtGui.QPushButton(settingsDialog)
        self.buttonApply.setObjectName("buttonApply")
        self.horizontalLayout.addWidget(self.buttonApply)
        self.buttonCancel = QtGui.QPushButton(settingsDialog)
        self.buttonCancel.setObjectName("buttonCancel")
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(settingsDialog)
        self.tabsSettings.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonOK, QtCore.SIGNAL("clicked()"), settingsDialog.onButtonOK)
        QtCore.QObject.connect(self.buttonApply, QtCore.SIGNAL("clicked()"), settingsDialog.onButtonApply)
        QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL("clicked()"), settingsDialog.onButtonCancel)
        QtCore.QObject.connect(self.cmbImportPatternName, QtCore.SIGNAL("activated(QString)"), settingsDialog.onImportPatternActivated)
        QtCore.QObject.connect(self.buttonImportAddPattern, QtCore.SIGNAL("clicked()"), settingsDialog.onImportAddPattern)
        QtCore.QObject.connect(self.buttonImportDeletePattern, QtCore.SIGNAL("clicked()"), settingsDialog.onImportDeletePattern)
        QtCore.QObject.connect(self.textImportPattern, QtCore.SIGNAL("textChanged()"), settingsDialog.onImportPatternChanged)
        QtCore.QObject.connect(self.editImportDelimiter, QtCore.SIGNAL("textChanged(QString)"), settingsDialog.onImportDelimiterChanged)
        QtCore.QObject.connect(self.editImportExtension, QtCore.SIGNAL("textChanged(QString)"), settingsDialog.onImportExtensionChanged)
        QtCore.QObject.connect(self.cmbImportEncoding, QtCore.SIGNAL("activated(QString)"), settingsDialog.onImportEncodingChanged)
        QtCore.QObject.connect(self.editImportDateFormat, QtCore.SIGNAL("textChanged(QString)"), settingsDialog.onImportDateFormatChanged)
        QtCore.QObject.connect(self.cmbExportPatternName, QtCore.SIGNAL("activated(QString)"), settingsDialog.onExportPatternActivated)
        QtCore.QObject.connect(self.buttonExportAddPattern, QtCore.SIGNAL("clicked()"), settingsDialog.onExportAddPattern)
        QtCore.QObject.connect(self.buttonExportDeletePattern, QtCore.SIGNAL("clicked()"), settingsDialog.onExportDeletePattern)
        QtCore.QObject.connect(self.textExportHeader, QtCore.SIGNAL("textChanged()"), settingsDialog.onExportHeaderChanged)
        QtCore.QObject.connect(self.textExportBody, QtCore.SIGNAL("textChanged()"), settingsDialog.onExportBodyChanged)
        QtCore.QObject.connect(self.textExportNotes, QtCore.SIGNAL("textChanged()"), settingsDialog.onExportNotesChanged)
        QtCore.QObject.connect(self.textExportBottom, QtCore.SIGNAL("textChanged()"), settingsDialog.onExportBottomChanged)
        QtCore.QObject.connect(self.editExportDateFormat, QtCore.SIGNAL("textChanged(QString)"), settingsDialog.onExportDateFormatChanged)
        QtCore.QObject.connect(self.cmbExportEncoding, QtCore.SIGNAL("activated(QString)"), settingsDialog.onExportEncodingChanged)
        QtCore.QObject.connect(self.chbAttachNotes, QtCore.SIGNAL("toggled(bool)"), settingsDialog.onApplicationAttachNotesChanged)
        QtCore.QObject.connect(self.editExportExtensions, QtCore.SIGNAL("textChanged(QString)"), settingsDialog.onExportExtensionChanged)
        QtCore.QObject.connect(self.cmbNotesPosition, QtCore.SIGNAL("activated(QString)"), settingsDialog.onApplicationAttachNotesSettingsChanged)
        QtCore.QObject.connect(self.chbIsDefaultImport, QtCore.SIGNAL("toggled(bool)"), settingsDialog.onImportIsDefaultChanged)
        QtCore.QObject.connect(self.chbIsDefaultExport, QtCore.SIGNAL("toggled(bool)"), settingsDialog.onExportIsDefaultChanged)
        QtCore.QObject.connect(self.editHighlightLanguage, QtCore.SIGNAL("textChanged(QString)"), settingsDialog.onApplicationHighlightLanguageChanged)
        QtCore.QObject.connect(self.editNoteLanguge, QtCore.SIGNAL("textChanged(QString)"), settingsDialog.onApplicationNoteLanguageChanged)
        QtCore.QObject.connect(self.editBookmarkLanguage, QtCore.SIGNAL("textChanged(QString)"), settingsDialog.onApplicationBookmarkLanguageChanged)
        QtCore.QObject.connect(self.editRangeSeparator, QtCore.SIGNAL("textChanged(QString)"), settingsDialog.onApplicationRangeSeparatorChanged)
        QtCore.QObject.connect(self.cmbDateLanguage, QtCore.SIGNAL("currentIndexChanged(QString)"), settingsDialog.onApplicationDateLanguageChanged)
        QtCore.QMetaObject.connectSlotsByName(settingsDialog)
        settingsDialog.setTabOrder(self.chbAttachNotes, self.cmbNotesPosition)
        settingsDialog.setTabOrder(self.cmbNotesPosition, self.cmbDateLanguage)
        settingsDialog.setTabOrder(self.cmbDateLanguage, self.editRangeSeparator)
        settingsDialog.setTabOrder(self.editRangeSeparator, self.editHighlightLanguage)
        settingsDialog.setTabOrder(self.editHighlightLanguage, self.editNoteLanguge)
        settingsDialog.setTabOrder(self.editNoteLanguge, self.editBookmarkLanguage)
        settingsDialog.setTabOrder(self.editBookmarkLanguage, self.cmbImportPatternName)
        settingsDialog.setTabOrder(self.cmbImportPatternName, self.chbIsDefaultImport)
        settingsDialog.setTabOrder(self.chbIsDefaultImport, self.buttonImportAddPattern)
        settingsDialog.setTabOrder(self.buttonImportAddPattern, self.buttonImportDeletePattern)
        settingsDialog.setTabOrder(self.buttonImportDeletePattern, self.editImportDelimiter)
        settingsDialog.setTabOrder(self.editImportDelimiter, self.textImportPattern)
        settingsDialog.setTabOrder(self.textImportPattern, self.editImportDateFormat)
        settingsDialog.setTabOrder(self.editImportDateFormat, self.editImportExtension)
        settingsDialog.setTabOrder(self.editImportExtension, self.cmbImportEncoding)
        settingsDialog.setTabOrder(self.cmbImportEncoding, self.cmbExportPatternName)
        settingsDialog.setTabOrder(self.cmbExportPatternName, self.chbIsDefaultExport)
        settingsDialog.setTabOrder(self.chbIsDefaultExport, self.buttonExportAddPattern)
        settingsDialog.setTabOrder(self.buttonExportAddPattern, self.buttonExportDeletePattern)
        settingsDialog.setTabOrder(self.buttonExportDeletePattern, self.textExportHeader)
        settingsDialog.setTabOrder(self.textExportHeader, self.textExportBody)
        settingsDialog.setTabOrder(self.textExportBody, self.textExportNotes)
        settingsDialog.setTabOrder(self.textExportNotes, self.textExportBottom)
        settingsDialog.setTabOrder(self.textExportBottom, self.editExportDateFormat)
        settingsDialog.setTabOrder(self.editExportDateFormat, self.editExportExtensions)
        settingsDialog.setTabOrder(self.editExportExtensions, self.cmbExportEncoding)
        settingsDialog.setTabOrder(self.cmbExportEncoding, self.buttonOK)
        settingsDialog.setTabOrder(self.buttonOK, self.buttonApply)
        settingsDialog.setTabOrder(self.buttonApply, self.buttonCancel)
        settingsDialog.setTabOrder(self.buttonCancel, self.buttonWhatsThis)
        settingsDialog.setTabOrder(self.buttonWhatsThis, self.tabsSettings)

    def retranslateUi(self, settingsDialog):
        settingsDialog.setWindowTitle(QtGui.QApplication.translate("settingsDialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupNotesAttachments.setTitle(QtGui.QApplication.translate("settingsDialog", "Notes", None, QtGui.QApplication.UnicodeUTF8))
        self.chbAttachNotes.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Highlights and related notes are stored separately in \'My Clippings.txt\'. Check the box if you want to unify them in a one table row.", None, QtGui.QApplication.UnicodeUTF8))
        self.chbAttachNotes.setText(QtGui.QApplication.translate("settingsDialog", "Attach notes to highlights they are attributed to:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNotesPosition.setText(QtGui.QApplication.translate("settingsDialog", "Notes found:", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbNotesPosition.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Choose here where notes are found: before highlight, after highlights, or automatic search.", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbNotesPosition.setItemText(0, QtGui.QApplication.translate("settingsDialog", "Automatic (default)", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbNotesPosition.setItemText(1, QtGui.QApplication.translate("settingsDialog", "Before highlights", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbNotesPosition.setItemText(2, QtGui.QApplication.translate("settingsDialog", "After highlights", None, QtGui.QApplication.UnicodeUTF8))
        self.groupLanguage.setTitle(QtGui.QApplication.translate("settingsDialog", "Language", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDateLanguage.setText(QtGui.QApplication.translate("settingsDialog", "Date Interpreter", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbDateLanguage.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Language used to interpret dates.", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbDateLanguage.setItemText(0, QtGui.QApplication.translate("settingsDialog", "English (default)", None, QtGui.QApplication.UnicodeUTF8))
        self.editRangeSeparator.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Text used to separate two values in a page/location range.", None, QtGui.QApplication.UnicodeUTF8))
        self.editRangeSeparator.setPlaceholderText(QtGui.QApplication.translate("settingsDialog", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelHighlightLanguage.setText(QtGui.QApplication.translate("settingsDialog", "Highlight:", None, QtGui.QApplication.UnicodeUTF8))
        self.editHighlightLanguage.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Highlight in \'MyClippings.txt\' file language (e.g. Выделение)", None, QtGui.QApplication.UnicodeUTF8))
        self.editHighlightLanguage.setPlaceholderText(QtGui.QApplication.translate("settingsDialog", "Highlight", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNoteLanguge.setText(QtGui.QApplication.translate("settingsDialog", "Note:", None, QtGui.QApplication.UnicodeUTF8))
        self.editNoteLanguge.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Note in \'MyClippings.txt\' file language (e.g. Заметка)", None, QtGui.QApplication.UnicodeUTF8))
        self.editNoteLanguge.setPlaceholderText(QtGui.QApplication.translate("settingsDialog", "Note", None, QtGui.QApplication.UnicodeUTF8))
        self.labelBookmarkLanguage.setText(QtGui.QApplication.translate("settingsDialog", "Bookmark:", None, QtGui.QApplication.UnicodeUTF8))
        self.editBookmarkLanguage.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Bookmark in \'MyClippings.txt\' file language (e.g. Закладка)", None, QtGui.QApplication.UnicodeUTF8))
        self.editBookmarkLanguage.setPlaceholderText(QtGui.QApplication.translate("settingsDialog", "Bookmark", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRangeSeparator.setText(QtGui.QApplication.translate("settingsDialog", "Range Divider", None, QtGui.QApplication.UnicodeUTF8))
        self.tabsSettings.setTabText(self.tabsSettings.indexOf(self.tabApplication), QtGui.QApplication.translate("settingsDialog", "Application", None, QtGui.QApplication.UnicodeUTF8))
        self.labelImportPatternName.setText(QtGui.QApplication.translate("settingsDialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbImportPatternName.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Import</span><span style=\" font-size:8pt; font-weight:600;\"> pattern name</span><span style=\" font-size:8pt;\">, that will be shown in the Import button context menu.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.chbIsDefaultImport.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Make current import pattern default Import & Append buttons action", None, QtGui.QApplication.UnicodeUTF8))
        self.chbIsDefaultImport.setText(QtGui.QApplication.translate("settingsDialog", "Default", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonImportAddPattern.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Add new <span style=\" font-weight:600;\">import pattern</span>.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonImportAddPattern.setText(QtGui.QApplication.translate("settingsDialog", "Add...", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonImportDeletePattern.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Delete the active <span style=\" font-weight:600;\">import pattern</span>.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonImportDeletePattern.setText(QtGui.QApplication.translate("settingsDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.boxImportPattern.setTitle(QtGui.QApplication.translate("settingsDialog", "Notes pattern", None, QtGui.QApplication.UnicodeUTF8))
        self.labelImportDelimiter.setText(QtGui.QApplication.translate("settingsDialog", "Notes<br>delimiter:", None, QtGui.QApplication.UnicodeUTF8))
        self.editImportDelimiter.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Delimiter</span> is an array of characters used to divide notes in a file. If the field is empty, carrier return and line feed characters are used.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelImportPattern.setText(QtGui.QApplication.translate("settingsDialog", "Notes<br>pattern:", None, QtGui.QApplication.UnicodeUTF8))
        self.textImportPattern.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Notes pattern</span> is a regular expression used to divide notes into an array of named groups. Groups names must be the same as names of the Klippings table header: <span style=\" font-weight:600;\">(?P&lt;</span><span style=\" font-weight:600; font-style:italic;\">table_header_name</span><span style=\" font-weight:600;\">&gt;</span><span style=\" font-weight:600; font-style:italic;\">regular_expression</span><span style=\" font-weight:600;\">)</span>.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Patterns must be in <span style=\" font-weight:600;\">raw string notation</span>, <span style=\" font-weight:600;\">VERBOSE</span> and<span style=\" font-weight:600;\"> UNICODE</span> options are on. (<a href=\"http://docs.python.org/library/re.html\"><span style=\" text-decoration: underline; color:#0000ff;\">more</span></a>)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelImportDateFormat.setText(QtGui.QApplication.translate("settingsDialog", "Date<br>format:", None, QtGui.QApplication.UnicodeUTF8))
        self.editImportDateFormat.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Date and time forma</span><span style=\" font-size:8pt;\">t to convert a local languge string into a date. If the field is empty, &quot;My Clippings.txt\' date and time format &quot;dddd, MMMM dd, yyyy, hh:mm AP&quot; is used. If</span><span style=\" font-size:8pt; font-weight:600;\"> </span><span style=\" font-size:8pt;\">your OS local language is not English, and you want to use a custom import pattern for &quot;My Clippings.txt&quot; file, leave this field empty.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Date:</span></p></td>\n"
"<td></td></tr></table>\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">d</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the day as number without a leading zero (1 to 31)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">dd</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the day as number with a leading zero (01 to 31)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">ddd</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the abbreviated localized day name (e.g. \'Mon\' to \'Sun\') </span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">dddd</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the long localized day name (e.g. \'Monday\' )</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">M</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the month as number without a leading zero (1-12)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">MM</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the month as number with a leading zero (01-12)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">MMM</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the abbreviated localized month name (e.g. \'Jan\' to \'Dec\')</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">MMMM</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the long localized month name (e.g. \'January\' to \'December\')</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">yy</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the year as two digit number (00-99)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">yyyy</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the year as four digit number</span></p></td></tr></table>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Time</span></p></td>\n"
"<td></td></tr></table>\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">h</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the hour without a leading zero (0 to 23 or 1 to 12 if AM/PM display)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">hh</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the hour with a leading zero (00 to 23 or 01 to 12 if AM/PM display)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">m</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the minute without a leading zero (0 to 59)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">mm</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the minute with a leading zero (00 to 59)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">s</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the second without a leading zero (0 to 59)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">ss</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the second with a leading zero (00 to 59)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">z</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the milliseconds without leading zeroes (0 to 999)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">zzz</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the milliseconds with leading zeroes (000 to 999)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">AP</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">use AM/PM display. </span><span style=\" font-size:8pt; font-style:italic;\">AP</span><span style=\" font-size:8pt;\"> will be replaced by either &quot;AM&quot; or &quot;PM&quot;.</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">ap</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">use am/pm display. </span><span style=\" font-size:8pt; font-style:italic;\">ap</span><span style=\" font-size:8pt;\"> will be replaced by either &quot;am&quot; or &quot;pm&quot;.</span></p></td></tr></table></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.boxImportFileSettings.setTitle(QtGui.QApplication.translate("settingsDialog", "File settings", None, QtGui.QApplication.UnicodeUTF8))
        self.labelImportExtension.setText(QtGui.QApplication.translate("settingsDialog", "Extensions:", None, QtGui.QApplication.UnicodeUTF8))
        self.editImportExtension.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">File extensions</span> seprated by commas.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labeImportlEncoding.setText(QtGui.QApplication.translate("settingsDialog", "Encoding:", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbImportEncoding.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Source <span style=\" font-weight:600;\">file encoding.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabsSettings.setTabText(self.tabsSettings.indexOf(self.tabImport), QtGui.QApplication.translate("settingsDialog", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.labelExportPatternName.setText(QtGui.QApplication.translate("settingsDialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbExportPatternName.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Export</span><span style=\" font-size:8pt; font-weight:600;\"> pattern name</span><span style=\" font-size:8pt;\">, that will be shown in the Export button context menu.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.chbIsDefaultExport.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Make current export pattern default Export button action", None, QtGui.QApplication.UnicodeUTF8))
        self.chbIsDefaultExport.setText(QtGui.QApplication.translate("settingsDialog", "Default", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonExportAddPattern.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Add new </span><span style=\" font-size:8pt; font-weight:600;\">export</span><span style=\" font-size:8pt; font-weight:600;\"> pattern</span><span style=\" font-size:8pt;\">.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonExportAddPattern.setText(QtGui.QApplication.translate("settingsDialog", "Add...", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonExportDeletePattern.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Delete the active </span><span style=\" font-size:8pt; font-weight:600;\">export</span><span style=\" font-size:8pt; font-weight:600;\"> pattern</span><span style=\" font-size:8pt;\">.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonExportDeletePattern.setText(QtGui.QApplication.translate("settingsDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.boxExportPattern.setTitle(QtGui.QApplication.translate("settingsDialog", "Notes pattern", None, QtGui.QApplication.UnicodeUTF8))
        self.labelExportHeader.setText(QtGui.QApplication.translate("settingsDialog", "Header:", None, QtGui.QApplication.UnicodeUTF8))
        self.textExportHeader.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Header</span><span style=\" font-size:8pt;\"> is the data to write in the beginning of the export file.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelExportBody.setText(QtGui.QApplication.translate("settingsDialog", "Body:", None, QtGui.QApplication.UnicodeUTF8))
        self.textExportBody.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Body </span><span style=\" font-size:8pt;\">is a pattern to convert notes from the Klippings table into formated text. Wildcards </span><span style=\" font-size:8pt; font-weight:600;\">?P&lt;table_header_name&gt;</span><span style=\" font-size:8pt;\"> will be replaced by the edited, filtered and sorted table data.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelExportBottom.setText(QtGui.QApplication.translate("settingsDialog", "Bottom:", None, QtGui.QApplication.UnicodeUTF8))
        self.textExportBottom.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Bottom</span><span style=\" font-size:8pt;\"> is the data to append to the ending of the export file.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelExportDateFormat.setText(QtGui.QApplication.translate("settingsDialog", "Date<br>format:", None, QtGui.QApplication.UnicodeUTF8))
        self.editExportDateFormat.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Date and time forma</span><span style=\" font-size:8pt;\">t to convert a note date into a local language string.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Date:</span></p></td>\n"
"<td></td></tr></table>\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">d</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the day as number without a leading zero (1 to 31)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">dd</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the day as number with a leading zero (01 to 31)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">ddd</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the abbreviated localized day name (e.g. \'Mon\' to \'Sun\') </span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">dddd</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the long localized day name (e.g. \'Monday\' )</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">M</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the month as number without a leading zero (1-12)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">MM</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the month as number with a leading zero (01-12)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">MMM</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the abbreviated localized month name (e.g. \'Jan\' to \'Dec\')</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">MMMM</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the long localized month name (e.g. \'January\' to \'December\')</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">yy</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the year as two digit number (00-99)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">yyyy</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the year as four digit number</span></p></td></tr></table>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Time</span></p></td>\n"
"<td></td></tr></table>\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">h</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the hour without a leading zero (0 to 23 or 1 to 12 if AM/PM display)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">hh</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the hour with a leading zero (00 to 23 or 01 to 12 if AM/PM display)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">m</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the minute without a leading zero (0 to 59)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">mm</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the minute with a leading zero (00 to 59)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">s</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the second without a leading zero (0 to 59)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">ss</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the second with a leading zero (00 to 59)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">z</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the milliseconds without leading zeroes (0 to 999)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">zzz</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the milliseconds with leading zeroes (000 to 999)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">AP</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">use AM/PM display. </span><span style=\" font-size:8pt; font-style:italic;\">AP</span><span style=\" font-size:8pt;\"> will be replaced by either &quot;AM&quot; or &quot;PM&quot;.</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">ap</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">use am/pm display. </span><span style=\" font-size:8pt; font-style:italic;\">ap</span><span style=\" font-size:8pt;\"> will be replaced by either &quot;am&quot; or &quot;pm&quot;.</span></p></td></tr></table></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelExportNotes.setText(QtGui.QApplication.translate("settingsDialog", "Note\n"
"Pattern:", None, QtGui.QApplication.UnicodeUTF8))
        self.textExportNotes.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Body </span><span style=\" font-size:8pt;\">is a pattern to convert notes from the Klippings table into formated text. Wildcards </span><span style=\" font-size:8pt; font-weight:600;\">?P&lt;table_header_name&gt;</span><span style=\" font-size:8pt;\"> will be replaced by the edited, filtered and sorted table data.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.boxExportFileSettings.setTitle(QtGui.QApplication.translate("settingsDialog", "File settings", None, QtGui.QApplication.UnicodeUTF8))
        self.labelExtension.setText(QtGui.QApplication.translate("settingsDialog", "Extensions:", None, QtGui.QApplication.UnicodeUTF8))
        self.editExportExtensions.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">File extensions</span><span style=\" font-size:8pt;\"> seprated by commas.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelExportEncoding.setText(QtGui.QApplication.translate("settingsDialog", "Encoding:", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbExportEncoding.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Export <span style=\" font-weight:600;\">file encoding</span>.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbExportEncoding.setItemText(0, QtGui.QApplication.translate("settingsDialog", "UTF-8 (all languages)", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbExportEncoding.setItemText(1, QtGui.QApplication.translate("settingsDialog", "UTF-16 (all languages)", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbExportEncoding.setItemText(2, QtGui.QApplication.translate("settingsDialog", "UTF-32 (all languages)", None, QtGui.QApplication.UnicodeUTF8))
        self.tabsSettings.setTabText(self.tabsSettings.indexOf(self.tabExport), QtGui.QApplication.translate("settingsDialog", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonOK.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Save settings and close the window.", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonOK.setText(QtGui.QApplication.translate("settingsDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonApply.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Save settings.", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonApply.setText(QtGui.QApplication.translate("settingsDialog", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setWhatsThis(QtGui.QApplication.translate("settingsDialog", "Close the window and do not save settings.", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setText(QtGui.QApplication.translate("settingsDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

import mainWin_rc
