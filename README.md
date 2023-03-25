# OIIO-PythonBindings

![Windows Py 3.10](https://github.com/romainaugier/OIIO-PythonBindings/actions/workflows/windows-py310.yml/badge.svg)
![Windows Py 3.9](https://github.com/romainaugier/OIIO-PythonBindings/actions/workflows/windows-py39.yml/badge.svg)
![Linux Py 3.10](https://github.com/romainaugier/OIIO-PythonBindings/actions/workflows/linux-py310.yml/badge.svg)
![Linux Py 3.9](https://github.com/romainaugier/OIIO-PythonBindings/actions/workflows/linux-py39.yml/badge.svg)

Python bindings for OpenImageIO. It uses [Conan 1.59.0](https://conan.io) to build the custom recipe
you can find in *openimageio*.*/conanfile.py*.

If you encounter this error 
```
ERROR: 'settings.compiler' value not defined
```
Make sure to have a compiler installed on your computer (Visual Studio for windows, gcc for Linux...).

After you've installed a compiler, run 
```
conan profile new default --detect --force
```
To update the conan profile with the newly installed compiler.

## Windows 

### Building
```bat
git clone https://github.com/romainaugier/OIIO-PythonBindings.git
cd OIIO-PythonBindings
./build.bat
```

### Usage
```bat
.\scripts\activate.bat
python
>>> import OpenImageIO as oiio
>>> ...
>>> exit()
.\scripts\deactivate.bat
```

## Linux

### Building
```sh
git clone https://github.com/romainaugier/OIIO-PythonBindings.git
cd OIIO-PythonBindings
./build.sh
```

### Usage
```sh
./scripts/activate.sh
python
>>> import OpenImageIO as oiio
>>> ...
>>> exit()
./scripts/deactivate.sh
```

## MacOS
Not yet available, working on it
