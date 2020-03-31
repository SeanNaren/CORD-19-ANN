import json

from tqdm import tqdm


def create_mapping(articles):
    mapping = []
    for article_idx, article in tqdm(enumerate(articles), total=len(articles)):
        for paragraph_idx, paragraph in enumerate(article['body_text']):
            sentence_mappings = [{
                "sentence_idx": sentence_idx,
                "article_idx": article_idx,
                "paragraph_idx": paragraph_idx
            } for sentence_idx in range(len(paragraph['sentences']))]
            mapping += sentence_mappings
    return mapping


def load_mapping(mapping_path):
    with open(mapping_path) as f:
        mapping = json.load(f)
    return mapping


def flatten_sentences(articles):
    flattened_sentences = []
    for article_idx, article in tqdm(enumerate(articles), total=len(articles)):
        for paragraph_idx, paragraph in enumerate(article['body_text']):
            sentences = paragraph['sentences']
            flattened_sentences += sentences
    return flattened_sentences
