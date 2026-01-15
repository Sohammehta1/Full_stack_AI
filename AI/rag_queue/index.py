from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


pdfPath = Path(__file__).parent/"nodejs.pdf"

# Load this file in python program

loader = PyPDFLoader(file_path=pdfPath)
docs= loader.load() # splits the document in pages. 

# split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap= 300
)

chunks = text_splitter.split_documents(documents=docs)

# Vector embeddings. 

embeddingModel= OpenAIEmbeddings(
    model='text-embedding-3-large'
)

vectorStore= QdrantVectorStore.from_documents(
    documents = chunks,
    embedding=embeddingModel,
    url = "http://localhost:6333", 
    collection_name="learning to use RAG"
)