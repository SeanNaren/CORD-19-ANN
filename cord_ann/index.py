import json
from pathlib import Path

import numpy as np


class Index:
    def __init__(self, index_path, index_type, articles_path, mapping, k, num_workers):
        self.index = self.load_index(index_path, index_type)
        self.index_type = index_type
        self.articles_path = articles_path
        self.mapping = mapping
        self.k = k
        self.num_workers = num_workers

    def load_index(self, index_path, index_type):
        if index_type == 'nmslib':
            import nmslib
            index = nmslib.init(method='hnsw', space='cosinesimil')
            index.loadIndex(index_path)
        elif index_type == 'faiss':
            import faiss
            index = faiss.read_index(index_path)
        else:
            raise TypeError('Index type can only be faiss or nmslib.')
        return index

    def search_index(self, sentences, search_embeddings, return_batch_ids=False):
        if self.index_type == 'nmslib':
            batch = self.index.knnQueryBatch(search_embeddings,
                                             k=self.k,
                                             num_threads=self.num_workers)
            batch = np.array(batch)
            batch_ids = batch[:, 0].astype(np.int)
            batch_distances = batch[:, 1].astype(np.float32)
        elif self.index_type == 'faiss':
            batch_distances, batch_ids = self.index.search(np.array(search_embeddings), k=self.k)
        else:
            raise TypeError('Index type can only be faiss or nmslib.')

        results = self._format_results(batch_ids=batch_ids,
                                       batch_distances=batch_distances,
                                       sentences=sentences,
                                       articles_path=self.articles_path,
                                       mapping=self.mapping)
        if return_batch_ids:
            return results, batch_ids
        return results

    def _load_article(self, articles_path, paper_id):
        json_path = Path(articles_path) / (paper_id + '.json')
        with json_path.open() as f:
            article = json.load(f)
        return article

    def _extract_k_hits(self, ids, distances, sentence, articles_path, sent_article_mapping):
        extracted = {
            "query": sentence,
            "hits": []
        }

        for id, distance in zip(ids, distances):
            mapping = sent_article_mapping[id]
            paragraph_idx = mapping["paragraph_idx"]
            sentence_idx = mapping["sentence_idx"]
            article = self._load_article(articles_path=articles_path,
                                         paper_id=mapping["paper_id"])
            extracted["hits"].append({
                "title": article['metadata']['title'],
                "authors": article['metadata']['authors'],
                "paragraph": article['body_text'][paragraph_idx],
                "sentence": article['body_text'][paragraph_idx]["sentences"][sentence_idx],
                "abstract": article['abstract'],
                "distance": float(distance)
            })
        return extracted

    def _format_results(self, batch_ids, batch_distances, sentences, articles_path, mapping):
        return [self._extract_k_hits(ids=batch_ids[x],
                                     distances=batch_distances[x],
                                     sentence=query_sentence,
                                     articles_path=articles_path,
                                     sent_article_mapping=mapping) for x, query_sentence in enumerate(sentences)]


def search_args(parser):
    parser.add_argument('--index_path', default="index",
                        help='Path to the created index')
    parser.add_argument('--index_type', default="nmslib", type=str, choices=["nmslib", "faiss"],
                        help='Type of index')
    parser.add_argument('--articles_path', default="datasets/cord_19/cord_19.json",
                        help='Path to the extracted sentences')
    parser.add_argument('--mapping_path', default="datasets/cord_19/cord_19_sent_to_article_mapping.json",
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
    parser.add_argument('--silent', action="store_true",
                        help='Turn off progress bar when searching')
    return parser
