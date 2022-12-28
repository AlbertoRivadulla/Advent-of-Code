cmake_minimum_required(VERSION 3.7)

# Obtain a file compile_commands.json used by ccls (through the plugin coc.nvim)
# to provide code completion in Neovim
set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE INTERNAL "")

# Name of the project
project(project)

# Create a variable with all the include directories
set(INCLUDE
    ${PROJECT_SOURCE_DIR}
)

include_directories(${INCLUDE})

# Create a variable with a link to all cpp files to compile
# set(SOURCES
#     # ${PROJECT_SOURCE_DIR}/main.cpp
#     # "${PROJECT_SOURCE_DIR}/main.cpp"
#     # "../main.cpp"
# )

# add_executable(main ${SOURCES})

# Create a variable with a link to all cpp files to compile
file(GLOB main_SRC
    "${PROJECT_SOURCE_DIR}/*.cpp"
)

# Add an executable with all the files above
add_executable(main ${main_SRC})

# Get rid of the cmake_install.cmake file created
set(CMAKE_SKIP_INSTALL_RULES True)

# Move the file compile_commands.json to the directory of the project.
execute_process(COMMAND cp compile_commands.json ..) 

