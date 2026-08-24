import pandas as pd
import chromadb
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Project root
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

# OpenAI client
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ChromaDB client
chroma_client = chromadb.PersistentClient(
    path=os.path.join(BASE_DIR, "vector_db")
)

# Create collection
collection = chroma_client.get_or_create_collection(
    name="hospital_documents"
)

# Load CSV files
faq_df = pd.read_csv(
    os.path.join(BASE_DIR, "data", "hospital_faqs.csv")
)

policy_df = pd.read_csv(
    os.path.join(BASE_DIR, "data", "hospital_policies.csv")
)

print("FAQs loaded:", len(faq_df))
print("Policies loaded:", len(policy_df))



def create_embedding(text):
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


# -----------------------------
# Store FAQs
# -----------------------------

faq_count = 0

for _, row in faq_df.iterrows():

    document = f"""
Question: {row['question']}

Answer: {row['answer']}
"""

    embedding = create_embedding(document)

    collection.upsert(
        ids=[f"faq_{row['faq_id']}"],
        documents=[document],
        embeddings=[embedding],
        metadatas=[{
            "source": "faq",
            "category": str(row["category"])
        }]
    )

    faq_count += 1


# -----------------------------
# Store Policies
# -----------------------------

policy_count = 0

for _, row in policy_df.iterrows():

    document = f"""
Title: {row['title']}

Content: {row['content']}
"""

    embedding = create_embedding(document)

    collection.upsert(
        ids=[f"policy_{row['policy_id']}"],
        documents=[document],
        embeddings=[embedding],
        metadatas=[{
            "source": "policy",
            "category": str(row["category"])
        }]
    )

    policy_count += 1


print("\nIndexing completed successfully!")

print("FAQs stored:", faq_count)
print("Policies stored:", policy_count)
print("Total documents:", collection.count())