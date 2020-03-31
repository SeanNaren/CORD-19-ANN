# CORD-19-ANN

This repo allows us to search through the [CORD-19](https://pages.semanticscholar.org/coronavirus-research) 
dataset using [S-BERT](https://github.com/UKPLab/sentence-transformers) embeddings via [nmslib](https://github.com/nmslib/nmslib/blob/master/python_bindings/README.md). 

We include instructions to finetune [SciBERT](https://github.com/allenai/scibert) on the NLI dataset using a modified Sentence Transformers package to improve understanding of scientific text.

Finally we provide a front-end that can be used to search through the journals and extract information via a UI. Instructions and installation for the front-end can be found [here](TODO).

### Installation

We assume you have installed PyTorch and the necessary CUDA packages from [here](https://pytorch.org/).
```
git clone https://github.com/SeanNaren/CORD-19-ANN.git --recursive
cd CORD-19-ANN
pip install -r requirements.txt
pip install .
```

## Pre-trained Search

Coming Soon!

## From Scratch

The process requires a GPU enabled node such as a GCP n8 node with a nvidia-tesla-v100 with atleast 40GB RAM. The Index requires around 20GB and the embeddings another 19GB.

## Format CORD-19 Data

Currently we tokenize at the sentence level using SciSpacy, however future work may look into using paragraph level tokenization.

```
mkdir datasets/
python download_data.py --output_path datasets/cord_19/
python extract_sentences.py --input_path datasets/cord_19/ --output_path cord_19.json --num_workers 16
```

## Generating embeddings
 
### Using pre-trained SBERT

```
python generate_embeddings.py --input_path cord_19.json --output_path pretrained_embeddings.npy --device cuda --batch_size 256
```

### Using fine-tuned SciBERT

Currently we don't offer pre-trained models, thus we'll need to train from scratch. This takes a few hours on a GCP n8 node with a nvidia-tesla-v100.

Once trained the model is saved to the `output/` folder by default. Inside there you'll find checkpoints such as `output/training_nli_allenai/scibert_scivocab_cased-2020-03-30_10-51-49/` after training has finished. Use this as the model path when generating your embeddings.
```
python sentence-transformers/examples/datasets/get_data.py --output_path datasets/
python sentence-transformers/examples/training_nli_transformers.py --model_name_or_path allenai/scibert_scivocab_cased
python generate_embeddings.py --model_name_or_path output/{REPLACE PATH TO MODEL HERE} --output_path scibert_embeddings.py
```

## Create the Index

```
python create_index.py --output_path index --embedding_path pretrained_embeddings.npy # Swap to scibert_embeddings.py if using fine-tuned SciBERT embeddings
python search_index.py --index_path index  --device cpu -k 10 --input_path sentences.txt --output_path output.json
```

## Searching the Index

We recommend using the server but we do offer a simple script to search given a text file of sentences:

```
echo "These RNA transcripts may be spliced to give rise to mRNAs encoding the envelope (Env) glycoproteins (Fig. 1a)" > sentences.txt
python search_index.py --index_path index  --device cpu --input_path sentences.txt --output_path output.json
```

### Server

To start the server:
```
YOUR_IP=0.0.0.0
YOUR_PORT=1337
python index_server.py --index_path index --device cpu --address $YOUR_IP --port $YOUR_PORT -k 10
```

To test the server:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '["These RNA transcripts may be spliced to give rise to mRNAs encoding the envelope (Env) glycoproteins (Fig. 1a)"]' \
  http://YOUR_IP:YOUR_PORT/query
```

## Output

The output from the index is a JSON object containing the top K hits from the index, an example of the API is given below:

```

```