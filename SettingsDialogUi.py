# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Settings.ui'
#
# Created: Sun Oct 26 18:16:48 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(400, 192)
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(SettingsDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.loadProvidersAtStartupCheckbox = QtWidgets.QCheckBox(self.groupBox)
        self.loadProvidersAtStartupCheckbox.setChecked(True)
        self.loadProvidersAtStartupCheckbox.setObjectName("loadProvidersAtStartupCheckbox")
        self.verticalLayout_2.addWidget(self.loadProvidersAtStartupCheckbox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.urlOfThelistLabel = QtWidgets.QLabel(self.groupBox)
        self.urlOfThelistLabel.setObjectName("urlOfThelistLabel")
        self.horizontalLayout.addWidget(self.urlOfThelistLabel)
        self.urlOfThelistInput = QtWidgets.QLineEdit(self.groupBox)
        self.urlOfThelistInput.setObjectName("urlOfThelistInput")
        self.horizontalLayout.addWidget(self.urlOfThelistInput)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.pagesSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.pagesSpinBox.setMinimum(1)
        self.pagesSpinBox.setProperty("value", 3)
        self.pagesSpinBox.setObjectName("pagesSpinBox")
        self.horizontalLayout_2.addWidget(self.pagesSpinBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings"))
        self.groupBox.setTitle(_translate("SettingsDialog", "General Setttings"))
        self.loadProvidersAtStartupCheckbox.setText(_translate("SettingsDialog", "Load providers from list at startup"))
        self.urlOfThelistLabel.setText(_translate("SettingsDialog", "URL of the list:"))
        self.label_2.setText(_translate("SettingsDialog", "Pages to fetch:"))

