In this hands-on exercise, you will use CLAP zero-shot audio classification to detect when a fan turns on and off in a real recording (fan.mp3). The workflow covers loading audio, building a zero-shot pipeline with the LAION CLAP model, splitting audio into chunks, classifying each chunk, detecting state changes, and visualizing results.

This mirrors typical tasks in smart home monitoring, facility management, and energy efficiency analytics where appliance state needs to be inferred from sound without task-specific model training.

Prerequisites:
Classroom workspace with Jupyter Notebook access
Python 3.9+ and the following packages installed:
transformers, librosa, numpy, matplotlib, tqdm, IPython
Internet access for the first model download from Hugging Face Hub
The audio file fan.mp3 available in the working directory
Optional GPU for faster inference (CPU works for this exercise)
Objectives:
By the end of this exercise, you will be able to:

Configure a zero-shot audio classification pipeline with CLAP
Segment an audio file and classify each chunk for ON/OFF state
Detect transitions, visualize results, and estimate duty cycle
Steps:
Configure the lab environment

To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/exercises/2-clap/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Load and preview audio

Set the path: audio_path = "fan.mp3".
Complete the TODO to load audio at 48 kHz:
audio, sr = librosa.load(audio_path, sr=48000)
Run the playback cell to confirm the recording loads and plays.
Initialize the CLAP zero-shot pipeline

Complete the TODO to create the pipeline:
pipe = pipeline("zero-shot-audio-classification", model="laion/larger_clap_general")
The first run will download the model; ensure internet access.
Choose labels and set the positive class

Provide two concise, specific labels: one for background/silence and one for fan noise. Example:
candidate_labels = ["background noise", "electric fan noise"]
Set the positive label to match the “fan on” description:
POSITIVE_LABEL = "electric fan noise"
Tip: Short, specific labels often outperform vague phrases. Try alternatives like "household fan" or "ventilation fan".
Split audio into overlapping chunks

Use the provided parameters to create 1-second chunks with overlap:
chunk_duration = 1.0
overlap = 0.25 (adjust to 0.5 for true 50% overlap if desired)
Run the cell to generate chunks and timestamps.
Play a sample chunk to validate segmentation.
Classify each chunk with CLAP

Complete the TODO in the loop to call the pipeline:
result = pipe(chunk, candidate_labels=candidate_labels)
Extract the probability for POSITIVE_LABEL and store it in fan_scores.
Progress should show a tqdm bar; runtime depends on audio length.
Detect ON/OFF transitions

Use the provided threshold-based logic (default threshold = 0.5):
fan_states = [score > threshold for score in fan_scores]
Transition detection rule:
OFF → ON when fan_scores crosses above threshold
ON → OFF when crossing below threshold
Print the detected transition timestamps and new states.
Visualize waveform, scores, states, and spectrogram

Run the plotting cell to view:
Waveform
Fan detection score over time with threshold line
Binary ON/OFF state
Mel spectrogram
Vertical dashed lines mark state changes; green for ON, red for OFF.
Summarize system behavior

Execute the summary cell to compute:
Total audio duration
Estimated fan on time
Duty cycle (% time ON)
Number of state changes
Interpret whether the model’s detections align with audible fan behavior.
Extend and refine (optional)

Labels: Try alternatives ("box fan", "AC vent") and compare results.
Threshold: Adjust to 0.4–0.6 for sensitivity/precision trade-offs.
Chunking: Test chunk_duration = 0.5–2.0 and overlap = 0.25–0.75.
Smoothing: Apply a short moving average to fan_scores before thresholding.
Robustness: Test with different recordings (distance, noise sources).
