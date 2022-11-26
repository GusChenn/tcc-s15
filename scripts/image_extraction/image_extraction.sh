#!/bin/bash

for video in ../video_acquisition/output/*; do
  echo "Processando ${video}"
  set="-i ${video}"
  extraction_type="-vf fps=20"

  file_name_without_path=${video:28}
  file_name_without_extension=${file_name_without_path::-4}

  # png, jpg, bmp
  output_name="./outputs/${file_name_without_extension}%06d.jpg"

  command="ffmpeg ${set} ${extraction_type} ${output_name}"
  eval "$command"
done
