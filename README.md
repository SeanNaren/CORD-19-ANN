# CORD-19-ANN

![cord_website](./imgs/cord_ann_example.gif)

This repo allows searching through the [CORD-19](https://pages.semanticscholar.org/coronavirus-research) 
dataset using [S-BERT](https://github.com/UKPLab/sentence-transformers) embeddings via [nmslib](https://github.com/nmslib/nmslib/blob/master/python_bindings/README.md). 

We're not versed in the medical field, so any feedback or improvements we deeply encourage in the form of issues/PRs!

We include a the pre-trained SciBERT model and instructions to finetune [SciBERT](https://github.com/allenai/scibert) which has ben trained on scientific text, on the NLI dataset using a modified Sentence Transformers package.

Finally we provide a front-end that can be used to search through the dataset and extract information via a UI. Instructions and installation for the front-end can be found [here](frontend/README.md).

Currently we do not have a server running (if anyone can help that would be great!). We'll work to try provide the index and metadata such that setup is not required from scratch.

We do however provide the pre-trained SciBERT model, which can be downloaded following the instructions below. 

## Installation

### Source
We assume you have installed PyTorch and the necessary CUDA packages from [here](https://pytorch.org/).
```
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

We also provide a docker container if preferred:

```
docker pull seannaren/cord-19-ann
```

## From Scratch

The process requires a GPU enabled node such as a GCP n8 node with a nvidia-tesla-v100 with atleast 40GB RAM. The Index requires around 20GB and the embeddings another 19GB.

### Preparing the dataset

Currently we tokenize at the sentence level using SciSpacy, however future work may look into using paragraph level tokenization.

```
mkdir datasets/
python download_data.py --output_dir datasets/
python extract_sentences.py --input_path datasets/cord_19/ --num_workers 16
```

### Generating embeddings

#### Using fine-tuned SciBERT

##### Using Pre-trained SciBERT

```
wget https://github.com/SeanNaren/CORD-19-ANN/releases/download/V1.0/s-scibert-pretrained.tar.gz
python generate_embeddings.py --model_name_or_path s-scibert-pretrained/ --embedding_path scibert_embeddings.npy --device cuda --batch_size 256
```

#### Using pre-trained S-BERT

You can also use the standard pre-trained model from the S-BERT repo like below.

```
python generate_embeddings.py --model_name_or_path bert-base-nli-mean-tokens --embedding_path pretrained_embeddings.npy --device cuda --batch_size 256
```

##### Training the model from scratch

This takes a few hours on a GCP n8 node with a nvidia-tesla-v100.

Once trained the model is saved to the `output/` folder by default. Inside there you'll find checkpoints such as `output/training_nli_allenai/scibert_scivocab_cased-2020-03-30_10-51-49/` after training has finished. Use this as the model path when generating your embeddings.
```
python sentence-transformers/examples/datasets/get_data.py --output_path datasets/
python sentence-transformers/examples/training_nli_transformers.py --model_name_or_path allenai/scibert_scivocab_cased
```

### Create the Index

```
python create_index.py --output_path index --embedding_path pretrained_embeddings.npy # Swap to scibert_embeddings.npy if using fine-tuned SciBERT embeddings
```

### Searching the Index

We recommend using the server but we do offer a simple script to search given a text file of sentences:

```
echo "These RNA transcripts may be spliced to give rise to mRNAs encoding the envelope (Env) glycoproteins (Fig. 1a)" > sentences.txt
python search_index.py --index_path index --model_name_or_path bert-base-nli-mean-tokens --device cpu --input_path sentences.txt --output_path output.json
```

If you're using the finetuned SciBERT model, make sure to update the command accordingly:

```
echo "These RNA transcripts may be spliced to give rise to mRNAs encoding the envelope (Env) glycoproteins (Fig. 1a)" > sentences.txt
python search_index.py --index_path index --model_name_or_path s-scibert-pretrained/ --device cpu --input_path sentences.txt --output_path output.json
```

#### Using the server

To start the server:
```
YOUR_IP=0.0.0.0
YOUR_PORT=1337
python index_server.py --index_path index --model_name_or_path bert-base-nli-mean-tokens --device cpu --address $YOUR_IP --port $YOUR_PORT -k 10
```

If you're using the finetuned SciBERT model, make sure to update the command accordingly:

```
python index_server.py --index_path index --model_name_or_path s-scibert-pretrained/ --device cpu --address $YOUR_IP --port $YOUR_PORT -k 10
```

To test the server:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '["These RNA transcripts may be spliced to give rise to mRNAs encoding the envelope (Env) glycoproteins (Fig. 1a)"]' \
  http://YOUR_IP:YOUR_PORT/query
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
        "sentence": "The semantically similar sentence"
      }
    ]
  }
]
```

## Citation and Acknowledgements

Thanks to the authors of the various libraries that made this possible!

### [sentence-transformers](https://github.com/UKPLab/sentence-transformers)
```
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "http://arxiv.org/abs/1908.10084",
}
```

### [cord-19](https://pages.semanticscholar.org/coronavirus-research)
```
COVID-19 Open Research Dataset (CORD-19). 2020. Version 2020-03-20. Retrieved from https://pages.semanticscholar.org/coronavirus-research. Accessed YYYY-MM-DD. doi:10.5281/zenodo.3715505
```

### [scibert](https://github.com/allenai/scibert)
```
@inproceedings{Beltagy2019SciBERT,
  title={SciBERT: Pretrained Language Model for Scientific Text},
  author={Iz Beltagy and Kyle Lo and Arman Cohan},
  year={2019},
  booktitle={EMNLP},
  Eprint={arXiv:1903.10676}
}
```

### [nmslib](https://github.com/nmslib/nmslib)