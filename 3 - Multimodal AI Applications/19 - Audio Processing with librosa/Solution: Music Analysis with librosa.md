This walkthrough demonstrates a compact audio analysis pipeline using librosa:

Load and resample an MP3 file.
Convert and save to WAV.
Visualize the waveform.
Listen to the audio inline.
Compute and interpret a Mel spectrogram.
Focus: how digital audio becomes data that can be visualized, processed, and interpreted. The same tools support musical signals and non-musical sounds (for example, heart sounds in medical audio).

Librosa provides an accessible way to handle audio as numerical arrays. A typical flow starts with librosa.load, which returns:

y: a NumPy array containing the audio samples (mono by default, float32 between -1 and 1).
sr: the sampling rate in Hz (samples per second).
Saving to WAV with soundfile preserves the waveform and sample rate. Visualizing the waveform reveals amplitude over time. Listening confirms that processing preserved content.

A Mel spectrogram represents energy over time across frequency bands scaled on the Mel scale. The Mel scale groups frequencies in a way that aligns with human hearing. Converting to decibels with librosa.power_to_db improves contrast and readability. Patterns in the Mel spectrogram reveal rhythm (repeating vertical stripes), pitch content (horizontal bands), and instrument timbre (texture across bands).

These visual tools generalize beyond music. The included Mel spectrogram of a phonocardiogram (heart sound) shows how similar methods apply to medical audio to study normal and abnormal conditions.

Step-by-Step Instructions
1) Imports and setup
To use the Udacity workspace:

At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/exercises/1-librosa/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from IPython.display import Audio
import soundfile as sf
librosa and librosa.display for analysis and plotting.
soundfile for writing WAV files.
Audio for inline playback in notebooks.
2) Load the audio file (default settings)
y, sr = librosa.load('music.mp3')
Returns mono audio at the default sample rate (22050 Hz).
For native sampling rate without resampling, use: librosa.load('music.mp3', sr=None)
3) Load at 44.1 kHz (CD quality)
y, sr = librosa.load('music.mp3', sr=44100)
Ensures consistent processing at 44,100 Hz.
Useful for aligning with standard datasets or models expecting this rate.
4) Save as WAV
sf.write('music.wav', y, sr)
Stores the resampled waveform to a lossless format.
WAV is preferred for further processing and reproducibility.
5) Plot the waveform
plt.figure(figsize=(10, 3))
librosa.display.waveshow(y, sr=sr, color='steelblue')
plt.title('Waveform')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()
Displays amplitude over time.
Regions of higher amplitude often correspond to louder sections or percussive hits.
6) Play the audio inline
Audio(y, rate=sr)
Confirms the audio sounds as expected after resampling and conversions.
7) Compute and plot the Mel spectrogram
mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

plt.figure(figsize=(10, 4))
librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel', cmap='magma')
plt.title('Mel Spectrogram (dB)')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()
n_mels=128 creates 128 Mel bands (common for music tasks).
power_to_db converts power to decibels for better dynamic range visualization.
Interpreting the plot:
Low-frequency energy (e.g., kick drum, bass) appears at the bottom.
Higher-frequency content (e.g., cymbals, guitar harmonics) appears higher.
Repeated vertical patterns often indicate beats.
Sustained horizontal bands can reflect held notes or steady tones.
Remember: use Mel spectrograms (in dB) to reveal rhythm, pitch content, and timbre in a way that aligns with human hearing.

Keep sampling rate choices consistent and prefer lossless formats (WAV) for downstream processing and reproducibility.







Welcome. In this exercise, you explored some fundamental audio processing techniques using Librosa, a powerful Python library for audio analysis. Let's walk through each step and see what's happening in the code. We kicked things off by importing the essential libraries, numpy for numerical operations, matplotlib for plotting, Librosas display module for visualizing audio and the audio class to play sound directly in the notebook. First, you loaded the music.mp3 audio file using Librosa load function. This function reads the file and returns both the audio time series as a numpy array and the sample rate. By default, Librosa loads audio at the native sample rate of the file. But you can specify a different sample rate if you want. Next, you loaded the same file again. This time, explicitly setting the sample rate to 44,100 hertz to exercise the on the fly resembling capability of Librosa. Often, AI models need specific sample rates in input. This capability can come in handy. After that, you saved the audio as a wave file using the sound file library. The write function takes the file name, the audio data, and the sample rate, and writes everything out in wave format. This step demonstrated how to convert between audio formats in Python. Moving forward, you visualize the wave form using Librosas wave show function. This plot shows the amplitude of the audio signal over time, giving you a quick sense of the structure of the sound, where the loud and quiet parts are, and how the sound evolves. To listen to the audio, you used the audio component from iPython. By passing in the audio data and the sample rate, you created the player right in the notebook, making it easy to check your results. Let's hear the content of the audio file we loaded. Next, you computed and plotted a mel spectrogram. Using Librosa's melspectrogram function, you generated a representation of the sounds frequency content over time mapped onto the mel scale. You then converted the spectrogram to decibels for easier visualization and plotted it with spectro. This allowed you to see which frequencies are present at different times in the audio. The beat of the drums and the phrasing of the guitar are clearly visible in the spectrogram. Then you had a little challenge to solve. You had to guess what this particular spectrogram image represents. We can now reveal the answer. The image is a mel spectrogram of a healthy heart, recorded as a phonocardiogram with the two characteristics beats. Mel spectrograms are a primary input to deep learning models for medical applications involving sounds. That concludes our solution, congrats in completing this exercise, and see you next time.