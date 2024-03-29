# !bin/sh

docker run \
-it \
-p 8888:8888 \
--rm \
-v "/Users/lucaspereyra/luqui/travis/notebooks":/home/jovyan/work \
jupyter/datascience-notebook 