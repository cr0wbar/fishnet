# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProviderManagerDialog.ui'
#
# Created: Wed Oct 22 23:21:47 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_ProviderManagerDialog(object):
    def setupUi(self, ProviderManagerDialog):
        ProviderManagerDialog.setObjectName("ProviderManagerDialog")
        ProviderManagerDialog.resize(439, 457)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProviderManagerDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.providersBox = QtWidgets.QGroupBox(ProviderManagerDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.providersBox.sizePolicy().hasHeightForWidth())
        self.providersBox.setSizePolicy(sizePolicy)
        self.providersBox.setMinimumSize(QtCore.QSize(0, 350))
        self.providersBox.setObjectName("providersBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.providersBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.providersList = QtWidgets.QListView(self.providersBox)
        self.providersList.setObjectName("providersList")
        self.verticalLayout_2.addWidget(self.providersList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addNewProviderButton = QtWidgets.QToolButton(self.providersBox)
        self.addNewProviderButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.addNewProviderButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.addNewProviderButton.setObjectName("addNewProviderButton")
        self.horizontalLayout.addWidget(self.addNewProviderButton)
        self.removeProviderButton = QtWidgets.QToolButton(self.providersBox)
        self.removeProviderButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.removeProviderButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.removeProviderButton.setObjectName("removeProviderButton")
        self.horizontalLayout.addWidget(self.removeProviderButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addWidget(self.providersBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.buttonBox = QtWidgets.QDialogButtonBox(ProviderManagerDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(ProviderManagerDialog)
        QtCore.QMetaObject.connectSlotsByName(ProviderManagerDialog)

    def retranslateUi(self, ProviderManagerDialog):
        _translate = QtCore.QCoreApplication.translate
        ProviderManagerDialog.setWindowTitle(_translate("ProviderManagerDialog", "Manage Providers"))
        self.providersBox.setTitle(_translate("ProviderManagerDialog", "Providers"))
        self.addNewProviderButton.setText(_translate("ProviderManagerDialog", "..."))
        self.removeProviderButton.setText(_translate("ProviderManagerDialog", "..."))

