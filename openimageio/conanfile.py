import glob
from conan.tools.microsoft import is_msvc, is_msvc_static_runtime
from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import functools
import os

required_conan_version = ">=1.45.0"


class OpenImageIOConan(ConanFile):
    name = "openimageio"

    version = "2.4"

    description = (
        "OpenImageIO is a library for reading and writing images, and a bunch "
        "of related classes, utilities, and applications. There is a "
        "particular emphasis on formats and functionality used in "
        "professional, large-scale animation and visual effects work for film."
    )

    topics = ("vfx", "image", "picture")
    license = "BSD-3-Clause"
    homepage = "http://www.openimageio.org/"
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "arch", "compiler", "build_type"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "python_bindings": [True, False],
        "with_libjpeg": ["libjpeg", "libjpeg-turbo"],
        "with_libpng": [True, False],
        "with_freetype": [True, False],
        "with_hdf5": [True, False],
        "with_opencolorio": [True, False],
        "with_opencv": [True, False],
        "with_tbb": [True, False],
        "with_dicom": [True, False],
        "with_ffmpeg": [True, False],
        "with_giflib": [True, False],
        "with_libheif": [True, False],
        "with_raw": [True, False],
        "with_openjpeg": [True, False],
        "with_openvdb": [True, False],
        "with_ptex": [True, False],
        "with_libwebp": [True, False],
    }

    default_options = {
        "shared": True,
        "fPIC": True,
        "python_bindings": True,
        "with_libjpeg": "libjpeg",
        "with_libpng": True,
        "with_freetype": True,
        "with_hdf5": True,
        "with_opencolorio": False,
        "with_opencv": False,
        "with_tbb": True,
        "with_dicom": False, # Heavy dependency, disabled by default
        "with_ffmpeg": False,
        "with_giflib": True,
        "with_libheif": False,
        "with_raw": False, # libraw is available under CDDL-1.0 or LGPL-2.1, for this reason it is disabled by default
        "with_openjpeg": True,
        "with_openvdb": False, # FIXME: broken on M1
        "with_ptex": True,
        "with_libwebp": True,
    }

    short_paths = True
    generators = "cmake", "cmake_find_package"

    @property
    def _source_subfolder(self):
        return "openimageio_source"

    @property
    def _build_subfolder(self):
        return "openimageio_build"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def requirements(self):
        # Required libraries
        self.requires("zlib/1.2.12")
        self.requires("boost/1.78.0")
        self.requires("libtiff/4.3.0")
        self.requires("openexr/3.1.5")
        if self.options.with_libjpeg == "libjpeg":
            self.requires("libjpeg/9d")
        elif self.options.with_libjpeg == "libjpeg-turbo":
            self.requires("libjpeg-turbo/2.1.2")
        self.requires("pugixml/1.12.1")
        self.requires("libsquish/1.15")
        self.requires("tsl-robin-map/1.0.1")
        self.requires("fmt/8.1.1")

        # Optional libraries
        if self.options.python_bindings:
            self.requires("pybind11/2.10.1")
        if self.options.with_libpng:
            self.requires("libpng/1.6.37")
        if self.options.with_freetype:
            self.requires("freetype/2.12.1")
        if self.options.with_hdf5:
            self.requires("hdf5/1.12.1")
        if self.options.with_opencolorio:
            if tools.Version(self.version) < "2.3.7.2":
                self.requires("opencolorio/1.1.1")
        if self.options.with_opencv:
            self.requires("opencv/4.5.5")
        if self.options.with_tbb:
            self.requires("onetbb/2021.7.0")
        if self.options.with_dicom:
            self.requires("dcmtk/3.6.6")
        if self.options.with_ffmpeg:
            self.requires("ffmpeg/4.4")
        # TODO: Field3D dependency
        if self.options.with_giflib:
            self.requires("giflib/5.2.1")
        if self.options.with_libheif:
            self.requires("libheif/1.12.0")
        if self.options.with_raw:
            self.requires("libraw/0.20.2")
        if self.options.with_openjpeg:
            self.requires("openjpeg/2.5.0")
        if self.options.with_openvdb:
            self.requires("openvdb/8.0.1")
        if self.options.with_ptex:
            self.requires("ptex/2.4.0")
        if self.options.with_libwebp:
            self.requires("libwebp/1.2.3")
        # TODO: R3DSDK dependency
        # TODO: Nuke dependency

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            if tools.Version(self.version) >= "2.3.0.0" or self.options.with_openvdb:
                tools.check_min_cppstd(self, 14)
            else:
                tools.check_min_cppstd(self, 11)
        if is_msvc(self) and is_msvc_static_runtime(self) and self.options.shared:
            raise ConanInvalidConfiguration("Building shared library with static runtime is not supported!")

    def _patch_fmt_include(self):
        # replace FMT_INCLUDES with fmt_INCLUDES
        files = glob.glob("{0}/src/include/CMakeLists.txt".format(self._source_subfolder))

        if files:
            cmake_file = files[0]

            with open(cmake_file, "r") as file:
                content = file.read()

            content = content.replace("FMT_INCLUDES", "fmt_INCLUDES")

            with open(cmake_file, "w") as file:
                file.write(content)

            print("Patched fmt include")

    def _patch_openjpeg_include(self):
        # replace OPENJPEG_INCLUDE with OpenJPEG_INCLUDES
        files = glob.glob("{0}/src/jpeg2000.imageio/CMakeLists.txt".format(self._source_subfolder))

        if files:
            cmake_file = files[0]

            with open(cmake_file, "r") as file:
                content = file.read()

            content = content.replace("OPENJPEG_INCLUDES", "OpenJPEG_INCLUDES")
            content = content.replace("OPENJPEG_LIBRARIES", "OpenJPEG_LIBRARIES")

            with open(cmake_file, "w") as file:
                file.write(content)

            print("Patched OpenJPEG include")

    def _patch_openexr_includes(self):
        # replace OPENEXR_INCLUDES with OpenEXR_INCLUDES
        # replace IMATHS_INCLUDES with Imath_INCLUDES
        files = glob.glob("{0}/src/cmake/externalpackages.cmake".format(self._source_subfolder))

        if files:
            cmake_file = files[0]

            with open(cmake_file, "r") as file:
                content = file.read()

            content = content.replace("IMATH_INCLUDE", "Imath_INCLUDES")
            content = content.replace("OPENEXR_INCLUDES", "OpenEXR_INCLUDES")

            content = content.replace(
"""
if (OPENEXR_VERSION VERSION_GREATER_EQUAL 3.0)
    set (OIIO_USING_IMATH 3)
else ()
    set (OIIO_USING_IMATH 2)
endif ()
""",
"""
set (OIIO_USING_IMATH 3)
""")

            with open(cmake_file, "w") as file:
                file.write(content)

            print("Patched OpenEXR includes")

    def source(self):
        tools.download("https://github.com/OpenImageIO/oiio/archive/refs/tags/v2.4.9.0.zip", "oiio-2.4.9.0.zip")

        tools.unzip("oiio-2.4.9.0.zip", self._source_subfolder, strip_root=True)

        # tools.get("https://github.com/OpenImageIO/oiio/archive/refs/tags/v2.4.4.2.zip", destination=self._source_subfolder)

        self._patch_fmt_include()
        self._patch_openjpeg_include()
        self._patch_openexr_includes()

    @functools.lru_cache(1)
    def _configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["CMAKE_MODULE_PATH"] = self.install_folder.replace("\\", "/")

        print("*" * 100)
        print(self.install_folder.replace("\\", "/"))
        print("*" * 100)

        # CMake options
        cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "" # Needed for 2.3.x.x+ versions
        cmake.definitions["OIIO_BUILD_TOOLS"] = False
        cmake.definitions["OIIO_BUILD_TESTS"] = False
        cmake.definitions["BUILD_DOCS"] = False
        cmake.definitions["INSTALL_DOCS"] = False
        cmake.definitions["INSTALL_FONTS"] = False
        cmake.definitions["INSTALL_CMAKE_HELPER"] = False
        cmake.definitions["EMBEDPLUGINS"] = True
        cmake.definitions["USE_PYTHON"] = self.options.python_bindings
        cmake.definitions["USE_EXTERNAL_PUGIXML"] = True

        # OIIO CMake files are patched to check USE_* flags to require or not use dependencies
        cmake.definitions["USE_JPEGTURBO"] = self.options.with_libjpeg == "libjpeg-turbo"
        cmake.definitions["USE_JPEG"] = True # Needed for jpeg.imageio plugin, libjpeg/libjpeg-turbo selection still works
        cmake.definitions["USE_HDF5"] = self.options.with_hdf5
        cmake.definitions["USE_OPENCOLORIO"] = self.options.with_opencolorio
        cmake.definitions["USE_OPENCV"] = self.options.with_opencv
        cmake.definitions["USE_TBB"] = self.options.with_tbb
        cmake.definitions["USE_DCMTK"] = self.options.with_dicom
        cmake.definitions["USE_FFMPEG"] = self.options.with_ffmpeg
        cmake.definitions["USE_FIELD3D"] = False
        cmake.definitions["USE_GIF"] = self.options.with_giflib
        cmake.definitions["USE_LIBHEIF"] = self.options.with_libheif
        cmake.definitions["USE_LIBRAW"] = self.options.with_raw
        cmake.definitions["USE_OPENVDB"] = self.options.with_openvdb
        cmake.definitions["USE_PTEX"] = self.options.with_ptex
        cmake.definitions["USE_R3DSDK"] = False
        cmake.definitions["USE_NUKE"] = False
        cmake.definitions["USE_OPENGL"] = False
        cmake.definitions["USE_QT"] = False
        cmake.definitions["USE_LIBPNG"] = self.options.with_libpng
        cmake.definitions["USE_FREETYPE"] = self.options.with_freetype
        cmake.definitions["USE_LIBWEBP"] = self.options.with_libwebp
        cmake.definitions["USE_OPENJPEG"] = self.options.with_openjpeg

        # cmake.definitions["BOOST_ALL_NO_LIB"] = True

        if self.options.with_openvdb:
            cmake.definitions["CMAKE_CXX_STANDARD"] = 14

        cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)

        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "share"))

        self.copy("LICENSE.md", src=self._source_subfolder, dst="licenses")

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "OpenImageIO")
        self.cpp_info.set_property("cmake_target_name", "OpenImageIO::OpenImageIO")
        self.cpp_info.set_property("pkg_config_name", "OpenImageIO")

        self.cpp_info.components["openimageio_util"].set_property("cmake_target_name", "OpenImageIO::OpenImageIO_Util")
        self.cpp_info.components["openimageio_util"].libs = ["OpenImageIO_Util"]
        self.cpp_info.components["openimageio_util"].requires = [
            "boost::filesystem", "boost::thread", "boost::system",
            "boost::regex", "openexr::openexr",
        ]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["openimageio_util"].system_libs.extend(["dl", "m", "pthread"])

        self.cpp_info.components["main"].set_property("cmake_target_name", "OpenImageIO::OpenImageIO")
        self.cpp_info.components["main"].set_property("pkg_config_name", "OpenImageIO")
        self.cpp_info.components["main"].libs = ["OpenImageIO"]
        self.cpp_info.components["main"].requires = [
            "openimageio_util", "zlib::zlib", "boost::thread", "boost::system",
            "boost::container", "boost::regex", "libtiff::libtiff",
            "openexr::openexr", "pugixml::pugixml", "tsl-robin-map::tsl-robin-map",
            "libsquish::libsquish", "fmt::fmt",
        ]
        if self.options.with_libjpeg == "libjpeg":
            self.cpp_info.components["main"].requires.append("libjpeg::libjpeg")
        elif self.options.with_libjpeg == "libjpeg-turbo":
            self.cpp_info.components["main"].requires.append("libjpeg-turbo::libjpeg-turbo")
        if self.options.with_libpng:
            self.cpp_info.components["main"].requires.append("libpng::libpng")
        if self.options.with_freetype:
            self.cpp_info.components["main"].requires.append("freetype::freetype")
        if self.options.with_hdf5:
            self.cpp_info.components["main"].requires.append("hdf5::hdf5")
        if self.options.with_opencolorio:
            self.cpp_info.components["main"].requires.append("opencolorio::opencolorio")
        if self.options.with_opencv:
            self.cpp_info.components["main"].requires.append("opencv::opencv")
        if self.options.with_tbb:
            self.cpp_info.components["main"].requires.append("onetbb::onetbb")
        if self.options.with_dicom:
            self.cpp_info.components["main"].requires.append("dcmtk::dcmtk")
        if self.options.with_ffmpeg:
            self.cpp_info.components["main"].requires.append("ffmpeg::ffmpeg")
        if self.options.with_giflib:
            self.cpp_info.components["main"].requires.append("giflib::giflib")
        if self.options.with_libheif:
            self.cpp_info.components["main"].requires.append("libheif::libheif")
        if self.options.with_raw:
            self.cpp_info.components["main"].requires.append("libraw::libraw")
        if self.options.with_openjpeg:
            self.cpp_info.components["main"].requires.append("openjpeg::openjpeg")
        if self.options.with_openvdb:
            self.cpp_info.components["main"].requires.append("openvdb::openvdb")
        if self.options.with_ptex:
            self.cpp_info.components["main"].requires.append("ptex::ptex")
        if self.options.with_libwebp:
            self.cpp_info.components["main"].requires.append("libwebp::libwebp")
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["main"].system_libs.extend(["dl", "m", "pthread"])

        if not self.options.shared:
            self.cpp_info.components["main"].defines.append("OIIO_STATIC_DEFINE")

        # TODO: to remove in conan v2 once cmake_find_package* & pkg_config generators removed
        self.cpp_info.names["cmake_find_package"] = "OpenImageIO"
        self.cpp_info.names["cmake_find_package_multi"] = "OpenImageIO"
        self.cpp_info.names["pkg_config"] = "OpenImageIO"
        self.cpp_info.components["openimageio_util"].names["cmake_find_package"] = "OpenImageIO_Util"
        self.cpp_info.components["main"].names["cmake_find_package"] = "OpenImageIO"

