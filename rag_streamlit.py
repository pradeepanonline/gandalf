# rag_streamlit.py

import streamlit as st
from openai import OpenAI
import os
from retriever import retrieve_top_matches

# Setup OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="Compliance Copilot (RAG)", layout="centered")
st.title("🤖 Ask Me Anything — Powered by Your Principles + RAG")
st.markdown("Ask a question, and I’ll answer using the most relevant principles from your knowledge base.")

user_question = st.text_area("💬 Your Question", height=150)

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

        try:
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            answer = response.choices[0].message.content
            st.markdown("### 🧠 Answer")
            st.markdown(answer)

            with st.expander("🔎 Source Principles Used"):
                for match in top_matches:
                    st.markdown(f"**{match['title']}** — from *{match['source_file']}* (Similarity: `{match['similarity']:.2f}`)")
                    st.markdown(f"> {match['text'][:500]}...")
                    st.markdown("---")

        except Exception as e:
            st.error(f"❌ Error: {e}")

else:
    st.info("Ask a question and click 'Get Answer 🚀'")

