import argparse

import json
from multiprocessing.pool import Pool
from shutil import copyfile

from cord_ann.index import paths_from_dataset_path
from cord_ann.mapping import flatten_sentences, create_sentence_to_article_mapping
from tqdm import tqdm
from pathlib import Path
import spacy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Formats the CORD19 data into appropriate formats for indexing/searching and generating embeddings")
    parser.add_argument('--input_path', default="cord_19_dataset/")
    parser.add_argument('--output_dir', default="cord_19_dataset_formatted/")
    parser.add_argument('--num_workers', default=8, type=int)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    articles_path, sentences_path, mapping_path, metadata_path = paths_from_dataset_path(output_dir)

    articles_path.mkdir(parents=True, exist_ok=True)

    nlp = spacy.load("en_core_sci_sm")  # Use SciSpacy to tokenize into sentences
    articles_path = Path(args.input_path)
    articles = list(articles_path.rglob('*.json'))


    def _tokenize_paragraphs(journal):
        with journal.open('r') as f:
            journal = json.load(f)
        for x, paragraph in enumerate(journal['body_text']):
            paragraph = paragraph['text']
            doc = nlp(paragraph)
            sentences = [x.text for x in doc.sents]
            journal['body_text'][x]['sentences'] = sentences
        paper_id = journal['paper_id']
        output_path = articles_path / (paper_id + '.json')
        with output_path.open('w') as f:
            json.dump(journal, f)
        return journal


    with Pool(processes=args.num_workers) as pool:
        articles_tokenized = list(tqdm(pool.imap_unordered(_tokenize_paragraphs, articles), total=len(articles)))

    with open(sentences_path, 'w') as f:
        f.write('\n'.join(flatten_sentences(articles_tokenized)))
    with open(mapping_path, 'w') as f:
        sent_article_mapping = create_sentence_to_article_mapping(articles_tokenized)
        json.dump(sent_article_mapping, f)

    # Copy the metadata.csv file to the formatted directory
    copyfile(metadata_path, output_dir / 'metadata.csv')
