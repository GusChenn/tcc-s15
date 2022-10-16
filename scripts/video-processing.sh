#!/bin/bash

input_prefix="videos-"
output_prefix="images-"
patter="(.*)(-)(.*)(-)(.*)(-)([^\/]*)"
regex="((${input_prefix})${patter})"

for dir in inputs/*/; do
  if [[ $dir =~ $regex ]]; then
    echo "Processando ${BASH_REMATCH[3]}"
    set=""
    extraction_type=""
    init_time=""
    end_time=""
    output_name=""
    if [ ${BASH_REMATCH[3]} != "null" ]; then
      set="-i ./${dir}${BASH_REMATCH[3]}.mp4"
    fi
    if [ ${BASH_REMATCH[5]} != "normal" ]; then
      extraction_type="select='not(mod(n\,10))"
    fi
    if [ ${BASH_REMATCH[7]} != "null" ]; then
      init_time="-ss ${BASH_REMATCH[7]}"
    fi
    if [ ${BASH_REMATCH[9]} != "null" ]; then
      end_time="-t ${BASH_REMATCH[9]}"
    fi
    # png, jpg, bmp
    output_name="./outputs/${output_prefix}${BASH_REMATCH[3]}/${BASH_REMATCH[3]}%06d.bmp"
  fi
  command="ffmpeg ${init_time} ${set} ${end_time} ${output_name}"
  eval "$command"
  # ffmpeg -i ./inputs/videos-set1-normal-null-null/set1.mp4 out%05d.png
done

# ffmpeg -i input.mp4 -an -vcodec rawvideo -pix_fmt yuv420p rawbitstream.yuv
