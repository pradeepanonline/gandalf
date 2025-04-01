# embedder.py

import openai
import os
import json
import numpy as np
from load_principles import load_principles_from_folder

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text, model="text-embedding-3-small"):
    response = openai.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

def build_and_save_embeddings(folder="principles", output="principles_embeddings.json"):
    chunks = load_principles_from_folder(folder)
    embedded_chunks = []

    for chunk in chunks:
        embedding = get_embedding(chunk["text"])
        embedded_chunks.append({
            "id": chunk["id"],
            "title": chunk["title"],
            "source_file": chunk["source_file"],
            "text": chunk["text"],
            "embedding": embedding
        })

    with open(output, "w") as f:
        json.dump(embedded_chunks, f)

    print(f"✅ Saved {len(embedded_chunks)} embedded principles to {output}")

if __name__ == "__main__":
    build_and_save_embeddings()

