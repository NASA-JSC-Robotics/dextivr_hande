cmake_minimum_required(VERSION 3.5)
project(dextivr_hande_deploy)

find_package(ament_cmake)

if(ament_cmake_FOUND)

  install(
    DIRECTORY launch rviz
    DESTINATION share/${PROJECT_NAME}
  )

  ament_export_dependencies(${THIS_PACKAGE_INCLUDE_DEPENDS})

  ament_package()

else()

  find_package(catkin REQUIRED)
  catkin_package()
  install(DIRECTORY launch rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  )
endif()
