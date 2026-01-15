from fastapi import FastAPI, Body
import ollama

app =FastAPI()
client = ollama.Client(
    host="http://localhost:11434"
)

@app.get("/")
def read_root():
    return {"Hello": "world"}

@app.get("/contact-us")
def read_root():
    return {"email": "sammer22323@gmail.com"}

@app.post("/chat")
def chat(message: str = Body(
        ..., 
        description= "some message"
)):
    response= client.chat(model='gemma3:1b',
                messages=[
                    {"role": "user", "content": message}
                ]
            )
    return {"response": response['message']['content']}