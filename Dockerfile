FROM ubuntu:18.04 
ARG DEBIAN_FRONTEND=noninteractive 
RUN apt-get update 
RUN apt-get install -y curl wget unzip awscli sudo openssh-server git jq 
