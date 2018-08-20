@echo off
set file1=
set file2=

echo Drag and drop Python Script + Enter:
set /p file1=
echo.

echo Drag and drop Maya Files + Enter:
set /p file2=
echo.

echo.&echo.
echo %file1% 
echo %file2%
echo.

"C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe" %file1% %file2%

echo Completed.
PAUSE
