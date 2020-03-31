import argparse
import json
from pathlib import Path

import nmslib
from cord_ann.embeddings import load_embedding_model, encode_sentences
from cord_ann.mapping import load_mapping


def extract_k_hits(result, sentence, articles, sent_article_mapping):
    ids, distances = result
    extracted = {
        "query": sentence,
        "hits": []
    }

    for id, distance in zip(ids, distances):
        mapping = sent_article_mapping[id]
        article_idx = mapping["article_idx"]
        paragraph_idx = mapping["paragraph_idx"]
        sentence_idx = mapping["sentence_idx"]
        article = articles[article_idx]
        extracted["hits"].append({
            "title": article['metadata']['title'],
            "authors": article['metadata']['authors'],
            "paragraph": article['body_text'][paragraph_idx],
            "sentence": article['body_text'][paragraph_idx]["sentences"][sentence_idx],
            "abstract": article['abstract']
        })
    return extracted


def format_results(results, sentences, articles, mapping):
    return [extract_k_hits(result=result,
                           sentence=query_sentence,
                           articles=articles,
                           sent_article_mapping=mapping) for query_sentence, result in zip(sentences, results)]


def search_index(sentences, model, batch_size, k, num_workers, articles, index, mapping):
    search_embeddings = encode_sentences(model=model,
                                         batch_size=batch_size,
                                         sentences=sentences)

    results = index.knnQueryBatch(search_embeddings, k=k, num_threads=num_workers)
    results = format_results(results=results,
                             sentences=sentences,
                             articles=articles,
                             mapping=mapping)
    return results


def add_search_args(parser):
    parser.add_argument('--index_path', default="index",
                        help='Path to the created index')
    parser.add_argument('--articles_path', default="cord_19.json",
                        help='Path to the extracted sentences')
    parser.add_argument('--mapping_path', default="sent_article_mapping.json",
                        help='Path to the generated mapping from the embeddings script')
    parser.add_argument('--model_name_or_path', default='bert-base-nli-mean-tokens')
    parser.add_argument('--batch_size', default=8, type=int,
                        help='Batch size for the transformer model encoding')
    parser.add_argument('--num_workers', default=8, type=int,
                        help='Number of workers to use when parallelizing the index search')
    parser.add_argument('--k', default=10, type=int,
                        help='The top K hits to return from the index')
    parser.add_argument('--device', default='cpu',
                        help='Set to cuda to use the GPU')
    return parser


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = add_search_args(parser)
    parser.add_argument('--input_path', default="sentences.txt")
    parser.add_argument('--output_path', default="search.json")
    args = parser.parse_args()
    sentences = Path(args.input_path).read_text().strip().split('\n')

    model = load_embedding_model(model_name_or_path=args.model_name_or_path,
                                 device=args.device)

    index = nmslib.init(method='hnsw', space='cosinesimil')
    index.loadIndex(args.index_path)

    sent_article_mapping = load_mapping(args.mapping_path)

    with open(args.articles_path) as f:
        articles = json.load(f)

    results = search_index(sentences=sentences,
                           model=model,
                           batch_size=args.batch_size,
                           k=args.k,
                           num_workers=args.num_workers,
                           articles=articles,
                           index=index,
                           mapping=sent_article_mapping)
    with open(args.output_path, 'w') as f:
        json.dump(results, f)
