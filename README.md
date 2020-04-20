# CORD-19-ANN

![cord_website](imgs/cord_ann_example.gif)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/137jbpY3yQJGSzlLHZGUYBk5F78bwuqKJ) [![Open In Colab](https://github.com/aleen42/badges/raw/master/src/medium.svg)](https://medium.com/@seannaren/cord-19-ann-semantic-search-engine-using-s-bert-aebc5bcc5442?sk=92ea4a22df3cd1343c86a1e880b78f6f) [GitHub Pages](https://seannaren.github.io/CORD-19-ANN/)

This repo contains the scripts and models to search [CORD-19](https://pages.semanticscholar.org/coronavirus-research) using [S-BERT](https://github.com/UKPLab/sentence-transformers) embeddings via [nmslib](https://github.com/nmslib/nmslib/blob/master/python_bindings/README.md) or [faiss](https://github.com/facebookresearch/faiss).

Sentence embeddings are not perfect for searching (see [this issue](https://github.com/UKPLab/sentence-transformers/issues/174)) however can provide insight into the data that basic search functionality cannot. There is still room to improve the retrieval of relevant documents.

We're not versed in the medical field, so any feedback or improvements we deeply encourage in the form of issues/PRs!

We've included pre-trained models and the FAISS index to start your own server with instructions below.

Finally we provide a front-end that can be used to search through the dataset and extract information via a UI. Instructions and installation for the front-end can be found [here](frontend/README.md).

We currently are hosting the server on a gcp instance, if anyone can contribute for a more permanent hosting solution it would be appreciated.

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
```

### Docker

We also provide a docker container:

```
docker pull seannaren/cord-19-ann
sudo docker run -it --net=host --ipc=host --entrypoint=/bin/bash --rm seannaren/cord-19-ann
```

## Download Models

We currently offer sentence models trained on [BlueBERT](https://github.com/ncbi-nlp/bluebert) (base uncased model) and [BioBERT](https://github.com/naver/biobert-pretrained) (base cased model) with the appropriate metadata/index. We currently serve S-BlueBERT however it is interchangeable.


### Download S-BERT Models and Search Index

Download the corresponding Model and Index file. We suggest using S-BioBERT and assume you have done so for the subsequent commands. They are interchangeable however.

| Model                       | Index                          | Test MedNLI Accuracy | Test STS Benchmark Cosine Pearson |
|-----------------------------|--------------------------------|-----------------|------------------------------|
| [S-BioBERT Base Cased](https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/s-biobert_base_cased_mli.tar.gz)    | [BioBERT_faiss_PCAR128_SQ8](https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/biobert_mli_faiss_PCAR128_SQ8)  | 0.7482          | 0.7122                       |
| [S-BlueBERT Base Uncased](https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/s-bluebert_base_uncased_mli.tar.gz) | [BlueBERT_faiss_PCAR128_SQ8](https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/bluebert_mli_faiss_PCAR128_SQ8) | 0.7525          | 0.6923                       |
| S-Bert Base Cased             |                                | 0.5689          | 0.7265                       |


### Download Metadata
```
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/cord_19_dataset_formatted_2020_03_27.tar.gz
tar -xzvf cord_19_dataset_formatted_2020_03_27.tar.gz cord_19_dataset_formatted/
```

## Searching the Index

We assume you've chosen the s-biobert model, it should be straightforward to swap in any other pre-trained models offered in this repo by modifying the paths below.

We recommend using the server but we do offer a simple script to search given a text file of sentences:

```
echo "These RNA transcripts may be spliced to give rise to mRNAs encoding the envelope (Env) glycoproteins (Fig. 1a)" > sentences.txt
python search_index.py --index_path biobert_mli_faiss_PCAR128_SQ8 --index_type faiss --model_name_or_path s-biobert_base_cased_mli/ --dataset_path cord_19_dataset_formatted/ --input_path sentences.txt --output_path output.json
```

#### Using the server

To start the server:
```
YOUR_IP=0.0.0.0
YOUR_PORT=1337
python index_server.py --index_path biobert_mli_faiss_PCAR128_SQ8 --index_type faiss --model_name_or_path s-biobert_base_cased_mli/ --dataset_path cord_19_dataset_formatted/ --address $YOUR_IP --port $YOUR_PORT --silent
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

The process requires a GPU enabled node such as a GCP n8 node with a nvidia-tesla-v100 to generate the embeddings, with at-least 20GB RAM.

### Preparing the dataset

Currently we tokenize at the sentence level using SciSpacy, however future work may look into using paragraph level tokenization.

```
mkdir datasets/
python download_data.py
python extract_sentences.py --num_workers 16
```

### Generating embeddings

#### Using fine-tuned BioBERT/BlueBERT

Using sentence-transformers we can fine-tune either model. BlueBERT offers only uncased models whereas BioBERT offer a cased model. We've converted them into PyTorch format and included them in releases, to download:

```
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/s-biobert_base_cased_mli.tar.gz
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/s-bluebert_base_uncased_mli.tar.gz
tar -xzvf s-biobert_base_cased_mli.tar.gz
tar -xzvf s-bluebert_base_uncased_mli.tar.gz
```

##### Using Pre-trained BioBERT/BlueBERT

```
python generate_embeddings.py --model_name_or_path s-biobert_base_cased_mli/ --embedding_path biobert_embeddings.npy --device cuda --batch_size 256 # If you want to use biobert
python generate_embeddings.py --model_name_or_path s-bluebert_base_uncased_mli/ --embedding_path bluebert_embeddings.npy --device cuda --batch_size 256 # If you want to use bluebert
```

#### Using pre-trained S-BERT models

You can also use the standard pre-trained model from the S-BERT repo like below, however we suggest using the fine-tuned models offered in this repo.

```
python generate_embeddings.py --model_name_or_path bert-base-nli-mean-tokens --embedding_path pretrained_embeddings.npy --device cuda --batch_size 256
```

##### Training the model from scratch

This takes a few hours on a V100 GPU.

If you'd like to include the MedNLI dataset during training, you'll need to download the dataset from [here](https://physionet.org/content/mednli/1.0.0/). Getting access requires credentialed access which requires some efforts and a waiting period of up to two weeks.

Once trained the model is saved to the `output/` folder by default. Inside there you'll find checkpoints such as `output/training_nli/biobert-2020-03-30_10-51-49/` after training has finished. Use this as the model path when generating your embeddings.

```
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/biobert_cased_v1.1.tar.gz
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/bluebert_base_uncased.tar.gz
tar -xzvf biobert_cased_v1.1.tar.gz
tar -xzvf bluebert_base_uncased.tar.gz

mkdkir datasets/
python sentence-transformers/examples/datasets/get_data.py --output_path datasets/
python sentence-transformers/examples/training_nli_transformers.py --model_name_or_path biobert_cased_v1.1/
python sentence-transformers/examples/training_nli_transformers.py --model_name_or_path bluebert_base_uncased/ --do_lower_case

# Training with medNLI
python sentence-transformers/examples/training_nli_transformers.py --model_name_or_path biobert_cased_v1.1/ --mli_dataset_path path/to/mednli/
python sentence-transformers/examples/training_nli_transformers.py --model_name_or_path bluebert_base_uncased/ --mli_dataset_path path/to/mednli/ --do_lower_case
```

### Create the Index

We have the ability to use faiss or nmslib given the parameter below. We've exposed the FAISS config string for modifying the index. More details about selecting the index can be seen [here](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index).

```
python create_index.py --output_path index --embedding_path pretrained_embeddings.npy --index_type faiss # Swap to scibert_embeddings.npy if using fine-tuned SciBERT embeddings
```

### Clustering

We also took the example clustering script out of sentence-transformers and added it to this repository for using the pre-trained models. An example below:

```
python cluster_sentences.py --input_path sentences.txt --model_name_or_path biobert_cased_v1.1/ --device cpu
```

There is also a more interactive version available using the Google Colab demo: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/137jbpY3yQJGSzlLHZGUYBk5F78bwuqKJ) 

## Acknowledgements

Thanks to the authors of the various libraries that made this possible!

- [sentence-transformers](https://github.com/UKPLab/sentence-transformers)
- [cord-19](https://pages.semanticscholar.org/coronavirus-research)
- [scibert](https://github.com/allenai/scibert)
- [nmslib](https://github.com/nmslib/nmslib)
- [FAISS](https://github.com/facebookresearch/faiss)