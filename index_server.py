import argparse
import json

import nmslib
import tornado.ioloop
import tornado.web
from cord_ann.mapping import load_mapping

from search_index import search_index, add_search_args
from cord_ann.embeddings import load_embedding_model


class QueryHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def data_received(self, chunk):
        pass

    def initialize(self, args, model, articles, index, sent_article_mapping):
        self.args = args
        self.articles = articles
        self.index = index
        self.model = model
        self.sent_article_mapping = sent_article_mapping

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
        results = search_index(sentences=sentences,
                               model=self.model,
                               batch_size=self.args.batch_size,
                               k=self.args.k,
                               num_workers=self.args.num_workers,
                               articles=self.articles,
                               index=self.index,
                               mapping=self.sent_article_mapping)
        results = results if is_json else results[0]  # Assume if not json, it was a single sentence
        self.write(json.dumps(results, ensure_ascii=False))
        self.finish()


def make_app(args):
    return tornado.web.Application([
        ('/query', QueryHandler, args),
    ], debug=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = add_search_args(parser)
    parser.add_argument('--port', default=8888, type=int)
    parser.add_argument('--address', default="")
    args = parser.parse_args()

    model = load_embedding_model(model_name_or_path=args.model_name_or_path,
                                 device=args.device)

    index = nmslib.init(method='hnsw', space='cosinesimil')
    index.loadIndex(args.index_path)

    sent_article_mapping = load_mapping(args.mapping_path)

    with open(args.articles_path) as f:
        articles = json.load(f)
    app_arguments = {
        'args': args,
        'model': model,
        'articles': articles,
        'index': index,
        'sent_article_mapping': sent_article_mapping
    }
    app = make_app(args=app_arguments)
    print("Index Server is listening...")
    app.listen(port=args.port,
               address=args.address)
    tornado.ioloop.IOLoop.current().start()
