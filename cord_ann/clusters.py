from sklearn.cluster import KMeans


def cluster_embeddings(embeddings, sentences, num_clusters):
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = [[] for i in range(num_clusters)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(sentences[sentence_id])
    return clustered_sentences
