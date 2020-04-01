import argparse

import json
from multiprocessing.pool import Pool

from cord_ann.mapping import flatten_sentences, create_mapping
from tqdm import tqdm
from pathlib import Path
import spacy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Formats the CORD19 data into appropriate formats for indexing/searching and generating embeddings")
    parser.add_argument('--input_path', default="datasets/cord_19/")
    parser.add_argument('--output_dir', default="datasets/")
    parser.add_argument('--num_workers', default=8, type=int)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

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
        return journal


    with Pool(processes=args.num_workers) as pool:
        articles_tokenized = list(tqdm(pool.imap_unordered(_tokenize_paragraphs, articles), total=len(articles)))

    with open(output_dir / 'cord_19.json', 'w') as f:
        json.dump(articles_tokenized, f)
    with open(output_dir / 'cord_19_sentences.txt') as f:
        f.write('\n'.join(flatten_sentences(articles)))
    with open(output_dir / 'cord_19_sent_to_article_mapping.json') as f:
        sent_article_mapping = create_mapping(articles)
        json.dump(sent_article_mapping, f)