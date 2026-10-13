# Audio Sentiment Analysis with Pydantic AI and Gemini

This demo shows how to analyze emotions and sentiment from speech audio using Pydantic AI with Google Gemini. A practical use case is contact-center monitoring, where structured emotion outputs can trigger alerts or guide agent assistance. The workflow covers structured outputs with Pydantic, audio handling, and running analyses on single and multiple clips.

What's shown:

Structuring model outputs with Pydantic for reliable downstream use
Sending audio to Gemini with BinaryContent
Building a Pydantic AI Agent for audio analysis
Running single and batch evaluations on a public dataset
Interpreting results and understanding limitations

Demo flow summary
Prepare environment and credentials
Define a structured EmotionAnalysis schema
Create a Gemini-powered Agent
Load audio samples from MELD_audio
Convert audio arrays to WAV bytes for the model
Run a single analysis and view structured results
Run a batch analysis across different labeled emotions
Commands and code used in the demo
1) Environment setup
To use the Udacity workspace:
In the navigation pane on the left (below the table of contents), click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/demos/5-sentiment-analysis/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Copy environment file:
cp env.example .env
Set `GEMINI_API_KEY` in `.env` and choose the matching endpoint:

- Google AI Studio key: `GOOGLE_GEMINI_BASE_URL=https://generativelanguage.googleapis.com`
- Udacity/Vocareum key: `GOOGLE_GEMINI_BASE_URL=https://gemini.vocareum.com`

The notebook defaults to Google's API. An existing `.env` endpoint overrides that default. It uses `load_dotenv(override=True)` so rerunning setup picks up edited values. After changing credentials or the endpoint, rerun setup and recreate the agent.

A `This key was not found` response means the selected service rejected the key. Check that the key and endpoint match; if a Vocareum-issued key fails at the Vocareum endpoint, check the current credentials in the course workspace.

2) Define the structured output schema
from typing import List
from typing_extensions import Literal

class EmotionAnalysis(BaseModel):
    primary_emotion: List[Literal[
        "anger", "disgust", "fear", "happiness",
        "surprise_or_disappointment", "sadness", "neutral",
    ]] = Field(description="The dominant emotion detected in the audio")
    sentiment_polarity: str = Field(description="Overall sentiment: positive, negative, or neutral")
    intensity: str = Field(description="Emotion intensity: low, medium, or high")
    description: str = Field(description="Brief description of the emotional tone and characteristics")
Note: confidence scoring from an LLM is not reliable; avoid naive confidence fields.

3) Create the Pydantic AI Agent with Gemini
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider

settings = GoogleModelSettings(google_thinking_config={"thinking_budget": 0})
gemini_base_url = (
    os.getenv("GOOGLE_GEMINI_BASE_URL", "").strip()
    or "https://generativelanguage.googleapis.com"
)
provider = GoogleProvider(
    api_key=os.environ["GEMINI_API_KEY"].strip(),
    base_url=gemini_base_url,
)
model = GoogleModel("gemini-2.5-flash-lite", provider=provider)

emotion_agent = Agent(
    model=model,
    output_type=EmotionAnalysis,
    instructions="""
    You are an expert audio sentiment analyzer. Listen to the provided audio and analyze:
    1. The primary emotions expressed by the speaker
    2. The overall sentiment polarity (positive/negative/neutral)
    3. The intensity of the emotional expression
    4. A brief description of the emotional characteristics and a rationale for your choices
    Be precise and analytical in your assessment.
    """,
    model_settings=settings,
)

## Load the Dataset and Preview Samples

`datasets` 4 and later removed support for dataset scripts, including `trust_remote_code=True`. Use the built-in Parquet and CSV loaders for the same MELD dataset. The Parquet export contains audio only, so restore transcripts and labels from `train.csv` by clip ID. The first run downloads about 1.1 GB of training audio.

```python
from datasets import load_dataset
from datasets import Audio as DatasetAudio

# Use built-in file loaders: datasets >= 4 no longer runs dataset scripts.
dataset = load_dataset(
    "parquet",
    data_files={
        "train": "hf://datasets/ajyy/MELD_audio@refs/convert/parquet/default/train/*.parquet"
    },
    split="train",
)
annotations = load_dataset(
    "csv",
    data_files={"train": "https://huggingface.co/datasets/ajyy/MELD_audio/resolve/main/train.csv"},
    split="train",
)

# The Parquet export contains audio only. Restore labels by clip ID, not row order.
annotations_by_clip = {
    f"dia{row['Dialogue_ID']}_utt{row['Utterance_ID']}": row
    for row in annotations
}
clip_ids = [key.rsplit("/", 1)[-1] for key in dataset["__key__"]]
matched_indices = [
    i for i, clip_id in enumerate(clip_ids) if clip_id in annotations_by_clip
]
if not matched_indices:
    raise ValueError("No MELD audio clips matched the training annotations.")

dataset = dataset.select(matched_indices)
for column, source_column in (
    ("text", "Utterance"),
    ("emotion", "Emotion"),
    ("sentiment", "Sentiment"),
):
    dataset = dataset.add_column(
        column,
        [annotations_by_clip[clip_ids[i]][source_column] for i in matched_indices],
    )

dataset = dataset.rename_column("flac", "audio")
dataset = dataset.cast_column("audio", DatasetAudio(sampling_rate=16000))
dataset = dataset.remove_columns(["__key__", "__url__"])

print(f"Dataset loaded with {len(dataset)} samples")
print(f"Available emotions: {set(dataset['emotion'])}")
```

Optional preview (audio playback in notebooks):

```python
for i in range(3):
    display(Audio(dataset[i]["audio"]["array"], rate=dataset[i]["audio"]["sampling_rate"]))
    print(f"Sample {i}: {dataset[i]['text']} - {dataset[i]['emotion']})")
```

5) Helper functions for audio packaging
def audio_to_bytes(audio_array, sample_rate):
    buf = io.BytesIO()
    sf.write(buf, audio_array, sample_rate, format='WAV')
    buf.seek(0)
    return buf.getvalue()

def format_audio_for_gemini(sample_idx):
    sample = dataset[sample_idx]
    audio_bytes = audio_to_bytes(sample['audio']['array'], sample['audio']['sampling_rate'])
    audio_content = BinaryContent(data=audio_bytes, media_type='audio/wav')
    return sample, audio_content
6) Single audio analysis
sample_idx = 10
sample, audio_content = format_audio_for_gemini(sample_idx)
display(Audio(sample["audio"]["array"], rate=sample["audio"]["sampling_rate"]))

result = emotion_agent.run_sync(
    ["Analyze the emotion and sentiment in this audio clip.", audio_content]
)

print("Analysis Results:")
print(f"Primary Emotion: {result.output.primary_emotion}")
print(f"Sentiment: {result.output.sentiment_polarity}")
print(f"Intensity: {result.output.intensity}")
print(textwrap.fill(result.output.description))
print(f"Ground Truth: {sample['emotion']}")
7) Batch analysis across emotions
emotions_to_test = {"fear", "joy", "sadness", "anger", "surprise", "disgust", "neutral"}
emotion_samples = {}

for emotion in emotions_to_test:
    for idx, item in enumerate(dataset):
        if item["emotion"] == emotion and emotion not in emotion_samples:
            emotion_samples[emotion] = idx
            break

for emotion, idx in emotion_samples.items():
    sample, audio_content = format_audio_for_gemini(idx)
    display(Audio(sample["audio"]["array"], rate=sample["audio"]["sampling_rate"]))
    print(f"Text: '{sample['text']}'")
    result = emotion_agent.run_sync(
        ["Analyze the emotion and sentiment in this audio clip.", audio_content]
    )
    print(result.output.model_dump_json(indent=2))
Takeaways
BinaryContent is required to send audio bytes to the model.
Dataset labels are not used for supervision here; treat comparisons as informal.
Avoid LLM self-reported confidence; use alternative calibration methods if needed.







In this demo, we're going to explore how to analyze emotions and sentiment in audio using pydantic AI and Google Gemini. Let's get started. We start by importing all the necessary libraries. This includes tools for environment management, data handling, and audio processing. We use dotenv to load our API Key from the dotenv file. Make sure you've copied envdot example to dotenv and added your Gemini Key. The assert statements check that everything is set up correctly, so you won't run into issues later. Next, we import nest_asyncio and apply it. This is a little trick to make sure asynchronous code works smoothly inside Jupiter notebooks, which can sometimes be finicky with event loops. It is required to use Pydantic AI within Jupiter in a non-async way. Now, we define our response schema using a Pydantic schema, also called data model. This is crucial. It lets us structure the output from our sentiment analysis in a way that's easy to parse and use later. We specify the possible emotions, sentiment polarity, intensity, and the description. Let's focus on the primary emotion for a second. First, this is a classification field, so we want the model to select among a limited number of options. To accomplish this, we provide the options in a literal block. Then, since a given audio file could have more than one emotion, we wrap that in a list to indicate to the model that it can provide more than one choice, but all choices must be valid emotion classifications. In other words, each choice must be one of the categories specified in the literal. Then, as usual, we use the field class to provide a description that helps the model understand what to put here. With the schema in place, we set up our Pydantic AI agent. We configure it to use Gemini, and we give it detailed instructions, so the model knows exactly what to do. Analyze the audio, identify the main emotions, rate the sentiment, judge the intensity, and explain its reasoning. We also use the Google model settings class to configure the model behavior. In particular, we disable thinking to keep responses fast and cheap. When you have settings like these, remember to pass them when you build the agent, as shown here. Time to load some data. We pull in a sample from the MELD audio data set, which is widely used for emotion recognition research. We print out the available emotions and show the structure of the data, so you know what you're working with. We also play a few audio samples and display their text and emotion labels for context. Also, I was the point person on my company's transition from the KL five to GR six systems. You must have had your hands full. No, Joan, I beg of you. Before running any analysis, we define helper functions to process the audio. The first function receives an array of audio data and converts it to a bytes representation using sound file. The second function formats a sample from the dataset in what Gemini expects. We first transform the sample to Bytes using the function we just defined. Then we wrap it into a binary content element using the media type audio wave. With that out of the way, let's analyze a single audio sample. We pick one by index formatted and display the audio so you can listen to it. Then we run the sentiment analysis agent and print out the results, primary motion, sentiment polarity, intensity, and the descriptive summary. We also show the ground truth label for comparison. Let's hear it. I see. But they'll be perhaps 30 people on the. We can see that the model picked up the right category. For a broader view, we run batch analysis across several emotions. We select one sample for each emotion type, play the audio, and print the text. The agent analyzes each clip, and we print the structured results for each one. This gives you a sense of how well the model performs across different emotional tones. Let's play the first couple of examples. Would you look at this dup? He hated us. This was his spinal bit. No, Joe, I beg of you. Again, the answers are pretty accurate. As you can see, the model choices are reasonable and the output is structured, making it easy to use for downstream tasks like alerting or reporting. That's it for this demo. You've seen how to set up, run, and interpret audio sentiment analysis using Pydantic AI and Gemini, with clear, structured results every step of the way. Congratulations, and see you next time.