cmake_minimum_required(VERSION 3.24)
project(Day16)
set(CMAKE_CXX_STANDARD 20)

find_package(nlohmann_json 3.11.2 REQUIRED)


add_executable(Day16
        solve.cpp)

target_link_libraries(Day16 PUBLIC nlohmann_json::nlohmann_json)

