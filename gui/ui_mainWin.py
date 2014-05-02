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


# Form implementation generated from reading ui file 'D:\Kindle\gui\mainWin.ui'
#
# Created: Mon Jun 20 20:21:58 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_mainWin(object):
    def setupUi(self, mainWin):
        mainWin.setObjectName(_fromUtf8("mainWin"))
        mainWin.resize(1000, 600)
        mainWin.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWin.setWindowIcon(icon)
        mainWin.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        mainWin.setIconSize(QtCore.QSize(48, 48))
        mainWin.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralWidget = QtGui.QWidget(mainWin)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setMargin(1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.toolButtonImport = QtGui.QToolButton(self.centralWidget)
        self.toolButtonImport.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonImport.setIcon(icon1)
        self.toolButtonImport.setIconSize(QtCore.QSize(36, 36))
        self.toolButtonImport.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.toolButtonImport.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButtonImport.setAutoRaise(True)
        self.toolButtonImport.setObjectName(_fromUtf8("toolButtonImport"))
        self.verticalLayout.addWidget(self.toolButtonImport)
        self.toolButtonAppend = QtGui.QToolButton(self.centralWidget)
        self.toolButtonAppend.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/addfile.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonAppend.setIcon(icon2)
        self.toolButtonAppend.setIconSize(QtCore.QSize(36, 36))
        self.toolButtonAppend.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.toolButtonAppend.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButtonAppend.setAutoRaise(True)
        self.toolButtonAppend.setObjectName(_fromUtf8("toolButtonAppend"))
        self.verticalLayout.addWidget(self.toolButtonAppend)
        self.toolButtonExport = QtGui.QToolButton(self.centralWidget)
        self.toolButtonExport.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/foldermove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonExport.setIcon(icon3)
        self.toolButtonExport.setIconSize(QtCore.QSize(36, 35))
        self.toolButtonExport.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.toolButtonExport.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButtonExport.setAutoRaise(True)
        self.toolButtonExport.setObjectName(_fromUtf8("toolButtonExport"))
        self.verticalLayout.addWidget(self.toolButtonExport)
        self.tableView = QtGui.QTableView(self.centralWidget)
        self.tableView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableView.setFrameShape(QtGui.QFrame.StyledPanel)
        self.tableView.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setShowGrid(True)
        self.tableView.setGridStyle(QtCore.Qt.NoPen)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.horizontalHeader().setDefaultSectionSize(120)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setDefaultSectionSize(40)
        self.verticalLayout.addWidget(self.tableView)
        self.filterLayout = QtGui.QGridLayout()
        self.filterLayout.setSpacing(6)
        self.filterLayout.setObjectName(_fromUtf8("filterLayout"))
        self.filterEdit = QtGui.QLineEdit(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterEdit.sizePolicy().hasHeightForWidth())
        self.filterEdit.setSizePolicy(sizePolicy)
        self.filterEdit.setStyleSheet(_fromUtf8(""))
        self.filterEdit.setObjectName(_fromUtf8("filterEdit"))
        self.filterLayout.addWidget(self.filterEdit, 0, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.filterLayout.addItem(spacerItem, 0, 7, 1, 1)
        self.filterCloseButton = QtGui.QToolButton(self.centralWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.filterCloseButton.setIcon(icon4)
        self.filterCloseButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.filterCloseButton.setAutoRaise(True)
        self.filterCloseButton.setObjectName(_fromUtf8("filterCloseButton"))
        self.filterLayout.addWidget(self.filterCloseButton, 0, 1, 1, 1)
        self.filterCaseBox = QtGui.QCheckBox(self.centralWidget)
        self.filterCaseBox.setObjectName(_fromUtf8("filterCaseBox"))
        self.filterLayout.addWidget(self.filterCaseBox, 0, 4, 1, 1)
        self.filterOptionButton = QtGui.QToolButton(self.centralWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/find1.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.filterOptionButton.setIcon(icon5)
        self.filterOptionButton.setIconSize(QtCore.QSize(16, 16))
        self.filterOptionButton.setCheckable(True)
        self.filterOptionButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.filterOptionButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.filterOptionButton.setAutoRaise(True)
        self.filterOptionButton.setArrowType(QtCore.Qt.NoArrow)
        self.filterOptionButton.setObjectName(_fromUtf8("filterOptionButton"))
        self.filterLayout.addWidget(self.filterOptionButton, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(5, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.filterLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.filterLayout)
        self.filterLine = QtGui.QFrame(self.centralWidget)
        self.filterLine.setFrameShape(QtGui.QFrame.HLine)
        self.filterLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.filterLine.setObjectName(_fromUtf8("filterLine"))
        self.verticalLayout.addWidget(self.filterLine)
        self.rowIndicator = QtGui.QLabel(self.centralWidget)
        self.rowIndicator.setFrameShape(QtGui.QFrame.StyledPanel)
        self.rowIndicator.setFrameShadow(QtGui.QFrame.Sunken)
        self.rowIndicator.setAlignment(QtCore.Qt.AlignCenter)
        self.rowIndicator.setObjectName(_fromUtf8("rowIndicator"))
        self.verticalLayout.addWidget(self.rowIndicator)
        mainWin.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(mainWin)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 633, 20))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menu_Help = QtGui.QMenu(self.menuBar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        mainWin.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(mainWin)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        mainWin.setStatusBar(self.statusBar)
        self.toolBar = QtGui.QToolBar(mainWin)
        self.toolBar.setEnabled(True)
        self.toolBar.setIconSize(QtCore.QSize(36, 36))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        mainWin.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionImport = QtGui.QAction(mainWin)
        self.actionImport.setIcon(icon1)
        self.actionImport.setObjectName(_fromUtf8("actionImport"))
        self.actionExit = QtGui.QAction(mainWin)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon6)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionAbout = QtGui.QAction(mainWin)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/infoabout.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon7)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionExport = QtGui.QAction(mainWin)
        self.actionExport.setIcon(icon3)
        self.actionExport.setObjectName(_fromUtf8("actionExport"))
        self.actionFilter = QtGui.QAction(mainWin)
        self.actionFilter.setIcon(icon5)
        self.actionFilter.setObjectName(_fromUtf8("actionFilter"))
        self.actionAppend = QtGui.QAction(mainWin)
        self.actionAppend.setIcon(icon2)
        self.actionAppend.setObjectName(_fromUtf8("actionAppend"))
        self.actionHelp = QtGui.QAction(mainWin)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/help.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(icon8)
        self.actionHelp.setObjectName(_fromUtf8("actionHelp"))
        self.actionSettings = QtGui.QAction(mainWin)
        self.actionSettings.setEnabled(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/configure.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon9)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionDeleteRow = QtGui.QAction(mainWin)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/cut.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDeleteRow.setIcon(icon10)
        self.actionDeleteRow.setObjectName(_fromUtf8("actionDeleteRow"))
        self.actionResizeRowsToContents = QtGui.QAction(mainWin)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Bloomy/textfile.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionResizeRowsToContents.setIcon(icon11)
        self.actionResizeRowsToContents.setObjectName(_fromUtf8("actionResizeRowsToContents"))
        self.actionResizeRows = QtGui.QAction(mainWin)
        self.actionResizeRows.setObjectName(_fromUtf8("actionResizeRows"))
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionAppend)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionFilter)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionHelp)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.actionFilter)
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionHelp)
        self.toolBar.addAction(self.actionAbout)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(mainWin)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWin.close)
        QtCore.QObject.connect(self.actionImport, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWin.onImport)
        QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWin.onAbout)
        QtCore.QObject.connect(self.actionExport, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWin.onExport)
        QtCore.QObject.connect(self.actionFilter, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWin.onFilter)
        QtCore.QObject.connect(self.filterEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), mainWin.onFilterInput)
        QtCore.QObject.connect(self.filterCloseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), mainWin.onFilter)
        QtCore.QObject.connect(self.actionAppend, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWin.onImport)
        QtCore.QObject.connect(self.filterCaseBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")),
                               mainWin.onFilterCaseState)
        QtCore.QObject.connect(self.actionHelp, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWin.onHelp)
        QtCore.QObject.connect(self.actionSettings, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWin.onSettings)
        QtCore.QObject.connect(self.toolButtonImport, QtCore.SIGNAL(_fromUtf8("clicked()")), self.actionImport.trigger)
        QtCore.QObject.connect(self.toolButtonExport, QtCore.SIGNAL(_fromUtf8("clicked()")), self.actionExport.trigger)
        QtCore.QObject.connect(self.toolButtonAppend, QtCore.SIGNAL(_fromUtf8("clicked()")), self.actionAppend.trigger)
        QtCore.QObject.connect(self.actionDeleteRow, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWin.onDeleteRow)
        QtCore.QObject.connect(self.actionResizeRowsToContents, QtCore.SIGNAL(_fromUtf8("triggered()")),
                               mainWin.onResizeRowsToContents)
        QtCore.QObject.connect(self.actionResizeRows, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWin.onResizeRows)
        QtCore.QMetaObject.connectSlotsByName(mainWin)
        mainWin.setTabOrder(self.tableView, self.filterCloseButton)
        mainWin.setTabOrder(self.filterCloseButton, self.filterOptionButton)
        mainWin.setTabOrder(self.filterOptionButton, self.filterEdit)
        mainWin.setTabOrder(self.filterEdit, self.filterCaseBox)

    def retranslateUi(self, mainWin):
        mainWin.setWindowTitle(
            QtGui.QApplication.translate("mainWin", "DaleyKlippings", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButtonImport.setToolTip(
            QtGui.QApplication.translate("mainWin", "Import notes", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButtonImport.setStatusTip(
            QtGui.QApplication.translate("mainWin", "Import...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButtonImport.setText(
            QtGui.QApplication.translate("mainWin", "&Import", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButtonAppend.setToolTip(
            QtGui.QApplication.translate("mainWin", "Append highlights, notes, and bookmarks", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.toolButtonAppend.setStatusTip(
            QtGui.QApplication.translate("mainWin", "Append...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButtonAppend.setText(
            QtGui.QApplication.translate("mainWin", "&Append", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButtonExport.setToolTip(
            QtGui.QApplication.translate("mainWin", "Export notes", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButtonExport.setStatusTip(
            QtGui.QApplication.translate("mainWin", "Export...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButtonExport.setText(
            QtGui.QApplication.translate("mainWin", "&Export", None, QtGui.QApplication.UnicodeUTF8))
        self.filterEdit.setPlaceholderText(
            QtGui.QApplication.translate("mainWin", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.filterCloseButton.setText(
            QtGui.QApplication.translate("mainWin", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.filterCaseBox.setText(
            QtGui.QApplication.translate("mainWin", "Case &sensitive", None, QtGui.QApplication.UnicodeUTF8))
        self.filterOptionButton.setText(
            QtGui.QApplication.translate("mainWin", "▼", None, QtGui.QApplication.UnicodeUTF8))
        self.rowIndicator.setText(
            QtGui.QApplication.translate("mainWin", "Rows: 0/0", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("mainWin", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("mainWin", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(
            QtGui.QApplication.translate("mainWin", "Show tool bar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setText(
            QtGui.QApplication.translate("mainWin", "&Import...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setToolTip(
            QtGui.QApplication.translate("mainWin", "Import highlights, notes, and bookmarks", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setStatusTip(
            QtGui.QApplication.translate("mainWin", "Load clippings...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setShortcut(
            QtGui.QApplication.translate("mainWin", "Ctrl+I", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("mainWin", "E&xit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setToolTip(
            QtGui.QApplication.translate("mainWin", "Close application", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setStatusTip(
            QtGui.QApplication.translate("mainWin", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(
            QtGui.QApplication.translate("mainWin", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("mainWin", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setToolTip(
            QtGui.QApplication.translate("mainWin", "Info about DaleyKlippings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setStatusTip(
            QtGui.QApplication.translate("mainWin", "About DaleyKlippings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setText(
            QtGui.QApplication.translate("mainWin", "&Export...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setToolTip(
            QtGui.QApplication.translate("mainWin", "Export edited highlights, notes, and bookmarks", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setStatusTip(
            QtGui.QApplication.translate("mainWin", "Export notes...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setShortcut(
            QtGui.QApplication.translate("mainWin", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFilter.setText(
            QtGui.QApplication.translate("mainWin", "&Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFilter.setToolTip(
            QtGui.QApplication.translate("mainWin", "Filter the table", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFilter.setStatusTip(
            QtGui.QApplication.translate("mainWin", "Filter...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFilter.setShortcut(
            QtGui.QApplication.translate("mainWin", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAppend.setText(
            QtGui.QApplication.translate("mainWin", "&Append...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAppend.setToolTip(
            QtGui.QApplication.translate("mainWin", "Append current list of hilghlights, notes, and bookmarks", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.actionAppend.setStatusTip(
            QtGui.QApplication.translate("mainWin", "Append clippings...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAppend.setShortcut(
            QtGui.QApplication.translate("mainWin", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("mainWin", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setIconText(
            QtGui.QApplication.translate("mainWin", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setToolTip(QtGui.QApplication.translate("mainWin", "Open help webpage in your brouser", None,
                                                                QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setStatusTip(
            QtGui.QApplication.translate("mainWin", "Help webpage...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setShortcut(
            QtGui.QApplication.translate("mainWin", "Ctrl+H", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(
            QtGui.QApplication.translate("mainWin", "&Settings...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setToolTip(
            QtGui.QApplication.translate("mainWin", "Configure settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setStatusTip(
            QtGui.QApplication.translate("mainWin", "Settings...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setShortcut(
            QtGui.QApplication.translate("mainWin", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteRow.setText(
            QtGui.QApplication.translate("mainWin", "&Delete selected rows", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteRow.setShortcut(
            QtGui.QApplication.translate("mainWin", "Del", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResizeRowsToContents.setText(
            QtGui.QApplication.translate("mainWin", "&Resize rows to contents", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResizeRowsToContents.setShortcut(
            QtGui.QApplication.translate("mainWin", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResizeRows.setText(
            QtGui.QApplication.translate("mainWin", "Re&size rows...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResizeRows.setShortcut(
            QtGui.QApplication.translate("mainWin", "Ctrl+Alt+R", None, QtGui.QApplication.UnicodeUTF8))


import mainWin_rc
