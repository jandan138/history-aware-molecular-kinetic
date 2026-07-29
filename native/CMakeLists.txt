cmake_minimum_required(VERSION 3.22)
project(historykinetic_native LANGUAGES CXX)

option(HAMK_BUILD_TESTS "Build native smoke tests" ON)

add_library(historykinetic_native
    src/history_window.cpp
    src/solver.cpp
)
target_include_directories(historykinetic_native PUBLIC include)
target_compile_features(historykinetic_native PUBLIC cxx_std_20)
target_compile_options(historykinetic_native PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall;-Wextra;-Wpedantic;-Werror>
)

if(HAMK_BUILD_TESTS)
    enable_testing()
    add_executable(historykinetic_native_smoke tests/smoke.cpp)
    target_link_libraries(historykinetic_native_smoke PRIVATE historykinetic_native)
    add_test(NAME native_smoke COMMAND historykinetic_native_smoke)
endif()
