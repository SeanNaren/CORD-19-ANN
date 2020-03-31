FROM pytorch/pytorch:1.4-cuda10.1-cudnn7-devel

RUN apt-get update && apt-get install -y --no-install-recommends \
         cmake \
         ca-certificates \
         build-essential &&\
     rm -rf /var/lib/apt/lists/*

RUN conda install scipy scikit-learn
RUN conda install -c conda-forge spacy

WORKDIR /workspace/

# Install apex
RUN git clone --recursive https://github.com/NVIDIA/apex.git
RUN cd apex; pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./

# Install CORD-19-ANN
ADD . /workspace/CORD-19-ANN

WORKDIR /workspace/CORD-19-ANN

# Pre-requisities. Eventually once fixed move to transformers latest release
RUN pip install pysbd sentencepiece transformers==2.4.1
RUN pip install -r requirements.txt
RUN pip install .

ENTRYPOINT ["/opt/conda/bin/python"]