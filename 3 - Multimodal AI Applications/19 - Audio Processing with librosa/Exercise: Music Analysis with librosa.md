In this exercise, you will perform hands-on audio analysis using Python and the librosa library. Tasks include loading an MP3, resampling to 44.1 kHz, saving as WAV, visualizing a waveform, playing audio in a notebook, and creating a Mel spectrogram in decibels. These actions mirror common workflows in music information retrieval (MIR), podcast analytics, and audio ML pipelines used in industry and research. Mel spectrograms also support healthcare use cases such as phonocardiogram analysis for heart sound screening, showcased by the healthy heart spectrogram example in the notebook.

Prerequisites
Workspace with Jupyter Notebook access
Python 3.8+ with packages: librosa, soundfile, numpy, matplotlib, IPython
ffmpeg installed for robust MP3 decoding
Objectives
By the end of this exercise you will be able to:

Load audio at native and target sample rates
Save audio to WAV using the current sample rate
Plot & interpret waveform and Mel spectrogram representations
Steps
Open the starter notebook and verify environment

To use the Udacity workspace: At the top of the page, click Cloud Resources*. Then select* Start Cloud Resource*, and then* Open Cloud Console*.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/exercises/1-librosa/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Load the audio file (native sample rate)

Locate the TODO: “load the 'music.mp3' audio file”.
Replace y, sr = ... with:
y, sr = librosa.load("music.mp3")
Run the cell to ensure y (waveform samples) and sr (sample rate) are defined.
Resample to 44.1 kHz on load

Find the TODO: “load the file at 44.1kHz”.
Replace y, sr = ... with:
y, sr = librosa.load("music.mp3", sr=44100)
Run the cell; verify sr is 44100. This performs resampling inside librosa.load.
Save as WAV using soundfile

Find the TODO for saving.
Replace the placeholder with:
sf.write("music_44k.wav", y, sr)
Verify that music_44k.wav appears in the working directory. Download if playback outside the notebook is desired.
Plot the waveform

Find the TODO: “plot the waveform with librosa.display.waveshow”.
Replace the placeholder with:
plt.figure(figsize=(12, 3)); librosa.display.waveshow(y, sr=sr); plt.title("Waveform"); plt.tight_layout()
Observe amplitude envelopes and transients; dense vertical changes often indicate percussive content.
Play the audio in the notebook

Find the TODO for the Audio component.
Replace with:
Audio(y, rate=sr)
Execute the cell to enable inline playback. Adjust volume on the host system if silent.
Compute and visualize the Mel spectrogram

Find the TODO for the Mel spectrogram.
Replace mel_spec = ... with:
mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
Keep the provided conversion to decibels:
mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
Plot using:
plt.figure(figsize=(12, 4)); librosa.display.specshow(mel_spec_db, sr=sr, x_axis="time", y_axis="mel"); plt.colorbar(format="%+2.0f dB"); plt.title("Mel Spectrogram (dB)"); plt.tight_layout()
Inspect rhythmic patterns and timbral changes; strong drum hits appear as broad energy bursts across bands.
Reflect and compare

Compare the music Mel spectrogram to the provided heart sound spectrogram (phonocardiogram). Notice the periodicity and band energy patterns differ between music beats and cardiac cycles.
Optional exploration:
Change n_mels to 64 or 256 and replot.
Add fmax=8000 for speech-like focus: librosa.feature.melspectrogram(..., fmax=8000).
Adjust hop_length for sharper time detail (e.g., hop_length=256).
