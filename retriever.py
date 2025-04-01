# retriever.py

import openai
import os
import json
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text, model="text-embedding-3-small"):
    response = openai.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def load_embeddings(embedding_file="principles_embeddings.json"):
    with open(embedding_file, "r") as f:
        return json.load(f)

def retrieve_top_matches(query, embedding_file="principles_embeddings.json", top_k=5):
    query_embedding = get_embedding(query)
    chunks = load_embeddings(embedding_file)

    for chunk in chunks:
        chunk["similarity"] = cosine_similarity(chunk["embedding"], query_embedding)

    sorted_chunks = sorted(chunks, key=lambda x: x["similarity"], reverse=True)
    return sorted_chunks[:top_k]

