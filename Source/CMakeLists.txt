cmake_minimum_required(VERSION 3.25)
project(LuaCpp)

set(CMAKE_CXX_STANDARD 17)

# Source files
set(SOURCE_FILES
        Lua.hpp
        LuaCpp.hpp
        LuaVersion.cpp LuaVersion.hpp
        Engine/LuaState.cpp Engine/LuaState.hpp
        Engine/LuaType.cpp Engine/LuaType.hpp
        Engine/LuaTNil.cpp Engine/LuaTNil.hpp
        Engine/LuaTString.cpp Engine/LuaTString.hpp
        Engine/LuaTNumber.cpp Engine/LuaTNumber.hpp
        Engine/LuaTBoolean.cpp Engine/LuaTBoolean.hpp
        Engine/LuaTTable.cpp Engine/LuaTTable.hpp
        Engine/LuaTUserData.cpp Engine/LuaTUserData.hpp
        Registry/LuaRegistry.cpp Registry/LuaRegistry.hpp
        Registry/LuaCodeSnippet.cpp Registry/LuaCodeSnippet.hpp
        Registry/LuaCompiler.cpp Registry/LuaCompiler.hpp
        Registry/LuaCFunction.cpp Registry/LuaCFunction.hpp
        Registry/LuaLibrary.cpp Registry/LuaLibrary.hpp
        LuaContext.cpp LuaContext.hpp
        LuaMetaObject.cpp LuaMetaObject.hpp
)

include(GNUInstallDirs)

find_package(Lua REQUIRED)

add_library(luacpp SHARED ${SOURCE_FILES})
add_library(luacpp_static STATIC ${SOURCE_FILES})
set_target_properties(luacpp_static PROPERTIES OUTPUT_NAME luacpp)
target_link_libraries(luacpp lua::lua)
target_link_libraries(luacpp_static lua::lua)


#########
# Install
#########
include(CMakePackageConfigHelpers)

set(CMAKE_INSTALL_LIBDIR lib)
set(CMAKE_CONFIG_DEST "${CMAKE_INSTALL_LIBDIR}/${PROJECT_NAME}/cmake")
set(LuaCpp_INCLUDE_DIR "${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}")
set(LuaCpp_INSTALL_LIBDIR "${CMAKE_INSTALL_LIBDIR}")

install(TARGETS luacpp
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(TARGETS luacpp_static
        DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(FILES LuaCpp.hpp Lua.hpp LuaContext.hpp LuaMetaObject.hpp LuaVersion.hpp
        DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}")

install(DIRECTORY ${CMAKE_SOURCE_DIR}/Registry ${CMAKE_SOURCE_DIR}/Engine
        DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}"
        FILES_MATCHING
        PATTERN "*.hpp"
)
configure_package_config_file(
        LuaCppConfig.cmake.in
        ${CMAKE_CURRENT_BINARY_DIR}/LuaCppConfig.cmake
        INSTALL_DESTINATION "${CMAKE_CONFIG_DEST}"
        PATH_VARS
        LuaCpp_INCLUDE_DIR
        LuaCpp_INSTALL_LIBDIR
)
write_basic_package_version_file(
        ${CMAKE_CURRENT_BINARY_DIR}/LuaCppConfigVersion.cmake
        VERSION 0.1.0
        COMPATIBILITY SameMajorVersion
        ARCH_INDEPENDENT
)
install(FILES
        ${CMAKE_CURRENT_BINARY_DIR}/LuaCppConfigVersion.cmake
        ${CMAKE_CURRENT_BINARY_DIR}/LuaCppConfig.cmake
        DESTINATION ${CMAKE_CONFIG_DEST}
)

###########
# Documents
###########
option(BUILD_DOC "Build documentation" OFF)

# check if Doxygen is installed
find_package(Doxygen)
if (DOXYGEN_FOUND)
    # set input and output files
    set(DOXYGEN_IN ${PROJECT_SOURCE_DIR}/../docs/Doxyfile.in)
    set(DOXYGEN_OUT ${PROJECT_BINARY_DIR}/Doxyfile)

    # request to configure the file
    configure_file(${DOXYGEN_IN} ${DOXYGEN_OUT} @ONLY)
    message("Doxygen build started")

    # note the option ALL which allows to build the docs together with the application
    add_custom_target(doc_doxygen
            COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_OUT}
            WORKING_DIRECTORY ${PROJECT_BINARY_DIR}
            COMMENT "Generating API documentation with Doxygen"
            VERBATIM)
    add_custom_target(doc_pdf
            COMMAND cd doc_doxygen/latex && make pdf
            COMMAND mv doc_doxygen/latex/refman.pdf ${CMAKE_BINARY_DIR}/luacpp.pdf
            DEPENDS doc_doxygen
    )
else (DOXYGEN_FOUND)
    message("Doxygen need to be installed to generate the doxygen documentation")
endif (DOXYGEN_FOUND)
