from conan import ConanFile
from conan.tools.build import check_min_cppstd, check_max_cppstd
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class StellarForgeCommon(ConanFile):
    name = "lua-cpp"
    version = "1.0.0"

    # Optional metadata
    url = "https://github.com/epitech-mirroring/luacpp"
    description = "Lua engine for C++"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {}
    exports_sources = "CMakeLists.txt", "*", "!build/*"

    def config_options(self):
        pass

    def layout(self):
        cmake_layout(self)

    def validate(self):
        check_min_cppstd(self, "17")
        check_max_cppstd(self, "20")

    def requirements(self):
        self.requires("lua/5.4.7")
        self.requires("gtest/1.15.0")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["luacpp"]
        self.cpp_info.libdirs = ["lib"]
