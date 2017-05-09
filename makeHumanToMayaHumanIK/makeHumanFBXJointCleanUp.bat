REM drag and drop file, freeze transformation use mayapy
set MAYAPY="C:\Program Files\Autodesk\Maya2016.5\bin\mayapy.exe"
set PyScript=%~dp0makehumanFBXcleanup.py
echo %MAYAPY%
echo %*
%MAYAPY% %PyScript% %*
PAUSE

