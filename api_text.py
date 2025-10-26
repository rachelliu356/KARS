import openai
import os

BOSON_API_KEY = os.getenv("BOSON_API_KEY")

client = openai.OpenAI(
    api_key=BOSON_API_KEY,
    base_url="https://hackathon.boson.ai/v1"
)

response = client.chat.completions.create(
    model="higgs-audio-understanding-Hackathon", # replace it
    messages=[
        {"role": "system", "content": "You are a mean person."},
        {"role": "user", "content": "Explain quantum physics briefly."}
    ],
    max_tokens=128,
    temperature=0.7
)


print(response.choices[0].message.content)
