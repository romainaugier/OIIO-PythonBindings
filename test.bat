@echo off

rem Test the bindings are working and are imported correctly

call .\scripts\activate.bat

python tests\oiio_test.py

call .\scripts\deactivate.bat
