#!/bin/bash
set -ex
INPUT_FONTS_DIR=$(pwd)/targetfont

generate_ascii_3d_files() {
  FONT_FILE=$INPUT_FONTS_DIR/$1
  OUTPUTDIR=$(cd $INPUT_FONTS_DIR && cd .. && pwd)/output/$(basename $1 .ttf)
  mkdir -p $OUTPUTDIR
  cd font-to-3d-models
  #blender -b -P font_to_3d_models.py -- -f $FONT_FILE -o $OUTPUTDIR --format stl
  #blender -P font_to_3d_models.py -- -f $FONT_FILE -o $OUTPUTDIR --format stl
  blender -b -P font_to_3d_models.py -- -f $FONT_FILE -o $OUTPUTDIR --format stl --letters abcdefghijklmnopqrstuvwxyz
}

FILES=$(ls $INPUT_FONTS_DIR)
for f in $FILES; do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  #cat "$f"
  generate_ascii_3d_files $f
done
