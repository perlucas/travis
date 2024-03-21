# !bin/sh

docker run \
-it \
-p 8080:8888 \
--rm \
-v "C:\projects\travis\notebooks":/home/jovyan/work \
jupyter/datascience-notebook 