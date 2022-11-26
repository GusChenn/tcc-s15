#!/bin/bash

for video in ../video_acquisition/output/*; do
  echo "Processando ${video}"
  set="-i ${video}"
  extraction_type="-vf fps=20"

  # png, jpg, bmp
  output_name="./outputs/%06d.jpg"

  command="ffmpeg ${set} ${extraction_type} ${output_name}"
  eval "$command"
done
