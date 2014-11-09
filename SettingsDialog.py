from SettingsDialogUi import Ui_SettingsDialog
from Settings import Settings

class SettingsDialog(Ui_SettingsDialog):
    
    def setupUi(self,Dialog):
        Ui_SettingsDialog.setupUi(self,Dialog)
        self.parent = Dialog
        settings = Settings().instance.getSettings()
        self.loadProvidersAtStartupCheckbox.setChecked( settings["downloadProvidersListAtStartup"] )
        self.urlOfThelistInput.setText( settings["providersList"] )
        self.pagesSpinBox.setValue( settings["pages"] )
        self.buttonBox.accepted.connect(self.saveSettings)
        self.buttonBox.rejected.connect(self.closeDialog)
        
    def saveSettings(self):
        settings = Settings().instance.getSettings()
        settings["downloadProvidersListAtStartup"] = self.loadProvidersAtStartupCheckbox.isChecked()
        settings["providersList"] = self.urlOfThelistInput.text()
        settings["pages"] = self.pagesSpinBox.value()
        self.closeDialog()
    
    def closeDialog(self):
        self.parent.close()