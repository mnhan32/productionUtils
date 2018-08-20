
FOR %%A IN (%*) DO (
    "C:\Program Files\Side Effects Software\Houdini 16.0.504.20\bin\hython.exe"  %0\..\pathmap.py %%A
)
PAUSE
