import openai
import base64
import os

BOSON_API_KEY = os.getenv("BOSON_API_KEY")

def encode_audio_to_base64(file_path: str) -> str:
    """Encode audio file to base64 format."""
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

client = openai.Client(
    api_key="bai-gpr3RDJ208hq6QGZQ6RUt6N_kqHJ7aggUCwQAn2Hf50RvokU",
    base_url="https://hackathon.boson.ai/v1"
)

# Transcribe audio
audio_path = "C:/Users/aliso/Downloads/Recording.wav"
audio_base64 = encode_audio_to_base64(audio_path)
file_format = audio_path.split(".")[-1]

response = client.chat.completions.create(
    model="higgs-audio-understanding-Hackathon",
    messages=[
        {"role": "system", "content": "Transcribe this audio"},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": audio_base64,
                        "format": file_format,
                    },
                },
            ],
        },
    ],
    max_completion_tokens=256,
    temperature=0.4,
)

# Chat about the audio
audio_path = "C:/Users/aliso/Downloads/Recording.wav"
audio_base64 = encode_audio_to_base64(audio_path)
file_format = audio_path.split(".")[-1]

response = client.chat.completions.create(
    model="higgs-audio-understanding-Hackathon",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": audio_base64,
                        "format": file_format,
                    },
                },
            ],
        },
        {
            "role": "user",
            "content": "can you transcribe what i said into international phonetic alphabet",
        },
    ],
    max_completion_tokens=256,
    temperature=0.8,
)

print(response.choices[0].message.content)