from redis import Redis
from rq import Queue

queue = Queue(connection=Redis(
    host='localhost', 
    port="6379"))

# {
#   "status": "Enqueued",
#   "job_id": "e34cd462-ffff-4a9d-ae59-46cd39d751fe"
# }