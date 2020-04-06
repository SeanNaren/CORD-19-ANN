import argparse
import json

import numpy as np

from cord_ann.embeddings import load_embedding_model, encode_sentences
from cord_ann.mapping import flatten_sentences, create_sentence_to_article_mapping

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--articles_path', default="datasets/cord_19/cord_19.json",
                        help='Path to extracted sentences')
    parser.add_argument('--embedding_path', default="embeddings.npy",
                        help='Output path of the generated embeddings')
    parser.add_argument('--mapping_path', default="datasets/cord_19/cord_19_sent_to_article_mapping.json",
                        help='Output path of the sentence to article mapping to find original document')
    parser.add_argument('--model_name_or_path', default='bert-base-nli-mean-tokens')
    parser.add_argument('--batch_size', default=8, type=int)
    parser.add_argument('--device', default='cuda')
    args = parser.parse_args()

    with open(args.articles_path) as f:
        articles = json.load(f)

    sentences = flatten_sentences(articles)
    sent_article_mapping = create_sentence_to_article_mapping(articles)
    model = load_embedding_model(model_name_or_path=args.model_name_or_path,
                                 device=args.device)
    sentence_embeddings = encode_sentences(model=model,
                                           batch_size=args.batch_size,
                                           sentences=sentences)

    np.save(args.embedding_path, sentence_embeddings)
    with open(args.mapping_path, 'w') as f:
        json.dump(sent_article_mapping, f)
