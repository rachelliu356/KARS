import openai
import os

BOSON_API_KEY = os.getenv("BOSON_API_KEY")

client = openai.OpenAI(
    api_key="bai-gpr3RDJ208hq6QGZQ6RUt6N_kqHJ7aggUCwQAn2Hf50RvokU",
    base_url="https://hackathon.boson.ai/v1"
)
messages=[
        {"role": "system", "content": "You are helpful assistant."}
    ]
temp_list = []
print("🤖 Chat started!")
while True:
    user_input = input("🧑 You: ")
    messages.append({"role": "user", "content": user_input})

    if (len(messages) >= 10):
        temp_list = messages[-10:]
    else:
        temp_list = messages

    response = client.chat.completions.create(
        model="higgs-audio-understanding-Hackathon", # replace it
                   
        messages = temp_list,

        max_tokens=128,
        temperature=0.7
    )

    reply = response.choices[0].message.content
    print(f"assistant's reply: {reply}\n")
    messages.append({"role" : "system", "content" : reply})