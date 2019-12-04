cmake_minimum_required(VERSION 3.14)
project(OperatorModule)

set(CMAKE_CXX_STANDARD 14)

include_directories(D:/Install/Anaconda3/include)
link_directories(D:/Install/Anaconda3/libs)

find_library(PYTHONLIB python37 D:/Install/Anaconda3/libs)
link_libraries(python37)

add_executable(OperatorModule main.cpp)
target_link_libraries(OperatorModule ${PYTHONLIB})

