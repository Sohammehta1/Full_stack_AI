from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from langchain_qdrant import QdrantVectorStore

from uuid import uuid4

load_dotenv()


pdf_path=Path(__file__).parent/"nodeJs.pdf"

CHUNK_SIZE=1000
CHUNK_OVERLAP=400

#LOADING THE PDF
loader= PyPDFLoader(file_path=pdf_path)
docs= loader.load() # pages as list

print(f'Page count is : {len(docs)}')

#CHUNKING
text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

chunks = text_splitter.split_documents(docs)

print(f"Number of chunks({CHUNK_SIZE}B each): {len(chunks)}\n")

#VECTOR EMBEDDINGS

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# client = QdrantClient(":memory:")

# client.create_collection(
#     collection_name="demo_collection",
#     vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
# )

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    collection_name="learning_rag",
    embedding=embeddings,
    url="http://localhost:6333"
)

print("Indexing of documents done\n")

# uuids = [str(uuid4()) for _ in  range(len(chunks))]

# vector_store.add_documents(documents=chunks, ids=uuids)

results= vector_store.similarity_search("What is node")
print(f"Result of query is \n+++++++++++\n{results[0]}\n+++++++++++\n")