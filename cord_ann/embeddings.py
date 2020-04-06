from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self, model_name_or_path, device, batch_size, show_progress_bar=True):
        self.model = SentenceTransformer(model_name_or_path=model_name_or_path,
                                         device=device)
        self.batch_size = batch_size
        self.show_progress_bar = show_progress_bar

    def encode_sentences(self, sentences):
        sentence_embeddings = self.model.encode(sentences=sentences,
                                                batch_size=self.batch_size,
                                                show_progress_bar=self.show_progress_bar)
        return sentence_embeddings
