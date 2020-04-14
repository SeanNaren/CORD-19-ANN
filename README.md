# CORD-19-ANN

![cord_website](./imgs/cord_ann_example.gif)

This repo allows searching through the [CORD-19](https://pages.semanticscholar.org/coronavirus-research) 
dataset using [S-BERT](https://github.com/UKPLab/sentence-transformers) embeddings via [nmslib](https://github.com/nmslib/nmslib/blob/master/python_bindings/README.md) or [faiss](https://github.com/facebookresearch/faiss).

Sentence embeddings are not perfect for searching (see [this issue](https://github.com/UKPLab/sentence-transformers/issues/174)) however can provide insight into the data that basic search functionality cannot. There is still room to improve the retrieval of relevant documents.

We're not versed in the medical field, so any feedback or improvements we deeply encourage in the form of issues/PRs!

We've included pre-trained models and the FAISS index to start your own server with instructions below.

Finally we provide a front-end that can be used to search through the dataset and extract information via a UI. Instructions and installation for the front-end can be found [here](frontend/README.md).

Currently we do not have a server running (if anyone can help that would be great!). We'll work to try provide the index and metadata such that setup is not required from scratch.

## Installation

### Source
We assume you have installed PyTorch and the necessary CUDA packages from [here](https://pytorch.org/). We suggest using Conda to make installation easier.
```

# Install FAISS
conda install faiss-cpu -c pytorch # Other instructions can be found at https://github.com/facebookresearch/faiss/blob/master/INSTALL.md

git clone https://github.com/SeanNaren/CORD-19-ANN.git --recursive
cd CORD-19-ANN/
pip install -r requirements.txt
pip install .

# If you plan to finetune SciBERT from scratch using mixed-precision
git clone https://github.com/NVIDIA/apex.git
cd apex/
pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
```

### Docker

We also provide a docker container:

```
docker pull seannaren/cord-19-ann
sudo docker run -it --net=host --ipc=host --entrypoint=/bin/bash --rm seannaren/cord-19-ann
```

## Download Models

We currently offer sentence models trained on [BlueBERT](https://github.com/ncbi-nlp/bluebert) (base uncased model) and [BioBERT](https://github.com/naver/biobert-pretrained) (base cased model) with the appropriate metadata/index. We currently serve S-BlueBERT however it is interchangeable.

```
# Choose which model you'd like to download
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/s-bluebert-pretrained.tar.gz 
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/s-biobert-pretrained.tar.gz
tar -xzvf s-bluebert-pretrained.tar.gz
tar -xzvf s-bluebert-pretrained.tar.gz

# Download index based on the above choice
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/bluebert_faiss_PCAR128_SQ8
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/biobert_faiss_PCAR128_SQ8

# Download metadata 
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/dataset_formatted_2020_03_27.tar.gz
tar -xzvf dataset_formatted_2020_03_27.tar.gz dataset_formatted/
```

## Searching the Index

We assume you've chosen the s-bluebert model, it should be straightforward to swap in any other pre-trained models offered in this repo by modifying the paths below.

We recommend using the server but we do offer a simple script to search given a text file of sentences:

```
echo "These RNA transcripts may be spliced to give rise to mRNAs encoding the envelope (Env) glycoproteins (Fig. 1a)" > sentences.txt
python search_index.py --index_path bluebert_faiss_PCAR128_SQ8 --index_type faiss --model_name_or_path s-bluebert-pretrained/ --articles_path dataset_formatted/journals/ --mapping_path dataset_formatted/cord_19_sent_to_article_mapping.json --input_path sentences.txt --output_path output.json
```

#### Using the server

To start the server:
```
YOUR_IP=0.0.0.0
YOUR_PORT=1337
python index_server.py --index_path bluebert_faiss_PCAR128_SQ8 --index_type faiss --model_name_or_path s-bluebert-pretrained/ --articles_path dataset_formatted/journals/ --mapping_path dataset_formatted/cord_19_sent_to_article_mapping.json --address $YOUR_IP --port $YOUR_PORT --silent
```

To test the server:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '["These RNA transcripts may be spliced to give rise to mRNAs encoding the envelope (Env) glycoproteins (Fig. 1a)"]' \
  http://$YOUR_IP:$YOUR_PORT/query
```

### Output Format

The output from the index is a JSON object containing the top K hits from the index, an example of the API is given below:

```
[
  {
    "query": "These RNA transcripts may be spliced to give rise to mRNAs encoding the envelope (Env) glycoproteins (Fig. 1a)",
    "hits": [
      {
        "title": "Title",
        "authors": [
          "..."
        ],
        "abstract": [
          "..."
        ],
        "paragraph": "Paragraph that included the hit",
        "sentence": "The semantically similar sentence",
        "distance": 42,
      }
    ]
  }
]
```

## Creating the Index from scratch

The process requires a GPU enabled node such as a GCP n8 node with a nvidia-tesla-v100 to generate the embeddings, with at-least 40GB RAM.

### Preparing the dataset

Currently we tokenize at the sentence level using SciSpacy, however future work may look into using paragraph level tokenization.

```
mkdir datasets/
python download_data.py --output_dir datasets/
python extract_sentences.py --input_path datasets/cord_19/ --num_workers 16
```

### Generating embeddings

#### Using fine-tuned BioBERT/BlueBERT

Using sentence-transformers we can fine-tune either model. BlueBERT offers only uncased models whereas BioBERT offer a cased model. We've converted them into PyTorch format and included them in releases, to download:

```
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/s-biobert-pretrained.tar.gz
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/s-bluebert-pretrained.tar.gz 
```

##### Using Pre-trained BioBERT/BlueBERT

```
python generate_embeddings.py --model_name_or_path s-biobert-pretrained/ --embedding_path biobert_embeddings.npy --device cuda --batch_size 256 # If you want to use biobert
python generate_embeddings.py --model_name_or_path s-bluebert-pretrained/ --embedding_path bluebert_embeddings.npy --device cuda --batch_size 256 # If you want to use bluebert
```

#### Using pre-trained S-BERT models

You can also use the standard pre-trained model from the S-BERT repo like below, however we suggest using the fine-tuned models offered in this repo.

```
python generate_embeddings.py --model_name_or_path bert-base-nli-mean-tokens --embedding_path pretrained_embeddings.npy --device cuda --batch_size 256
```

##### Training the model from scratch

This takes a few hours on a V100 GPU.

Once trained the model is saved to the `output/` folder by default. Inside there you'll find checkpoints such as `output/training_nli/biobert-2020-03-30_10-51-49/` after training has finished. Use this as the model path when generating your embeddings.

```
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/biobert-pretrained.tar.gz
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/bluebert-pretrained.tar.gz 

mkdkir datasets/
python sentence-transformers/examples/datasets/get_data.py --output_path datasets/
python sentence-transformers/examples/training_nli_transformers.py --model_name_or_path biobert-pretrained.tar.gz
python sentence-transformers/examples/training_nli_transformers.py --model_name_or_path bluebert-pretrained.tar.gz --do_lower_case
```

### Create the Index

We have the ability to use faiss or nmslib given the parameter below. We've exposed the FAISS config string for modifying the index. More details about selecting the index can be seen [here](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index).

```
python create_index.py --output_path index --embedding_path pretrained_embeddings.npy --index_type faiss # Swap to scibert_embeddings.npy if using fine-tuned SciBERT embeddings
```

### Clustering

We also took the example clustering script out of sentence-transformers and added it to this repository for using the pre-trained models. An example below:

```
python cluster_sentences.py --input_path sentences.txt --model_name_or_path s-scibert-pretrained/ --device cpu
```

## Acknowledgements

Thanks to the authors of the various libraries that made this possible!

- [sentence-transformers](https://github.com/UKPLab/sentence-transformers)
- [cord-19](https://pages.semanticscholar.org/coronavirus-research)
- [scibert](https://github.com/allenai/scibert)
- [nmslib](https://github.com/nmslib/nmslib)
- [FAISS](https://github.com/facebookresearch/faiss)