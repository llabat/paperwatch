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

def single_out_specials(similarities, threshold):
    # Get the indices of the new papers that are similar to the seed papers
    beyond_threshold = np.where(similarities > threshold)

    # Create a dictionary to store the indices and their corresponding similarities
    specials = dict()
    for i, j in zip(beyond_threshold[0], beyond_threshold[1]):
        specials[int(i)] = specials.get(i, []) + [(int(j), float(similarities[i][j]))]

    return specials