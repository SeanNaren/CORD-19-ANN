import argparse
import json

import tornado.ioloop
import tornado.web

from cord_ann.embeddings import EmbeddingModel
from cord_ann.index import search_args, Index
from cord_ann.mapping import load_sentence_to_article_mapping


class QueryHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def data_received(self, chunk):
        pass

    def initialize(self, args, model, index):
        self.args = args
        self.index = index
        self.model = model

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def post(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            sentences = json.loads(self.request.body)
            is_json = True
        else:
            sentences = [self.request.body.decode("utf-8")]
            is_json = False
        search_embeddings = self.model.encode_sentences(sentences=sentences)
        results = self.index.search_index(sentences=sentences,
                                          search_embeddings=search_embeddings)
        results = results if is_json else results[0]  # Assume if not json, it was a single sentence
        self.write(json.dumps(results, ensure_ascii=False))
        self.finish()


def make_app(args):
    return tornado.web.Application([
        ('/query', QueryHandler, args),
    ], debug=True, autoreload=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = search_args(parser)
    parser.add_argument('--port', default=8888, type=int)
    parser.add_argument('--address', default="")
    args = parser.parse_args()
    sent_article_mapping = load_sentence_to_article_mapping(args.mapping_path)

    model = EmbeddingModel(model_name_or_path=args.model_name_or_path,
                           device=args.device,
                           batch_size=args.batch_size,
                           show_progress_bar=not args.silent)

    index = Index(index_path=args.index_path,
                  index_type=args.index_type,
                  articles_path=args.articles_path,
                  mapping=sent_article_mapping,
                  k=args.k,
                  num_workers=args.num_workers)

    app_arguments = {
        'args': args,
        'model': model,
        'index': index,
    }
    app = make_app(args=app_arguments)
    print("Index Server is listening...")
    app.listen(port=args.port,
               address=args.address)
    tornado.ioloop.IOLoop.current().start()
