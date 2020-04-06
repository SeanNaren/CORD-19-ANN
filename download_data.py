import argparse
import os
import urllib.request
import tarfile

from tqdm import tqdm

datasets = ['comm_use_subset.tar.gz', 'noncomm_use_subset.tar.gz', 'custom_license.tar.gz']
server = "https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-04-03/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_path', default="datasets/cord_19/")
    args = parser.parse_args()
    os.makedirs(args.output_path, exist_ok=True)

    print('Beginning download of datasets')
    for dataset in tqdm(datasets, total=len(datasets)):
        url = server + dataset
        dataset_path = os.path.join(args.output_path, dataset)
        urllib.request.urlretrieve(url, dataset_path)

        print("Extracting", dataset)

        tar = tarfile.open(dataset_path)
        tar.extractall(args.output_path)
        tar.close()
        os.remove(dataset_path)
    print("All datasets downloaded and extracted")
