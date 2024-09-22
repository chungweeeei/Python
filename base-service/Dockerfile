FROM ubuntu-fastdds:v2.14.2

USER root

RUN apt-get -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq install \
    git vim pip

RUN pip install --upgrade --user setuptools==58.0.0

# fastdds dependency
RUN apt install -y swig 
RUN pip3 install colcon-common-extensions
RUN pip3 install vcstool

RUN pip3 install pipenv 


# docker build -t failed on latest version of docker 
# do not use docker buildkit to build image
# DOCKER_BUILDKIT=0 docker build -t <docker-image-name> ,