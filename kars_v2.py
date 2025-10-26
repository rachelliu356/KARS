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
    api_key=BOSON_API_KEY,
    base_url="https://hackathon.boson.ai/v1"
)

st.title("Krazy Audio Revision Software")
st.write("A speaking solution for the hard of hearing and speech impaired. Building off of Boson AI's Audio processing software, the Krazy Audio Revision Software (KARS) aids the deaf and hard of hearning in learning to speak by listening to users, giving speaking practice, and providing feedback on pronunciation in a visual format.")

st.subheader("Input")
# Enter a phrase user is trying to say
prompt = st.text_input("Enter a phrase you want advice for:")

# Record audio from microphone
if prompt is not None:
    audio_data = st.audio_input("Record yourself saying the phrase:")

# Check if the user recorded something
if audio_data is not None:
    # Play back the recorded audio in Streamlit
    st.audio(audio_data, format="audio/wav")

    # Save it to a local file
    with open("recording.wav", "wb") as f:
        f.write(audio_data.getvalue())

    st.success("Audio saved as recording.wav")

# st.write("Processing input...")
def give_feedback(audio_data, prompt):
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
        st.subheader("Transcription")
        st.write(transcription)

        # Chat about the audio
        audio_path = "recording.wav"
        audio_base64 = encode_audio_to_base64(audio_path)
        file_format = audio_path.split(".")[-1]

        response = client.chat.completions.create(
            model="higgs-audio-understanding-Hackathon",
            messages=[
                {"role": "system", "content": "You are a frank, honest, and caring speech therapist."},
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
                    "content": "Compare the user's recording to the proper american pronunciation of '"+prompt+"' and give advice on how to make the pronounciation closer. Be conscise, only focus on the worst words, and give specicific advice on mouth movements. "
                    "The user may be silly and say other words than what they are supposed to. In this case, tell them to please stop being silly.",
                },
            ],
            max_completion_tokens=256,
            temperature=0.0,
        )

    return response

response = give_feedback(audio_data, prompt)

print(response.choices[0].message.content)
st.subheader("Advice")

st.write(response.choices[0].message.content)
