import torch
import numpy as np
from sentence_transformers import SentenceTransformer

def compute_similarities(texts1, texts2, model_name = "sentence-transformers/all-mpnet-base-v2"):

    # Load sentence encoder model
    model = SentenceTransformer(model_name)

    # Project abstracts onto the model space
    seed_embeddings = model.encode(texts1)
    new_abstract_embeddings = model.encode(texts2)

    # Compute cosine similarity
    return model.similarity(new_abstract_embeddings, seed_embeddings)


def rank_all_abstracts(abstracts_to_rank, similarities):

    # Average the scores
    scores = similarities.mean(axis=1)

    # Rank new abstract average cosine similarity with seeds (from highest to lowest)
    ranking = np.argsort(scores).flip(0)

    # Reorder the papers
    return [abstracts_to_rank[i] for i in ranking]