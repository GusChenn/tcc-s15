#!/bin/bash

input_prefix="videos-"
output_prefix="images-"
preprocessd_output_prefix="preprocessed-"
patter="(.*)(-)(.*)(-)(.*)(-)([^\/]*)"
regex="((${input_prefix})${patter})"

for dir in inputs/*/; do
  if [[ $dir =~ $regex ]]; then
    echo "Processando ${BASH_REMATCH[3]}"
    set=""
    extraction_type="-vf fps=20"
    init_time=""
    end_time=""
    output_name=""
    if [ ${BASH_REMATCH[3]} != "null" ]; then
      set="-i ./${dir}${BASH_REMATCH[3]}.mp4"
    fi
    if [ ${BASH_REMATCH[5]} != "normal" ]; then
      extraction_type="-vf fps=10"
    fi
    if [ ${BASH_REMATCH[7]} != "null" ]; then
      init_time="-ss ${BASH_REMATCH[7]}"
    fi
    if [ ${BASH_REMATCH[9]} != "null" ]; then
      end_time="-t ${BASH_REMATCH[9]}"
    fi
    # png, jpg, bmp
    output_name="./outputs/${output_prefix}${BASH_REMATCH[3]}/%06d.png"
  fi
  # deleta todos os frames da extracao anterior
  delete="rm ./outputs/${output_prefix}${BASH_REMATCH[3]}/*"
  delete_preprocessed="rm ./outputs/${preprocessd_output_prefix}${BASH_REMATCH[3]}/*"
  echo "Deletando todos os frames nas pastas de outuput (com e sem pre processamento)"
  eval "$delete"
  eval "$delete_preprocessed"

  # Realiza a extracao
  extract="ffmpeg ${init_time} ${set} ${extraction_type} ${end_time} ${output_name}"
  eval "$extract"
done

# ffmpeg -i input.mp4 -an -vcodec rawvideo -pix_fmt yuv420p rawbitstream.yuv
