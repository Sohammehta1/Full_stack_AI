from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import  Client
from dotenv import load_dotenv
load_dotenv()

embeddingModel= OpenAIEmbeddings(
    model='text-embedding-3-large'
)

vectorClient= QdrantVectorStore.from_existing_collection(
    url = "http://localhost:6333",
    embedding= embeddingModel,
    collection_name="learning to use RAG", 
)

userQuery = input("Hey, ask something important: ")

search_results = vectorClient.similarity_search(query=userQuery)


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

openaiClient= Client()

response = openaiClient.chat.completions.create(
        model="gpt-5",
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT}, 
            {'role': 'user', 'content': userQuery}
        ],  # <--- FIXED: Passed directly, not wrapped!
    )

print(f"Response 👉🏼: {response.choices[0].message.content}")