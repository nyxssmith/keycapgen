#!/bin/bash


pymesh_jupyter_image="pymeshjupyter"

docker build -t $pymesh_jupyter_image .

docker run -p 8888:8888 -v $(pwd)/pymeshroot:/local $pymesh_jupyter_image 