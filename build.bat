@echo off

rem Script to build the custom recipe

where python 
if %errorlevel% neq 0 (
    echo Python can't be found, please install it and make it available before continuing
    exit /B 1
)

python --version | findstr "3.10"
if %errorlevel% neq 0 (
    echo Python version must be 3.10, please install it and make it available before continuing
    exit /B 1
)

where conan
if %errorlevel% neq 0 (
    echo conan not found, installing it
    python -m venv env
    call env/Scripts/activate
    pip install conan
)

cd openimageio
conan create . openimageio/2.4@pythonbindings/1.0 -o with_ffmpeg=False -o *:shared=True

cd ..
conan install .
