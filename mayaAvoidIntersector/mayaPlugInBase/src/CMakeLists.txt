set(SOURCE_FILES
    "AvoidIntersectorCmd.h";
    "AvoidIntersectorCmd.cpp"
)

find_package(Maya REQUIRED)

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} PRIVATE Maya::Maya)
target_include_directories(${PROJECT_NAME} PRIVATE Maya::Maya)
MAYA_PLUGIN(${PROJECT_NAME})
