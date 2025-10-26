import os, openai, base64
client = openai.Client(api_key=BOSON_API_KEY,
                       base_url="https://hackathon.boson.ai/v1")

def encode_audio_to_base64(file_path: str) -> str:
    """Encode audio file to base64 format."""
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

audio_path = "C:/Users/aliso/Downloads/Recording (1).wav"
audio_base64 = encode_audio_to_base64(audio_path)
file_format = audio_path.split(".")[-1]

resp = client.chat.completions.create(
    model="Qwen3-Omni-30B-A3B-Thinking-Hackathon",
    messages=[
        {"role": "system", "content": "You are a helpful assistant and like to help people improve."},
        {"role": "user", "content": [
            # {"type": "image_url", "image_url": {
            #     "url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-Omni/demo/cars.jpg"}},
            {"type": "input_audio", "input_audio": {"data": audio_base64, "format": file_format,}},
            {"type": "text", "text": "I am trying to say: i love cats and like to pet them lots because i like that they are furry. But i don't know if my pronounciation is completely correct can you help me?"}
        ]}
    ],
    max_tokens=256,
    temperature=0.2,
)

print(resp.choices[0].message.content)
