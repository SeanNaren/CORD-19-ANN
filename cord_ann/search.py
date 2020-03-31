from cord_ann.embeddings import encode_sentences


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
