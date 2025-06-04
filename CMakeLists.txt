cmake_minimum_required(VERSION 3.5)
project(swd_starter_kit_bringup)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(lifecycle_msgs REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)

# ############
# # Clang ##
# ############

# Allow Clang-tidy
# set(CMAKE_CXX_CLANG_TIDY clang-tidy-12 --config-file=${CMAKE_SOURCE_DIR}/.clang-tidy --use-color --header-filter=${CMAKE_SOURCE_DIR}/include/)
# set(DCMAKE_EXPORT_COMPILE_COMMANDS ON)

install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})

ament_package()