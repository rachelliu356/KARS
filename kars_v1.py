import openai
import base64
import os
import streamlit as st

BOSON_API_KEY = os.getenv("BOSON_API_KEY")

def encode_audio_to_base64(file_path: str) -> str:
    """Encode audio file to base64 format."""
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

client = openai.Client(
    api_key="bai-bPL6u0Zj4AdyiwwS0rTxbIS5lRF00i4XG7TO6bqSYtQwFbsD",
    base_url="https://hackathon.boson.ai/v1"
)

st.title("🎙️ Streamlit Audio Recorder Example")

# Record audio from microphone
audio_data = st.audio_input("Record your voice:")

# Check if the user recorded something
if audio_data is not None:
    # Play back the recorded audio in Streamlit
    st.audio(audio_data, format="audio/wav")

    # Save it to a local file
    with open("recording.wav", "wb") as f:
        f.write(audio_data.getvalue())

    st.success("✅ Audio saved as recording.wav")

if audio_data is not None:
    # Save to file
    audio_path = "recording.wav"
    audio_base64 = encode_audio_to_base64(audio_path)
    file_format = audio_path.split(".")[-1]
    # Transcribe audio
    # audio_path = "recorded.wav"
    # audio_base64 = encode_audio_to_base64(audio_path)
    # file_format = audio_path.split(".")[-1]

    response = client.chat.completions.create(
        model="higgs-audio-understanding-Hackathon",
        messages=[
            {"role": "system", "content": "Transcribe this audio for me."},
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
        temperature=0.0,
    )

    transcription = response.choices[0].message.content
    st.subheader("📝 Transcription")
    st.write(transcription)

    # Chat about the audio
    audio_path = "recording.wav"
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
                "content": "compare this to a typical american accent. what ways should the pronounciation be changed to match the accent?",
            },
        ],
        max_completion_tokens=256,
        temperature=0.0,
    )

    print(response.choices[0].message.content)