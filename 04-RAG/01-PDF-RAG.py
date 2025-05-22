import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import QuantizationConfig

pdf_path = Path(__file__).parent / "nodejs-docs.pdf"
loader = PyPDFLoader(file_path = pdf_path)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
)

split_docs = text_splitter.split_documents(documents=docs)


embedder = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=os.environ["OPENAI_API_KEY"],
)


# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="nodejs-docs",
#     embedding=embedder,
# )

# vector_store.add_documents(documents=split_docs)
# print("Documents added to vector store.")
# =====================================================================

retrier = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="nodejs-docs",
    embedding=embedder,
)

relavent_chunks = retrier.similarity_search(
    query="What is module in Nodejs",
)

SYSTEM_PROMPT = f"""
You are a helpful assistant,who respondes based on available context.

Context:
{relavent_chunks}
"""

print("Relavent Chunks: ", relavent_chunks)
