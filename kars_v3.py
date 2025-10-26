import openai
import base64
import os
import streamlit as st
import wave

BOSON_API_KEY = os.getenv("BOSON_API_KEY")

def encode_audio_to_base64(file_path: str) -> str:
    """Encode audio file to base64 format."""
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

client = openai.Client(
    api_key=BOSON_API_KEY,
    base_url="https://hackathon.boson.ai/v1"
)

def user_input(prompt, i):


    # if "first_prompt" not in st.session_state:
    #     st.session_state.first_prompt = None

    # if st.session_state.first_prompt is None and prompt:
    #     st.session_state.first_prompt = prompt

    # Record audio from microphone
    if prompt is not None:
        audio_data = st.audio_input("Record yourself saying the phrase:", key = f"audio_{i}")

    # Check if the user recorded something
    if audio_data is not None:
        # Play back the recorded audio in Streamlit
        st.audio(audio_data, format="audio/wav")

        # Save it to a local file
        with open(f'recording_{i}.wav', "wb") as f:
            f.write(audio_data.getvalue())

        st.success(f"✅ Audio saved as recording_{i}.wav")

    # st.write("Processing input...")

    if audio_data is not None:
        # Save to file
        audio_path = f"recording_{i}.wav"
        audio_base64 = encode_audio_to_base64(audio_path)
        file_format = audio_path.split(".")[-1]

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
        audio_path = f"recording_{i}.wav"
        audio_base64 = encode_audio_to_base64(audio_path)
        file_format = audio_path.split(".")[-1]

        response = client.chat.completions.create(
            model="higgs-audio-understanding-Hackathon",
            messages=[
                {"role": "system", "content": "You are a speech therapist."},
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
                    "content": "Compare the user's recording to the proper american pronunciation of '"+prompt+"' and give advice on how to make the pronounciation closer. DO NOT used phonetics. Instead, use simpler words combined to assist pronounciation, such as man and go for mango. Keep the response under 1 minute of speaking time.",
                },
            ],
            max_completion_tokens=256,
            temperature=0.0,
        )

        print(response.choices[0].message.content)
        st.subheader("Advice")
        st.write(response.choices[0].message.content)
        return response.choices[0].message.content

def KARS_response(read_out, i):

    response = client.audio.speech.create(
    model="higgs-audio-generation-Hackathon",
    voice="belinda",
    input=f'{read_out}',
    response_format="pcm"
    )
    
    # You can use these parameters to write PCM data to a WAV file
    num_channels = 1        
    sample_width = 2        
    sample_rate = 24000   

    pcm_data = response.content

    with wave.open(f'out_{i}.wav', 'wb') as wav:
        wav.setnchannels(num_channels)
        wav.setsampwidth(sample_width)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm_data)

    st.subheader("KARS RESPONSE")
    st.audio(f'out_{i}.wav', format="audio/wav")

st.title("Krazy Audio Revision Software")
st.write("Your own virtual speech coach. Building off of Boson AI's Audio processing software, the Krazy Audio Revision Software (KARS) aids the deaf, hard of hearning, or anyone learning a new language in learning to speak by listening to users, giving speaking practice, and providing feedback on pronunciation in a visual format.")

st.subheader("Input")
# Enter a phrase user is trying to say


prompt = st.text_input("Enter a phrase you want advice for:")

if "i" not in st.session_state:
    st.session_state.i = 1

st.write(f"Iteration: {st.session_state.i}")

response_text = user_input(prompt, st.session_state.i)

if response_text:
    KARS_response(response_text, st.session_state.i)
    prompt = st.text_input("Enter a phrase you want advice for:")
    st.session_state.i +=1

    response_text = user_input(prompt, st.session_state.i)
