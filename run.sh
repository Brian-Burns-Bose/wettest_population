#!/bin/bash

docker run -d -p 8888:8888 \
  -v `pwd`:/home/jovyan/work bpburns/geopandas-notebook \
  start-notebook.sh \
  --NotebookApp.token='' \
  --NotebookApp.iopub_data_rate_limit=10000000000
