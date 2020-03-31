from sentence_transformers import SentenceTransformer


def load_embedding_model(model_name_or_path, device):
    model = SentenceTransformer(model_name_or_path=model_name_or_path,
                                device=device)
    return model


def encode_sentences(model, batch_size, sentences):
    sentence_embeddings = model.encode(sentences=sentences,
                                       batch_size=batch_size,
                                       show_progress_bar=True)
    return sentence_embeddings
