

# restoreNatronDefaultSettings
This reset Natron preference, because I can not find Natron 2.3.14 preference on Windows


1. RUN Natron in interactive mode
    + `%NATRON_BIN_FOLDER%\Natron.exe" -t`
2. Run The following line by line (check out [Natron Doc](https://natron.readthedocs.io/en/master/devel/PythonReference/NatronEngine/PyCoreApplication.html) and [AppSettings](https://natron.readthedocs.io/en/master/devel/PythonReference/NatronEngine/AppSettings.html), NatronEngine.natron.getSettings() basically return you Current NatronEngine AppSettings, which is in charge of preference settings.)
    + `NatronEngine.natron.getSettings().restoreDefaultSettings`
    + `NatronEngine.natron.getSettings().saveSettings()`
    + `exit()`

