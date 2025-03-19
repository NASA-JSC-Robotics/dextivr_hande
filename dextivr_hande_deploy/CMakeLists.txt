cmake_minimum_required(VERSION 3.5)
project(dextivr_hande_deploy)

find_package(ament_cmake REQUIRED)

  install(
    DIRECTORY launch rviz config
    DESTINATION share/${PROJECT_NAME}
  )

  ament_export_dependencies(${THIS_PACKAGE_INCLUDE_DEPENDS})

  ament_package()
