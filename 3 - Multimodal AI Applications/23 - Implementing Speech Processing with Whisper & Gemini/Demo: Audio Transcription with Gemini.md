Automatic speech recognition unlocks searchable transcripts, captions, and multilingual support across support calls, lectures, podcasts, and product walkthroughs. This demo shows how to build an audio-to-text workflow using Google’s Gemini models with the google-genai SDK. Covered tasks:

Basic transcription of a short audio clip
Transcription with timestamps
Audio translation to English

Process Summary
Set up environment and initialize the Gemini client.
Load a sample audio file, convert to WAV bytes, and request transcription.
Request timestamped transcription and parse timestamps with a regex.
Load another audio file and request translation to English.
Setup
To use the Udacity workspace:
In the navigation pane on the left (below the table of contents), click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/demos/4-gemini/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Environment variables file
Copy example and fill in GEMINI_API_KEY.
Initialize the Client
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

assert load_dotenv(), "Could not find credentials from .env file"
assert os.getenv("GEMINI_API_KEY"), "GEMINI_API_KEY not found"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("Gemini client initialized")
Step 1 — Simple Audio Transcription
Load a short public audio sample.
Convert to WAV bytes.
Ask Gemini for a transcript.
from datasets import load_dataset
from io import BytesIO
import soundfile as sf
import textwrap
from IPython.display import Audio, display

# Load sample audio (LibriSpeech)
dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
audio_sample = dataset[0]["audio"]
audio_array = audio_sample["array"]
sampling_rate = audio_sample["sampling_rate"]

# Convert to WAV bytes
buffer = BytesIO()
sf.write(buffer, audio_array, sampling_rate, format="WAV")
buffer.seek(0)
audio_bytes = buffer.read()

# Request transcription
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=[
        "Please transcribe this audio file.",
        types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
    ],
)

display(Audio(audio_bytes))
print("Transcription:")
print(textwrap.fill(response.text, width=80))
Note:

For longer files, upload is required and not supported in the Udacity environment:
# Example (not supported here):
# import audiofile as af
# af.write("sample.ogg", audio_array, sampling_rate)
# audio_file = client.files.upload(file="./sample.ogg")
# response = client.models.generate_content(
#     model="gemini-2.5-flash-lite",
#     contents=["Please transcribe this audio file.", audio_file],
# )
Step 2 — Transcription with Timestamps
Prompt Gemini to include timestamps in the format [HH:MM:SS].
Parse the result with a regular expression and print the lines.
import re

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=[
        """
        Transcribe this audio with timestamps in the format [HH:MM:SS] text, 
        where HH is the hour, MM is the minute, and SS is the second.
        """,
        types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
    ],
)

print("Transcription with timestamps:")
display(Audio(audio_array, rate=sampling_rate))

# Parse timestamps: [HH:MM:SS] followed by text
time_stamps = {
    match.group(1): match.group(2).strip()
    for match in re.finditer(
        r"\[(\d{2}:\d{2}:\d{2})\]\s*([^[]*?)(?=\[\d{2}:\d{2}:\d{2}\]|$)",
        response.text,
    )
}

for ts, text in time_stamps.items():
    print(f"[{ts}] {textwrap.fill(text, width=80)}")
Tips:

Timestamps are prompt-driven; consistent formatting in the prompt helps ensure stable parsing.
For diarization (speaker labels), include instructions in the prompt and parse accordingly.
Step 3 — Translation to English
Load an MP3 audio file and request translation.
with open("italian.mp3", "rb") as f:
    audio_bytes = f.read()

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=[
        "Translate this audio to English",
        types.Part.from_bytes(data=audio_bytes, mime_type="audio/mp3"),
    ],
)

display(Audio(audio_bytes))
print("Translation:")
print(textwrap.fill(response.text, width=80))
Takeaways
genai.Client with generate_content handles audio parts via types.Part.from_bytes.
Short audio can be sent as bytes; long audio should be uploaded, then referenced.
Output structure can be influenced through clear prompting (e.g., timestamp format).
Regular expressions enable simple parsing of timestamped output.
Multilingual support enables direct audio-to-English translation using the same model family.







This time we're going to see how to use Google's Gemini 2.5 flashlight model for automatic speech recognition and translation, all using simple Python code. This is going to be short and sweet. Let's go. First, we set up our environment. We import the necessary libraries, including the Google GenAI SDK, dotenv for environment variables, and some helpers for audio playback and formatting. Make sure you've got your dotenv file ready with your API key. Just copy the example file and fill in your key. We initialize the Gemini client using the API key from our environment. If everything set up correctly, you'll see a confirmation that the client is ready. Next, we grab a sample audio file. For this demo, we're using the librispeech dataset, which is a standard for speech recognition tasks. We load the first sample, extract the audio array and its sample rate, and get it ready for processing. Now, let's transcribe. We convert the audio array into wav format using soundfile and BytesIO. Then send it to Gemini with a simple prompt: Please transcribe this audio file. The model does its magic and returns the transcription. We also play back a few seconds of the audio so you can hear what was transcribed. Mr. Quilter is the apostle of the middle classes, and we are glad to welcome his gospel. Nor is Mr. Quilter's manner less interesting than his matter. He tells us that at this festive season of the year, with Christmas and roast beef looming before us, similes drawn from eating and its results occur most readily to the mind. The text generated is perfectly aligned with the audio. Please note that if you're working with longer audio files, you'll need to upload them to Google and provide a link instead of uploading them in line as we did here. I reported the necessary code in the comment up here. Moving on, let's add timestamps to our transcription. We prompt Gemini to return the transcript with timestamps in the format, hours, minutes, and seconds followed by the text. After getting the response, we use a regular expression to split out each timestamp and its corresponding text, then print them out in a readable format. This is super useful for aligning transcripts with audio, especially for longer recordings. Let's hear the first 20 seconds or so and see how the model did. Mr. Quilter is the apostle of the middle classes, and we are glad to welcome his gospel. Nor is Mr. Quilter's manner less interesting than his matter. He tells us that at this festive season of the year, with Christmas and roast beef looming before us, similes drawn from eating and its results occur most readily to the mind. The timestamps are correct, and so is the text. Now, let's see how Gemini handles translation. We load an Italian audio file, send it to Gemini with the prompt: translate this audio to English, and get back the translated text. Again, we play the audio so you can hear the original and print the translation for reference. [inaudible]. That's it for today's demo. You've seen how to set up Gemini, transcribe audio, add timestamps, and even translate speech, all in just a few lines of code. Thanks for watching.