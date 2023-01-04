#!/bin/bash
#set -ex
INPUT_FONTS_DIR=$(pwd)/targetfont

OUTPUTDIR_BASE_PATH=$(cd $INPUT_FONTS_DIR && cd .. && pwd)/output

# this must be upright when opened with F3d if not, rotate it in blender until it is
BASE_KEYCAP_STL=$(pwd)/"superbasickeycap1.stl"
BASE_KEYCAP_STL=$(pwd)/"keycap_lid.stl"
#BASE_KEYCAP_STL=$(pwd)/"cube.stl"

MESH_WORKING_DIR="meshworkingdir"

generate_ascii_3d_files() {
    # make the font into 3d models
    FONT_FILE=$INPUT_FONTS_DIR/$1
    OUTPUTDIR=$OUTPUTDIR_BASE_PATH/font_stl/$(basename $1 .ttf)
    mkdir -p $OUTPUTDIR || echo "" >/dev/null
    cd font-to-3d-models
    #blender -b -P font_to_3d_models.py -- -f $FONT_FILE -o $OUTPUTDIR --format stl
    #blender -P font_to_3d_models.py -- -f $FONT_FILE -o $OUTPUTDIR --format stl --letters abcdefghijklmnopqrstuvwxyz
    # lowercase
    #blender -b -P font_to_3d_models.py -- -f $FONT_FILE -o $OUTPUTDIR --format stl --letters abcdefghijklmnopqrstuvwxyz
    blender -b -P font_to_3d_models.py -- -f $FONT_FILE -o $OUTPUTDIR --format stl --letters ABCDEFGHIJKLMNOPQRSTUVWXYZ
}

combine_font_and_keycap_stls() {
    echo "combine $1 $2 into $3"

    # TODO move the build to earlier in script
    mkdir -p $MESH_WORKING_DIR

    # copy files to work on them
    cp $1 $MESH_WORKING_DIR/font.stl
    cp $2 $MESH_WORKING_DIR/keycap.stl

    # build and run docker image
    pymesh_jupyter_image="pymeshscript"

    docker build -t $pymesh_jupyter_image -f dockerfile.pymeshscript .

    docker run --rm -it -v $(pwd)/$MESH_WORKING_DIR:/local pymeshscript

    # copy files out
    cp $MESH_WORKING_DIR/keycap_with_cutout.obj $3/$(basename $1 .stl)_keycap.obj
    cp $MESH_WORKING_DIR/font_insert.obj $3/$(basename $1 .stl)_insert.obj

    #rm -rf $MESH_WORKING_DIR/*.stl
    #rm -rf $MESH_WORKING_DIR/*.obj
}

combine_font_files_with_keycaps() {
    # for each stl in the font folder, combine it with base cube

    FONT_STL_DIR=$OUTPUTDIR_BASE_PATH/font_stl/$(basename $1 .ttf)

    # create an output directory
    OUTPUTDIR=$OUTPUTDIR_BASE_PATH/keycap_stl/$(basename $1 .ttf)
    mkdir -p $OUTPUTDIR

    FILES=$(ls $FONT_STL_DIR)
    for f in $FILES; do
        echo "Processing font stl: $f "
        # call docker and run the combine
        combine_font_and_keycap_stls $FONT_STL_DIR/$f $BASE_KEYCAP_STL $OUTPUTDIR

        # TODO rm this to do all
        exit 0
    done
}

startdir=$(pwd)

FILES=$(ls $INPUT_FONTS_DIR)
for f in $FILES; do
    echo "Processing font: $f "
    # make a folder for and export all the font .stl files
    # TODO re-enable when needed
    generate_ascii_3d_files $f

    cd $startdir
    # combine with keycaps
    combine_font_files_with_keycaps $f

done
