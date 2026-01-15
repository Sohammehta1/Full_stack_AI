from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import ollama




def createEmbeddingModel() -> OpenAIEmbeddings:
    return  OpenAIEmbeddings(
        model='text-embedding-3-large'
    )

def createVectorDb () -> QdrantVectorStore:

    embeddingModel = createEmbeddingModel()
    vector_db = QdrantVectorStore.from_existing_collection(
        collection_name="learning_rag",
        embedding=embeddingModel, 
        url="http://localhost:6333"
    )

    return vector_db

def process_query(client: ollama.Client, query: str):

    vector_db: QdrantVectorStore = createVectorDb()

    search_results = vector_db.similarity_search(query)
    context = '\n\n\n'.join([
    f'''Page content: {result.page_content}\n 
        Page number: {result.metadata['page_label']}\n
        File location: {result.metadata['source']}\n
        '''
            for result in search_results
        ])
    
    SYSTEM_PROMPT = f'''
    You are a helpfull assistant who answers every query based on the chunks of PDF file given to you, 
    along with the page contents and page number

    You should only answer the user query based on the given context and navigate the user to 
    open the correct page number to know more. 

    Context: 
    {context}
    '''

    # response = client.chat(
    #     model="gemma3:1b",
    #     messages=[
    #         {'role': 'system', 'content': SYSTEM_PROMPT}, 
    #         {'role': 'user', 'content': query}
    #     ],  # <--- FIXED: Passed directly, not wrapped!
    # )

    response= client.chat(model='gemma3:1b',
                messages=[
                    {"role": "user", "content": "what is nature?"}
                ]
            )

    print(f"Response 👉🏼: {response['message']['content']}")
    return response['message']['content']