Automatic speech recognition transforms spoken audio into text. This demo uses OpenAI’s Whisper large-v3-turbo through Hugging Face Transformers to transcribe speech, produce timestamps, and translate non‑English audio into English. Common uses include meeting notes, live captions, call center analytics, voice search, and media indexing.

Workflow Summary
Setup environment (Transformers, Torch, torchcodec, ffmpeg, librosa)
Import libraries and select device (CPU/GPU)
Load model and processor (Whisper large-v3-turbo)
Load audio, inspect duration and reference text
Transcribe with processor + model.generate
Use the pipeline for longer inputs and timestamps
Translate non‑English audio to English
Step-by-Step Instructions
1) Setup and Dependencies
To use the Udacity workspace:
In the navigation pane on the left (below the table of contents), click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/demos/3-whisper/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
2) Import Libraries and Select Device
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration, pipeline
import torchcodec  # requires ffmpeg installed
import textwrap
from IPython.display import Audio, display
from datasets import load_dataset

device = (
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()
    else "cpu"
)
3) Load Whisper Model and Processor
model_name = "openai/whisper-large-v3-turbo"
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name).to(device)

print(f"Model loaded: {model_name}")
print(f"Model size: ~{sum(p.numel() for p in model.parameters()) / 1e6:.1f}M parameters")
4) Load and Inspect Audio
ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
audio_sample = ds[0]["audio"]
audio_array = audio_sample["array"]
sr = audio_sample["sampling_rate"]

print(f"Audio loaded: {len(audio_array)} samples at {sr} Hz")
print(f"Duration: {len(audio_array) / sr:.2f} seconds")
print("Ground truth:\n")
print(textwrap.fill(ds[0]["text"], width=70))
5) Transcribe with Processor + model.generate
inputs = processor(
    audio_array,
    sampling_rate=sr,
    return_tensors="pt",
    language="en",
    task="transcribe",
).input_features.to(device)

with torch.no_grad():
    ids = model.generate(inputs)

transcription = processor.batch_decode(ids, skip_special_tokens=True)[0]
print("\nTranscription:\n")
print(textwrap.fill(transcription, width=70))
6) Pipeline API for Longer Audio and Convenience
# Load a longer sample
long_ds = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
sample = long_ds[0]["audio"]

torch_dtype = (
    torch.float16 if torch.cuda.is_available()
    else torch.bfloat16 if torch.backends.mps.is_available()
    else torch.float32
)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    dtype=torch_dtype,
    device=device,
    return_timestamps=True  # enables chunking for long inputs
)

result = pipe(sample)
display(Audio(sample["array"], rate=sample["sampling_rate"]))
print(textwrap.fill(result["text"], width=80))
7) Timestamped Chunks
result = pipe(sample, return_timestamps=True)
for chunk in result["chunks"]:
    tstart, tstop = sorted(chunk["timestamp"])  # fix occasional inversion
    print(f"[{tstart:.2f}s -> {tstop:.2f}s] {textwrap.fill(chunk['text'], width=60)}")
8) Translate Non‑English Audio to English
import librosa

it_audio, it_sr = librosa.load("italian.mp3", sr=16000)  # replace with file path
display(Audio(it_audio, rate=it_sr))

translation = pipe(
    it_audio,
    generate_kwargs={"language": "english", "task": "translate"},
)
print("============== Translation ==============")
for chunk in translation["chunks"]:
    tstart, tstop = sorted(chunk["timestamp"])
    print(f"[{tstart:.2f}s -> {tstop:.2f}s] {textwrap.fill(chunk['text'], width=60)}")
Takeaways
Whisper large‑v3‑turbo with Transformers enables accurate and fast speech transcription.
Two workflows are supported: manual preprocessing with model.generate and the high‑level pipeline.
Timestamped chunks help align text to audio and support long recordings.
Built‑in translation converts non‑English audio to English text.
Device and dtype choices strongly impact speed; use GPU when available.
Proper setup requires torchcodec and an ffmpeg installation with libavutil.






Today we're going to see how to transcribe and translate speech using OpenAI's Whisper model, all from Python with hugging phase transformers. Let's get started. First, we import the libraries and load the Whisper model. I'm using the large V turbo variant here, which is a great balance between speed and accuracy. Make sure you have FFM peg installed on your system. Whisper needs it for audio processing. Once the model and processor are loaded, we grab a sample audio file. For this demo, I'm using a sample from the hugging phase datasets library. But in practice, you'd load your own audio file. We extract the audio array and sample rate and print out some info, how many samples, the sample rate, and the groundthrog text. Next, we preprocess the audio with the processor. This step handles all the normalization and formatting Whisper expects. Then we run the model to generate the transcription. Notice I'm using torch, no grad. This is important for inference as it speeds things up by skipping gradient calculations. Once we have the predicted IDs, we decode them to get the transcription. We then print the result and compare it to the ground truth to see how well Whisper did. As you can see, the transcription is very accurate. Now, for a more convenient approach, we can use the hugging phase pipeline interface. This wraps up the processor and model and lets you transcribe audio in one easy call. To test it out a little deeper, here we load a longer extract of the same audio. We then load the pipeline for transcription, passing in explicitly, the tokenizer and the feature extractor. We then have to activate the timestamps in order to also activate support for longer text. We then simply call the pipeline on the sample, and we print the result. Let's hear the first 20 seconds or so of the audio and follow it in the transcription. Mr. Quilter is the apostle of the middle classes, and we are glad to welcome his gospel. Nor is Mr. Quilter's manner less interesting than his matter. He tells us that at this festive season of the year, with Christmas and roast beef looming before us, similes drawn from eating and its results occur most readily to the mind. It is very accurate. Whisper can also generate time stamps. In other words, it can break down the transcription into segments, each with a start and stop time. This is super useful for aligning text with audio or for building things like subtitles. Just loop through the result chunks and print out the text with its time stamps. This is the result on the text we just heard. If you compare it to the audio, it is pretty accurate. Finally, Whisper isn't just for English. You can use it to translate audio from other languages into English. For example, here I load an Italian audio sample, run it through the pipeline with the translate task, and print out both the original and the translation chunk by chunk with time stamps. Let's hear the original now. [inaudible]. I am Italian, and I can tell you that the result is indeed accurate. That's it for this demo. You now know how to transcribe and translate audio with Whisper, handle timestamps, and use both the low level and pipeline APIs. Thanks for watching.