from fastapi import FastAPI, Query
from .db import process_query
from ollama import Client

ollamaClient = Client(
    host="http://0.0.0.0:8080"
)

app = FastAPI()

@app.get('/')
def root():
    return {'status': 'Server is up and running'}

@app.post('/chat')
def chat(
        query: str= Query(..., description="The chat Query")
):
    return process_query(ollamaClient, query)