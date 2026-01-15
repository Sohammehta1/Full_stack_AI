from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI


load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    collection_name="learning_rag",
    embedding=embeddings, 
    url="http://localhost:6333"
)

user_query = input("Ask your node js doubt 👉🏼")

search_results= vector_db.similarity_search(user_query)

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

client = OpenAI()

response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT}, 
            {'role': 'user', 'content': user_query}
        ],  # <--- FIXED: Passed directly, not wrapped!
    )

print(f"Response 👉🏼: {response.choices[0].message.content}")