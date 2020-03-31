import argparse

import json
from multiprocessing.pool import Pool

from tqdm import tqdm
from pathlib import Path
import spacy

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', default="datasets/cord_19/")
    parser.add_argument('--output_path', default="cord_19.json")
    parser.add_argument('--num_workers', default=8, type=int)
    args = parser.parse_args()

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

    with open(args.output_path, 'w') as f:
        json.dump(articles_tokenized, f)
