import argparse

import numpy as np

from cord_ann.embeddings import EmbeddingModel

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sentences_path', default="datasets/cord_19/cord_19_sentences.txt",
                        help='Path to extracted sentences')
    parser.add_argument('--embedding_path', default="embeddings.npy",
                        help='Output path of the generated embeddings')
    parser.add_argument('--model_name_or_path', default='bert-base-nli-mean-tokens')
    parser.add_argument('--batch_size', default=8, type=int)
    parser.add_argument('--device', default='cuda')
    args = parser.parse_args()

    with open(args.sentences_path) as f:
        sentences = f.read().split('\n')

    model = EmbeddingModel(model_name_or_path=args.model_name_or_path,
                           device=args.device,
                           batch_size=args.batch_size)
    sentence_embeddings = model.encode_sentences(sentences=sentences)

    np.save(args.embedding_path, sentence_embeddings)
