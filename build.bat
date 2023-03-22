@echo off

rem Script to build the custom recipe

where python 
if %errorlevel% neq 0 (
    echo Python can't be found, please install it and make it available in the PATH before continuing
    exit /B 1
) else (
    echo Found python
)

where cmake
if %errorlevel% neq 0 (
    echo CMake can't be found, please install it and make it available in the PATH before continuing
    exit /B 1
) else (
    echo Found CMake
)

where conan
if %errorlevel% neq 0 (
    echo conan not found, installing it
    python -m venv env
    call env/Scripts/activate
    pip install conan==1.59
) else (
    conan --version | findstr 1.59
    if %errorlevel% neq 0 (
        echo Conan version supported is 1.59.0, please install it or make a new virtual environment 
        exit /B 1
    )

    echo conan 1.59 found
)

cd openimageio
conan create . openimageio/2.4@pythonbindings/1.0 -o with_ffmpeg=False -o *:shared=True

cd ..
conan install .
