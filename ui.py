# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_test.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QLocale,
                            QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QFormLayout, QGridLayout, QHBoxLayout,
                               QLabel, QLayout, QLineEdit, QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
                               QTextBrowser, QWidget)

import hexviewer
import utilviewer


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1070, 670)
        MainWindow.setMinimumSize(QSize(1070, 670))
        font = QFont()
        font.setFamilies([u"Courier New"])
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(0, 0))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_2 = QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(7)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.hexEditBtn = QPushButton(self.tab)
        self.hexEditBtn.setObjectName(u"hexEditBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hexEditBtn.sizePolicy().hasHeightForWidth())
        self.hexEditBtn.setSizePolicy(sizePolicy)
        self.hexEditBtn.setMinimumSize(QSize(0, 0))
        self.hexEditBtn.setMaximumSize(QSize(65, 16777215))

        self.horizontalLayout_4.addWidget(self.hexEditBtn)

        self.hexEditDoneBtn = QPushButton(self.tab)
        self.hexEditDoneBtn.setObjectName(u"hexEditDoneBtn")
        sizePolicy.setHeightForWidth(self.hexEditDoneBtn.sizePolicy().hasHeightForWidth())
        self.hexEditDoneBtn.setSizePolicy(sizePolicy)
        self.hexEditDoneBtn.setMinimumSize(QSize(65, 0))
        self.hexEditDoneBtn.setMaximumSize(QSize(65, 16777215))

        self.horizontalLayout_4.addWidget(self.hexEditDoneBtn)

        self.refreshBtn = QPushButton(self.tab)
        self.refreshBtn.setObjectName(u"refreshBtn")
        self.refreshBtn.setMaximumSize(QSize(30, 30))
        font1 = QFont()
        font1.setFamilies([u"Courier New"])
        font1.setPointSize(25)
        font1.setKerning(False)
        self.refreshBtn.setFont(font1)
        self.refreshBtn.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.refreshBtn)

        self.moveBackwardBtn = QPushButton(self.tab)
        self.moveBackwardBtn.setObjectName(u"moveBackwardBtn")
        self.moveBackwardBtn.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_4.addWidget(self.moveBackwardBtn)

        self.moveForwardBtn = QPushButton(self.tab)
        self.moveForwardBtn.setObjectName(u"moveForwardBtn")
        self.moveForwardBtn.setEnabled(True)
        sizePolicy.setHeightForWidth(self.moveForwardBtn.sizePolicy().hasHeightForWidth())
        self.moveForwardBtn.setSizePolicy(sizePolicy)
        self.moveForwardBtn.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_4.addWidget(self.moveForwardBtn)

        self.disassemBtn = QPushButton(self.tab)
        self.disassemBtn.setObjectName(u"disassemBtn")
        sizePolicy.setHeightForWidth(self.disassemBtn.sizePolicy().hasHeightForWidth())
        self.disassemBtn.setSizePolicy(sizePolicy)
        self.disassemBtn.setMinimumSize(QSize(65, 0))
        self.disassemBtn.setMaximumSize(QSize(65, 16777215))

        self.horizontalLayout_4.addWidget(self.disassemBtn)

        self.historyBtn = QPushButton(self.tab)
        self.historyBtn.setObjectName(u"historyBtn")
        sizePolicy.setHeightForWidth(self.historyBtn.sizePolicy().hasHeightForWidth())
        self.historyBtn.setSizePolicy(sizePolicy)
        self.historyBtn.setMinimumSize(QSize(65, 0))
        self.historyBtn.setMaximumSize(QSize(65, 16777215))

        self.horizontalLayout_4.addWidget(self.historyBtn)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.addrInput = QLineEdit(self.tab)
        self.addrInput.setObjectName(u"addrInput")
        sizePolicy.setHeightForWidth(self.addrInput.sizePolicy().hasHeightForWidth())
        self.addrInput.setSizePolicy(sizePolicy)
        self.addrInput.setMinimumSize(QSize(0, 25))
        self.addrInput.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_2.addWidget(self.addrInput)

        self.addrBtn = QPushButton(self.tab)
        self.addrBtn.setObjectName(u"addrBtn")
        self.addrBtn.setMinimumSize(QSize(0, 31))
        self.addrBtn.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.addrBtn)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 8, 2, 1, 2)

        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setMaximumSize(QSize(16777215, 10))

        self.gridLayout_2.addWidget(self.label_2, 7, 2, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.attachBtn = QPushButton(self.tab)
        self.attachBtn.setObjectName(u"attachBtn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.attachBtn.sizePolicy().hasHeightForWidth())
        self.attachBtn.setSizePolicy(sizePolicy2)
        self.attachBtn.setMinimumSize(QSize(110, 0))
        self.attachBtn.setFocusPolicy(Qt.TabFocus)

        self.horizontalLayout_3.addWidget(self.attachBtn)

        self.detachBtn = QPushButton(self.tab)
        self.detachBtn.setObjectName(u"detachBtn")
        sizePolicy2.setHeightForWidth(self.detachBtn.sizePolicy().hasHeightForWidth())
        self.detachBtn.setSizePolicy(sizePolicy2)
        self.detachBtn.setMinimumSize(QSize(110, 0))

        self.horizontalLayout_3.addWidget(self.detachBtn)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 4, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
#ifndef Q_OS_MAC
        self.horizontalLayout.setSpacing(-1)
#endif
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.offsetInput = QLineEdit(self.tab)
        self.offsetInput.setObjectName(u"offsetInput")
        sizePolicy.setHeightForWidth(self.offsetInput.sizePolicy().hasHeightForWidth())
        self.offsetInput.setSizePolicy(sizePolicy)
        self.offsetInput.setMinimumSize(QSize(0, 25))
        self.offsetInput.setMaximumSize(QSize(16777215, 16777215))
        self.offsetInput.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.horizontalLayout.addWidget(self.offsetInput)

        self.offsetOkbtn = QPushButton(self.tab)
        self.offsetOkbtn.setObjectName(u"offsetOkbtn")
        self.offsetOkbtn.setMinimumSize(QSize(0, 31))
        self.offsetOkbtn.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.offsetOkbtn)


        self.gridLayout_2.addLayout(self.horizontalLayout, 6, 2, 1, 2)

        # self.hexViewer = QTextEdit(self.tab)
        self.hexViewer = hexviewer.HexViewerClass(self.tab)
        self.hexViewer.setObjectName(u"hexViewer")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(2)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.hexViewer.sizePolicy().hasHeightForWidth())
        self.hexViewer.setSizePolicy(sizePolicy3)
        self.hexViewer.setMinimumSize(QSize(685, 0))
        self.hexViewer.setMaximumSize(QSize(16777215, 16777215))
        self.hexViewer.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.hexViewer.setInputMethodHints(Qt.ImhMultiLine)
        self.hexViewer.setReadOnly(True)
        self.hexViewer.setOverwriteMode(True)
        self.hexViewer.setAcceptRichText(True)
        # self.hexViewer.setTextInteractionFlags(Qt.NoTextInteraction)

        self.gridLayout_2.addWidget(self.hexViewer, 4, 0, 16, 2)

        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy4)
        self.label_3.setScaledContents(False)
        self.label_3.setWordWrap(False)
        self.label_3.setMargin(0)
        self.label_3.setIndent(21)

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 2)

        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMaximumSize(QSize(16777215, 10))

        self.gridLayout_2.addWidget(self.label, 5, 2, 1, 1)

        self.tabWidget2 = QTabWidget(self.tab)
        self.tabWidget2.setObjectName(u"tabWidget2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.tabWidget2.sizePolicy().hasHeightForWidth())
        self.tabWidget2.setSizePolicy(sizePolicy5)
        self.tabWidget2.setMinimumSize(QSize(295, 0))
        self.tabWidget2.setMaximumSize(QSize(16777215, 16777215))
        self.tabWidget2.setFocusPolicy(Qt.NoFocus)
        self.tabWidget2.setLayoutDirection(Qt.LeftToRight)
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.formLayout = QFormLayout(self.tab_3)
        self.formLayout.setObjectName(u"formLayout")
        self.label_8 = QLabel(self.tab_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(55, 0))

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_8)

        self.status_kernel_slide = QTextBrowser(self.tab_3)
        self.status_kernel_slide.setObjectName(u"status_kernel_slide")
        self.status_kernel_slide.setMaximumSize(QSize(16777215, 25))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.status_kernel_slide)

        self.label_7 = QLabel(self.tab_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(55, 0))

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_7)

        self.status_kernel_base = QTextBrowser(self.tab_3)
        self.status_kernel_base.setObjectName(u"status_kernel_base")
        self.status_kernel_base.setMaximumSize(QSize(16777215, 25))

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.status_kernel_base)

        self.label_6 = QLabel(self.tab_3)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.status_current_kaddr = QTextBrowser(self.tab_3)
        self.status_current_kaddr.setObjectName(u"status_current_kaddr")
        self.status_current_kaddr.setMinimumSize(QSize(0, 0))
        self.status_current_kaddr.setMaximumSize(QSize(16777215, 25))

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.status_current_kaddr)

        self.label_9 = QLabel(self.tab_3)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_9)

        self.status_current_addr = QTextBrowser(self.tab_3)
        self.status_current_addr.setObjectName(u"status_current_addr")
        self.status_current_addr.setMinimumSize(QSize(0, 0))
        self.status_current_addr.setMaximumSize(QSize(16777215, 25))

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.status_current_addr)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(5, QFormLayout.FieldRole, self.verticalSpacer_2)

        self.status_kernel_version = QTextBrowser(self.tab_3)
        self.status_kernel_version.setObjectName(u"status_kernel_version")
        self.status_kernel_version.setMinimumSize(QSize(0, 50))
        self.status_kernel_version.setMaximumSize(QSize(16777215, 25))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.status_kernel_version)

        self.label_10 = QLabel(self.tab_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(55, 0))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_10)

        self.tabWidget2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_4 = QGridLayout(self.tab_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.offsetsViewer = QTextBrowser(self.tab_4)
        self.offsetsViewer.setObjectName(u"offsetsViewer")
        self.offsetsViewer.setMinimumSize(QSize(0, 0))

        self.gridLayout_4.addWidget(self.offsetsViewer, 0, 0, 1, 2)

        self.offsetFilter = QLineEdit(self.tab_4)
        self.offsetFilter.setObjectName(u"offsetFilter")

        self.gridLayout_4.addWidget(self.offsetFilter, 1, 0, 1, 2)

        self.tabWidget2.addTab(self.tab_4, "")

        self.gridLayout_2.addWidget(self.tabWidget2, 9, 2, 11, 2)

        self.tabWidget.addTab(self.tab, "")
        self.label.raise_()
        self.tabWidget2.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.hexViewer.raise_()
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_7 = QGridLayout(self.tab_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.utilTabWidget = QTabWidget(self.tab_2)
        self.utilTabWidget.setObjectName(u"utilTabWidget")
        sizePolicy5.setHeightForWidth(self.utilTabWidget.sizePolicy().hasHeightForWidth())
        self.utilTabWidget.setSizePolicy(sizePolicy5)
        self.utilTabWidget.setMinimumSize(QSize(295, 0))
        self.utilTabWidget.setMaximumSize(QSize(16777215, 16777215))
        self.utilTabWidget.setFocusPolicy(Qt.NoFocus)
        self.utilTabWidget.setLayoutDirection(Qt.LeftToRight)
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_8 = QGridLayout(self.tab_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.getVnodeAtPathBtn = QPushButton(self.tab_6)
        self.getVnodeAtPathBtn.setObjectName(u"getVnodeAtPathBtn")

        self.gridLayout_8.addWidget(self.getVnodeAtPathBtn, 8, 1, 1, 1)

        self.utilViewerFilter = QLineEdit(self.tab_6)
        self.utilViewerFilter.setObjectName(u"utilViewerFilter")

        self.gridLayout_8.addWidget(self.utilViewerFilter, 11, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer, 10, 0, 1, 1)

        self.getAllProcLabel = QLabel(self.tab_6)
        self.getAllProcLabel.setObjectName(u"getAllProcLabel")
        self.getAllProcLabel.setMaximumSize(QSize(16777215, 15))

        self.gridLayout_8.addWidget(self.getAllProcLabel, 3, 0, 1, 1)

        self.getAllProcBtn = QPushButton(self.tab_6)
        self.getAllProcBtn.setObjectName(u"getAllProcBtn")

        self.gridLayout_8.addWidget(self.getAllProcBtn, 3, 1, 1, 1)

        self.getVnodeAtPathInput = QLineEdit(self.tab_6)
        self.getVnodeAtPathInput.setObjectName(u"getVnodeAtPathInput")

        self.gridLayout_8.addWidget(self.getVnodeAtPathInput, 8, 0, 1, 1)

        self.getPidListBtn = QPushButton(self.tab_6)
        self.getPidListBtn.setObjectName(u"getPidListBtn")

        self.gridLayout_8.addWidget(self.getPidListBtn, 1, 1, 1, 1)

        self.getVnodeAtPathLabel = QLabel(self.tab_6)
        self.getVnodeAtPathLabel.setObjectName(u"getVnodeAtPathLabel")
        self.getVnodeAtPathLabel.setMaximumSize(QSize(16777215, 40))

        self.gridLayout_8.addWidget(self.getVnodeAtPathLabel, 6, 0, 1, 1)

        self.getKfdBtn = QPushButton(self.tab_6)
        self.getKfdBtn.setObjectName(u"getKfdBtn")

        self.gridLayout_8.addWidget(self.getKfdBtn, 0, 1, 1, 1)

        self.getPidListLabel = QLabel(self.tab_6)
        self.getPidListLabel.setObjectName(u"getPidListLabel")
        self.getPidListLabel.setMaximumSize(QSize(16777215, 15))

        self.gridLayout_8.addWidget(self.getPidListLabel, 1, 0, 1, 1)

        self.getKfdLabel = QLabel(self.tab_6)
        self.getKfdLabel.setObjectName(u"getKfdLabel")
        self.getKfdLabel.setMaximumSize(QSize(16777215, 15))

        self.gridLayout_8.addWidget(self.getKfdLabel, 0, 0, 1, 1)

        self.utilTabWidget.addTab(self.tab_6, "")

        self.gridLayout_7.addWidget(self.utilTabWidget, 0, 1, 1, 1)

        # self.utilViewer = QTextEdit(self.tab_2)
        self.utilViewer = utilviewer.UtilViewerClass(self.tab_2)
        self.utilViewer.setObjectName(u"utilViewer")
        sizePolicy3.setHeightForWidth(self.utilViewer.sizePolicy().hasHeightForWidth())
        self.utilViewer.setSizePolicy(sizePolicy3)
        self.utilViewer.setMinimumSize(QSize(630, 0))
        self.utilViewer.setMaximumSize(QSize(16777215, 16777215))
        self.utilViewer.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.utilViewer.setInputMethodHints(Qt.ImhMultiLine)
        self.utilViewer.setReadOnly(True)
        self.utilViewer.setOverwriteMode(True)
        self.utilViewer.setAcceptRichText(True)
        # self.utilViewer.setTextInteractionFlags(Qt.NoTextInteraction)

        self.gridLayout_7.addWidget(self.utilViewer, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget2.setCurrentIndex(0)
        self.utilTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"kfd-explorer", None))
        self.hexEditBtn.setText(QCoreApplication.translate("MainWindow", u"kwrite", None))
        self.hexEditDoneBtn.setText(QCoreApplication.translate("MainWindow", u"Done", None))
#if QT_CONFIG(whatsthis)
        self.refreshBtn.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.refreshBtn.setText(QCoreApplication.translate("MainWindow", u"\u21bb", None))
#if QT_CONFIG(whatsthis)
        self.moveBackwardBtn.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.moveBackwardBtn.setText(QCoreApplication.translate("MainWindow", u"\u25c0", None))
        self.moveForwardBtn.setText(QCoreApplication.translate("MainWindow", u"\u25b6", None))
        self.disassemBtn.setText(QCoreApplication.translate("MainWindow", u"Disasm", None))
        self.historyBtn.setText(QCoreApplication.translate("MainWindow", u"History", None))
        self.addrBtn.setText(QCoreApplication.translate("MainWindow", u"GO", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Address", None))
        self.attachBtn.setText(QCoreApplication.translate("MainWindow", u"Attach", None))
        self.detachBtn.setText(QCoreApplication.translate("MainWindow", u"Detach", None))
        self.offsetOkbtn.setText(QCoreApplication.translate("MainWindow", u"GO", None))
        self.hexViewer.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Courier New'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"ADDRESS   0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Offset", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>kslide</p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Kernel   <br/>Base</p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Current<br/>kaddr</p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Current<br/>addr</p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Kern<br/>version</p></body></html>", None))
        self.tabWidget2.setTabText(self.tabWidget2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Status", None))
        self.offsetFilter.setPlaceholderText(QCoreApplication.translate("MainWindow", u"filter", None))
        self.tabWidget2.setTabText(self.tabWidget2.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Offsets", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Viewer", None))
        self.getVnodeAtPathBtn.setText(QCoreApplication.translate("MainWindow", u"Get", None))
        self.utilViewerFilter.setPlaceholderText(QCoreApplication.translate("MainWindow", u"filter", None))
        self.getAllProcLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Get all proc</p></body></html>", None))
        self.getAllProcBtn.setText(QCoreApplication.translate("MainWindow", u"Get", None))
        self.getVnodeAtPathInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"full file path", None))
        self.getPidListBtn.setText(QCoreApplication.translate("MainWindow", u"Get", None))
        self.getVnodeAtPathLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Get vnode at path</p></body></html>", None))
        self.getKfdBtn.setText(QCoreApplication.translate("MainWindow", u"Get", None))
        self.getPidListLabel.setText(QCoreApplication.translate("MainWindow", u"Get pid list", None))
        self.getKfdLabel.setText(QCoreApplication.translate("MainWindow", u"Get kfd", None))
        self.getKfdBtn.setText(QCoreApplication.translate("MainWindow", u"Get", None))
        self.utilTabWidget.setTabText(self.utilTabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Info", None))
        self.utilViewer.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Courier New'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Util", None))
    # retranslateUi

