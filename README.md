# OIIO-PythonBindings

![Build Windows 3.10](https://github.com/romainaugier/OIIO-PythonBindings/actions/workflows/build-windows-310.yml/badge.svg)

Python bindings for OpenImageIO. It uses [Conan 1.59.0](https://conan.io) to build the custom recipe
you can find in *openimageio/conanfile.py*.

If you encounter this error 
```
ERROR: 'settings.compiler' value not defined
```
Make sure to have a compiler installed on your computer (Visual Studio for windows, gcc for Linux...).

## Windows 

### Building
```bat
mkdir oiiobindings
cd oiiobindings
./build.bat
```

### Usage
```bat
./setup_env.bat
python
>>> import OpenImageIO as oiio
>>> ...
```

## Linux
Not yet available, working on it

## MacOS
Not yet available, working on it
