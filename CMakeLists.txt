
cmake_minimum_required( VERSION 3.15 )

find_package( Python3 3.5 REQUIRED )

set( CMAKE_CONFIGURATION_TYPES "Debug;Release" CACHE STRING "Supported configuration types" FORCE )

project( njoy LANGUAGES Fortran )

include( GNUInstallDirs )

option( NJOY_BUILD_TESTS "Configure the njoy test suite" ON )

message( STATUS "" )
message( STATUS "-----------------------------------------------------------" )
message( STATUS "" )
message( STATUS "njoy" )
message( STATUS "Git current branch: ${GIT_BRANCH}" )
message( STATUS "Git commit hash: ${GIT_HASH}" )
message( STATUS "" )
message( STATUS "-----------------------------------------------------------" )

add_executable( njoy_executable
             "${CMAKE_CURRENT_SOURCE_DIR}/src/main.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/acecm.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/acedo.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/acefc.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/acepa.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/acepn.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/acer.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/aceth.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/broadr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/ccccr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/covr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/dtfr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/endf.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/errorr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/gaminr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/gaspr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/graph.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/groupr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/heatr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/leapr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/locale.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/main.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/mainio.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/mathm.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/matxsr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/mixr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/moder.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/phys.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/plotr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/powr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/purr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/reconr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/resxsr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/samm.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/thermr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/unresr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/util.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/vers.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/viewr.f90"
             "${CMAKE_CURRENT_SOURCE_DIR}/src/wimsr.f90" )
set_target_properties( njoy_executable PROPERTIES OUTPUT_NAME njoy )

if( SKBUILD )
  # The wheel ships the executable on its own, so link the compiler runtime
  # statically to keep it independent of the build machine's gcc installation.
  # libquadmath matters as much as libgfortran here: if it is left dynamic,
  # macOS wheel repair bundles Homebrew's libquadmath, whose minimum OS target
  # is that of the build runner and so raises the whole wheel's target.
  # Each flag is probed rather than assumed, since a toolchain missing the
  # matching static archive would otherwise fail to link.
  if( CMAKE_Fortran_COMPILER_ID STREQUAL "GNU" )
    include( CheckLinkerFlag )
    foreach( flag -static-libgfortran -static-libgcc -static-libquadmath )
      string( MAKE_C_IDENTIFIER "NJOY_HAVE${flag}" flag_var )
      check_linker_flag( Fortran "${flag}" ${flag_var} )
      if( ${flag_var} )
        target_link_options( njoy_executable PRIVATE "${flag}" )
      endif()
    endforeach()
  endif()
endif()

install( TARGETS njoy_executable RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}" )

if( NJOY_BUILD_TESTS )
  enable_testing()
  add_subdirectory( tests )
endif()
