FROM ubuntu:18.04

ARG PYTHON_VERSION=3.7
RUN apt-get update && apt-get install -y --no-install-recommends \
         build-essential \
         cmake \
         git \
         wget \
         ca-certificates \
         libjpeg-dev \
         libpng-dev && \
     rm -rf /var/lib/apt/lists/*


RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /opt/conda && \
     rm ~/miniconda.sh && \
     /opt/conda/bin/conda install -y python=$PYTHON_VERSION numpy pyyaml scikit-learn scipy ipython mkl mkl-include ninja cython typing && \
     /opt/conda/bin/conda clean -ya
ENV PATH /opt/conda/bin:$PATH

RUN conda install pytorch cpuonly faiss-cpu -c pytorch
RUN conda install -c conda-forge spacy

WORKDIR /workspace/

# Install CORD-19-ANN
ADD . /workspace/CORD-19-ANN

WORKDIR /workspace/CORD-19-ANN

# Pre-requisities. Errors out if not installed before running requirments install
RUN pip install pysbd sentencepiece transformers
RUN pip install -r requirements.txt
RUN pip install .

ENTRYPOINT ["/opt/conda/bin/python"]