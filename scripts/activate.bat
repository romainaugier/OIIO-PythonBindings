@echo off

rem Setup the virtual environment to run OpenImageIO

set __OLDPATH=%PATH%
set __OLDPYTHONPATH=%PYTHONPATH%

set PATH=%CD%\bin;%PATH%
set PYTHONPATH=%CD%\bin;%PYTHONPATH%
