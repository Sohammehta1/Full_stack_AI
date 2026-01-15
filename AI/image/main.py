from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()

image = "https://images.pexels.com/photos/34374535/pexels-photo-34374535.jpeg"

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "what's in this image?"},
            {
                "type": "image_url",
                "image_url": {"url":image}, 
            },
        ],
    }],
)

print(response.choices[0].message.content)