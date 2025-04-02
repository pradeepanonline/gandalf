# rag_streamlit_local_llm.py

import streamlit as st
import os
import requests
from retriever import retrieve_top_matches

# Streamlit page config
st.set_page_config(page_title="Compliance Copilot (RAG)", layout="centered")

st.markdown(
    """
    <div style="text-align:center;">
        <img src="https://cdn.pixabay.com/photo/2023/08/11/05/44/ai-generated-8182842_1280.jpg" alt="Gandalf Banner" style="width: 50%; height: auto; border-radius: 10px;" />
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ Local Deepseek query function (via Ollama)
def query_local_deepseek(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",  # Use exact model name you ran
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]
    except Exception as e:
        return f"❌ Error calling local model: {e}"
    

# Streamlit UI
st.title("🤖 Ask Gandalf")
st.markdown("Ask anything about Compliance principles.")



user_question = st.text_area("💬 Your Question", height=150)

# Run retrieval + generation
if st.button("Get Answer 🚀") and user_question.strip():
    with st.spinner("Retrieving relevant principles and generating answer..."):

        # Step 1: Get top matching principles
        top_matches = retrieve_top_matches(user_question, top_k=5)

        # Step 2: Inject selected principles into the GPT prompt
        context = ""
        for i, match in enumerate(top_matches):
            context += f"\n---\n[{match['source_file']}] {match['title']} (Similarity: {match['similarity']:.2f})\n{match['text']}\n"

        prompt = f"""
You are a senior compliance systems architect and coding expert. Answer the user's question based **only** on the provided principles below.
Cite relevant ideas when appropriate and do not make anything up.

### Principles:
{context}

### User Question:
{user_question}

### Answer:
"""
        # Step 3: Get answer from local Deepseek LLM
        answer = query_local_deepseek(prompt)

        # Step 4: Display answer
        st.markdown("### 🧠 Answer")
        st.markdown(answer)

        # Step 5: Optional source reference
        with st.expander("🔎 Source Principles Used"):
            for match in top_matches:
                st.markdown(f"**{match['title']}** — from *{match['source_file']}* (Similarity: `{match['similarity']:.2f}`)")
                st.markdown(f"> {match['text'][:500]}...")
                st.markdown("---")
else:
    st.info("Ask a question and click 'Get Answer 🚀'")

