import argparse
from pathlib import Path

from cord_ann.clusters import cluster_embeddings
from cord_ann.embeddings import load_embedding_model, encode_sentences

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Takes a text file of sentences and applies clustering '
                                                 'based on a pre-trained sentence embedding model')
    parser.add_argument('--input_path', default='sentences.txt')
    parser.add_argument('--model_name_or_path', default='bert-base-nli-mean-tokens')
    parser.add_argument('--batch_size', default=8, type=int,
                        help='Batch size for the transformer model encoding')
    parser.add_argument('--device', default='cpu',
                        help='Set to cuda to use the GPU')
    parser.add_argument('--num_clusters', default=5, type=int,
                        help='Number of clusters for Kmeans')
    args = parser.parse_args()
    sentences = Path(args.input_path).read_text().split('\n')
    model = load_embedding_model(model_name_or_path=args.model_name_or_path,
                                 device=args.device)

    embeddings = encode_sentences(model=model,
                                  batch_size=args.batch_size,
                                  sentences=sentences)
    clusters = cluster_embeddings(sentences=sentences,
                                  embeddings=embeddings,
                                  num_clusters=args.num_clusters)

    for i, cluster in enumerate(clusters):
        print("Cluster ", i + 1)
        print(cluster)
        print("")
