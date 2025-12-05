import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from parse_sql_schema import parse_sql_schema
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# New correct client setup
chroma = chromadb.PersistentClient(path="chroma_store")

collection = chroma.get_or_create_collection(
    name="schema_store",
    metadata={"hnsw:space": "cosine"}
)

schema = parse_sql_schema("schema.sql")

def embed(texts):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [item.embedding for item in resp.data]

docs, ids, metas = [], [], []

for i, table in enumerate(schema):
    text = (
        f"TABLE: {table['name']} | "
        f"COLUMNS: {', '.join(table['columns'])} | "
        f"DESCRIPTION: {table['description']}"
    )

    docs.append(text)
    ids.append(str(i))
    metas.append({
        "name": table["name"],
        "type": "table",
        "description": table["description"],
        "columns": ", ".join(table["columns"])  # ← FIXED
    })

vectors = embed(docs)

collection.add(
    ids=ids,
    documents=docs,
    embeddings=vectors,
    metadatas=metas
)

print("✅ Schema successfully indexed into ChromaDB!")
