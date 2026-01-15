from fastapi import FastAPI, Query
from dotenv import load_dotenv
load_dotenv()
from client.rq_client import queue
from queues.worker import process_query
app = FastAPI()

@app.get('/')
def root():
    return {"status": "server is up and running"}

@app.post('/chat')
def chat(
    query: str = Query(..., description='Doubt regarding Node Js')
):

    job = queue.enqueue(process_query, query)
    job_id = job.id
    # return process_query(query)
    return {'status': 'Enqueued', 'job_id': job_id}

@app.get('/result')
def get_result(
    job_id: str = Query(..., description="Id of the job")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return  {"result": result}  