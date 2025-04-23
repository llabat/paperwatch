import numpy as np
from sentence_transformers import SentenceTransformer

def rank_abstracts_by_relevance(seed_abstracts, new_abstracts):
   
    # Load sentence encoder model
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    # Project abstracts onto the model space
    seed_embeddings = model.encode(seed_abstracts)
    new_abstract_embeddings = model.encode(new_abstracts)

    # Compute cosine similarity
    similarities = model.similarity(new_abstract_embeddings, seed_embeddings)

    # Average the scores
    scores = similarities.mean(axis=1)

    # Rank new abstract average cosine similarity with seeds (from highest to lowest)
    ranking = np.argsort(scores).flip(0)

    return ranking