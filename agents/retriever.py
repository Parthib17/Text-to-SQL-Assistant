import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma = chromadb.PersistentClient(path="chroma_store")

collection = chroma.get_or_create_collection("schema_store")

def embed(text):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=[text]
    )
    return resp.data[0].embedding

def retrieve_schema(question, top_k=3):
    emb = embed(question)

    result = collection.query(
        query_embeddings=[emb],
        n_results=top_k
    )

    context = ""
    for meta in result["metadatas"][0]:
        context += (
            f"\nTABLE: {meta['name']}\n"
            f"COLUMNS: {meta['columns']}\n"
            f"DESCRIPTION: {meta['description']}\n"
        )

    return context
