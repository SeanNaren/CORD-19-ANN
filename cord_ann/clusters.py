from sklearn.cluster import KMeans

from cord_ann.embeddings import encode_sentences


def encode_and_cluster(sentences, model, batch_size, num_clusters):
    embeddings = encode_sentences(model=model,
                                  batch_size=batch_size,
                                  sentences=sentences)

    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = [[] for i in range(num_clusters)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(sentences[sentence_id])
    return clustered_sentences
