import argparse

import numpy

parser = argparse.ArgumentParser()
parser.add_argument('--embedding_path', default="embeddings.npy",
                    help='Path to generated embeddings.')
parser.add_argument('--output_path', default="index",
                    help='Path to save index')
parser.add_argument('--index_type', default="nmslib", type=str, choices=["nmslib", "faiss"],
                    help='Type of index you want like to create')
parser.add_argument('--faiss_config', default='PCAR256,SQ8', type=str,
                    help='FAISS offers a large selection of parameters that can be seen here:'
                         'https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index')
if __name__ == "__main__":
    args = parser.parse_args()

    embeddings = numpy.load(args.embedding_path)

    if args.index_type == 'nmslib':
        import nmslib

        index = nmslib.init(method='hnsw', space='cosinesimil')
        index.addDataPointBatch(embeddings)
        index.createIndex({'post': 2}, print_progress=True)
        index.saveIndex(args.output_path, save_data=False)
    elif args.index_type == 'faiss':
        import faiss

        d = embeddings.shape[-1]
        index = faiss.index_factory(d, args.faiss_config)  # build the index
        if not index.is_trained:
            print("Training index.")
            index.train(embeddings)
        print("Adding embeddings to index.")
        index.add(embeddings)  # add vectors to the index
        print(index.ntotal)
        print("Saving index.")
        faiss.write_index(index, args.output_path)
