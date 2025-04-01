# load_principles.py

import os
import json

def load_principles_from_folder(folder_path="principles"):
    all_chunks = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as f:
                principles = json.load(f)
                for p in principles:
                    chunk = {
                        "source_file": filename,
                        "id": p.get("id"),
                        "title": p.get("title"),
                        "text": f"{p.get('title', '')}\n\nRationale: {p.get('rationale', '')}\n\nImplementation: {p.get('implementation', '')}\n\nBenefits: {p.get('benefits', '')}"
                    }
                    all_chunks.append(chunk)
    
    return all_chunks

