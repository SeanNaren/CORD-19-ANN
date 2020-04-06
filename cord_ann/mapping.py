import json

from tqdm import tqdm


def create_sentence_to_article_mapping(articles):
    mapping = []
    for article in tqdm(enumerate(articles), total=len(articles)):
        for paragraph_idx, paragraph in enumerate(article['body_text']):
            sentence_mappings = [{
                "sentence_idx": sentence_idx,
                "paper_id": article['paper_id'],
                "paragraph_idx": paragraph_idx
            } for sentence_idx in range(len(paragraph['sentences']))]
            mapping += sentence_mappings
    return mapping


def load_sentence_to_article_mapping(mapping_path):
    with open(mapping_path) as f:
        mapping = json.load(f)
    return mapping


def flatten_sentences(articles):
    flattened_sentences = []
    for article in tqdm(articles, total=len(articles)):
        for paragraph in article['body_text']:
            sentences = paragraph['sentences']
            flattened_sentences += sentences
    return flattened_sentences
