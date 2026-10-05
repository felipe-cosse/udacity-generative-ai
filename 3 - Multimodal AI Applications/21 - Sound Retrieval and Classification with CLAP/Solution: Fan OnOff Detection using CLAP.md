This walkthrough demonstrates how zero-shot audio classification with CLAP can flag when a household fan is ON or OFF. The exercise builds an end-to-end mini-pipeline: load audio at the correct sample rate, split into manageable chunks, classify each chunk with natural-language labels, threshold the scores, detect state changes, visualize, and summarize behavior over time.

What this develops:

Practical use of CLAP for sound event detection without training.
A repeatable pattern for turning model scores into discrete state changes and metrics.

CLAP (Contrastive Language-Audio Pretraining) maps audio and text into the same space. By providing short, specific candidate labels (e.g., “the sound of a fan”), CLAP can perform zero-shot classification over audio segments.

The approach:

Load the audio at 48 kHz (CLAP-friendly).
Slice the waveform into fixed-length, overlapping chunks (1 s with adjustable overlap).
For each chunk, request scores for candidate labels via the zero-shot-audio-classification pipeline using laion/larger_clap_general.
Extract the score for the positive label (fan ON), then apply a threshold (e.g., 0.5) to convert scores into ON/OFF states.
Detect transitions when the state flips across adjacent chunks.
Plot waveform, scores, binary states, and the mel spectrogram to interpret results.
Summarize total ON time, duty cycle, and number of transitions.
Why label wording matters:

Short, concrete labels reduce ambiguity.
Include a negative/background class (e.g., “silence or background noise”) to give the model contrast.
Step-by-Step Instructions
To use the Udacity workspace:

At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/exercises/2-clap/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Load audio at 48 kHz
Use librosa.load to resample to 48,000 Hz for CLAP compatibility.
audio_path = "fan.mp3"
audio, sr = librosa.load(audio_path, sr=48000)
Confirm duration and sample rate.
Optional: quick listen with IPython.display.Audio.
Initialize the CLAP zero-shot pipeline
from transformers import pipeline
pipe = pipeline("zero-shot-audio-classification", model="laion/larger_clap_general")
Define candidate labels and the positive class
Keep labels short and specific.
Include one label for background, one for fan sound.
candidate_labels = ["silence or background noise", "the sound of a fan"]
POSITIVE_LABEL = "the sound of a fan"
Chunk the audio into overlapping windows
Use 1.0 s chunks and set overlap (e.g., 0.25 => 25% overlap). Adjust for trade-offs between temporal resolution and stability.
chunk_duration = 1.0
overlap = 0.25
chunk_samples = int(chunk_duration * sr)
hop_samples = int(chunk_samples * (1 - overlap))

chunks, timestamps = [], []
for start in range(0, len(audio) - chunk_samples + 1, hop_samples):
    end = start + chunk_samples
    chunks.append(audio[start:end])
    timestamps.append(start / sr)
Classify each chunk and collect fan scores
For each chunk, request scores and keep the score for the positive label.
fan_scores = []
for chunk in chunks:
    result = pipe(chunk, candidate_labels=candidate_labels)
    prob_on = [x["score"] for x in result if x["label"] == POSITIVE_LABEL][0]
    fan_scores.append(prob_on)
Convert scores to ON/OFF states
Apply a threshold; 0.5 is a simple starting point. Tune based on false positives/negatives.
threshold = 0.5
fan_states = [score > threshold for score in fan_scores]
Detect state changes
A change occurs when adjacent binary states differ.
state_changes = []
for i in range(1, len(fan_states)):
    if fan_states[i] != fan_states[i-1]:
        new_state = "ON" if fan_states[i] else "OFF"
        state_changes.append((timestamps[i], new_state))
Visualize waveform, scores, states, and spectrogram
Combine plots to verify alignment and interpret ambiguous regions.
Add vertical lines at transition times for quick reading.
Summarize usage metrics
Compute estimated ON time, duty cycle, and count of transitions.
total_on_time = sum(fan_states)  *chunk_duration*  (1 - overlap)
total_duration = len(audio) / sr
duty_cycle = total_on_time / total_duration * 100
Adjust and iterate
Tune candidate_labels, threshold, chunk_duration, and overlap.
Consider smoothing scores (e.g., moving average) if states flicker.
Remember: Short, specific candidate labels and a well-chosen threshold turn zero-shot scores into reliable ON/OFF state detection.







This exercise, you used the clap models zero shot audio classification to detect when a fan is on or off in an audio recording. In a real scenario, you might be monitoring a production line where a fan needs to be working continuously. You could capture chunks of one second and in real time classify them and send an alert to a supervisor if you detect that the fan is off or even shut down the production line automatically to avoid damage. Let's walk through the solution. We start by importing the necessary libraries. In particular, we load the librosa for audio processing and the pipeline function from transformers to access CLAP. We also import the audio class to play audio directly in the notebook. Next, you loaded the audio file using librosa.load, specifying a sample rate of 48,000 hertz, which is expected by CLAP. This function returns both the audio data and the sample rate. We print out the duration and sample rate to confirm everything loaded correctly, and then we use the audio display to listen to the file. Let's listen to a few seconds. Let's move on. Here, you had to set up the CLAP pipeline for zero shot audio classification. The pipeline is initialized with the larger CLAP general model, which is designed for general audio tasks. You defined two candidate labels, one for silence or background noise, and one for the sound of a fan. It's best to keep these labels short and specific. Here I decided to use these two. Then you also set a variable for the positive label, which in my case, is the sound of a fan. Now, we provided you with a code to split the audio into overlapping chunks of 1 second each. It calculates the number of samples per chunk and the hop size for overlap. Then it loops through the audio, extracting each chunk and recording its start time. This gives you a list of audio segments and their corresponding time stems. To make sure the chunking worked, we play one of the chunks using the audio display. This is a quick sanity check before moving on. Okay. Things are working. Next, you had to classify each chunk using the CLAP pipeline. For each chunk, you passed it to the pipeline along with your candidate labels. The pipeline returned scores for each label, and we extract the score for the positive label, Fan sound. Then we store these scores in a list for later analysis. With the scores in hand, we provided some code to convert them to binary states. If the score was above 0.5, the fan was considered on. Otherwise, it was off. Then, whenever the state changed from on to off or vice versa, we record the timestamp and the new state. This let you pinpoint exactly when the fan turned on or off. Finally, we visualize the results with a set of plots. First, we plot the audio wave form. Then we show the fan detection scores over time marking the threshold. Next, we plot the binary fan states. Finally, for good measure, we display the mel spectrogram of the audio. For each detected state change, we add a vertical line to all plots, colored green for on, and red for off. This gives a clear visual summary of the fans activity. To wrap up, we print a summary, the total duration of the audio, the estimated time the fan was on, the duty cycle, percentage of time the fan was on, and the number of state changes detected. This approach leverages CLAPS zero shock capabilities to solve a real world problem without any training or optimization. It's quick, flexible, and gives you a taste of the power of modern audio models. Of course, this is not the only way to approach a problem like this, but it is fun and simple. Congrats in completing this exercise and see you next time.