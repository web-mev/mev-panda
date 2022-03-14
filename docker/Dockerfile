FROM debian:bullseye

SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    wget \
    git \
    python3 \
    python3-pip

# Install all software under /opt/software:
RUN mkdir -p /opt/software 
RUN mkdir -p /opt/software/resources
ADD panda.py /opt/software/ 

# Copy the bucket-based file into this Docker:
RUN wget https://storage.googleapis.com/mev-public-data/tissues_ppi.tsv -O /opt/software/resources/tissues_ppi.tsv
RUN wget https://storage.googleapis.com/mev-public-data/tissues_motif.tsv -O /opt/software/resources/tissues_motif.tsv

# Install the NetZoo python library
RUN wget https://github.com/netZoo/netZooPy/archive/refs/tags/0.8.1.tar.gz \
    -P /opt/software && \
    tar xzvf /opt/software/0.8.1.tar.gz -C /opt/software && \
    pip3 install -e /opt/software/netZooPy-0.8.1/ 
    
RUN pip3 install joblib

ENTRYPOINT ["/bin/bash"]
