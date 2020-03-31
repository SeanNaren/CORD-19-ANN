import argparse

import nmslib
import numpy

parser = argparse.ArgumentParser()
parser.add_argument('--embedding_path', default="embeddings.npy",
                    help='Path to generated embeddings.')
parser.add_argument('--output_path', default="index",
                    help='Path to save index')

if __name__ == "__main__":
    args = parser.parse_args()
    embeddings = numpy.load(args.embedding_path)

    index = nmslib.init(method='hnsw', space='cosinesimil')
    index.addDataPointBatch(embeddings)
    index.createIndex({'post': 2}, print_progress=True)
    index.saveIndex(args.output_path, save_data=False)
