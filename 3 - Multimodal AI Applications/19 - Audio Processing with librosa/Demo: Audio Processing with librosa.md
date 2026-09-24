This demo shows practical audio processing workflows using librosa and soundfile. The focus is on loading audio safely, changing sample rates and formats, and creating Mel spectrograms for machine learning and analysis. Such steps map directly to real-world tasks like:

Preparing datasets for speech recognition and speaker verification
Music information retrieval and tagging
Environmental sound classification and monitoring
Feature extraction pipelines for audio models
What will be learned:

How to load audio with or without resampling
How to convert sample rates and save to common formats
How to create and interpret Mel spectrograms
How to compare spectra for voice, music, and ambient noise

Step-by-Step Instructions
To use the Udacity workspace:

At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/demos/1-librosa/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
1) Load audio and inspect basics
Load with native sample rate to avoid unintended resampling.
Inspect array shape, sample rate, and duration.
Optional: play audio in a notebook.
import librosa
from IPython.display import Audio, display

audio_file = "LJ037-0171.wav"  # replace with a file path

# Load using native sample rate
y, sr = librosa.load(audio_file, sr=None)

print(f"Audio shape: {y.shape}")
print(f"Sample rate: {sr} Hz")
print(f"Duration: {len(y)/sr:.2f} seconds")

display(Audio(y, rate=sr))
Tips:

librosa.load defaults to mono by averaging channels. To keep stereo, use mono=False.
Use sr=None to preserve the file’s original sample rate.
2) Convert sample rates and save in different formats
Resample to standard rates (e.g., 16 kHz for speech models, 44.1 kHz for music).
Save as FLAC, OGG, WAV (16/24-bit), and MP3.
# Resample
y_16k, sr_16k = librosa.load(audio_file, sr=16000)
y_44k, sr_44k = librosa.load(audio_file, sr=44100)

print(f"Original: {len(y)} samples at {sr} Hz")
print(f"16 kHz: {len(y_16k)} samples at {sr_16k} Hz")
print(f"44.1 kHz: {len(y_44k)} samples at {sr_44k} Hz")

# Save to multiple formats
import soundfile as sf

sf.write('output.flac', y, sr)                              # FLAC (lossless)
sf.write('output.ogg',  y, sr, format='OGG', subtype='VORBIS')  # OGG (lossy)
sf.write('output_pcm16.wav', y, sr, subtype='PCM_16')       # WAV 16-bit
sf.write('output_pcm24.wav', y, sr, subtype='PCM_24')       # WAV 24-bit

# MP3 support depends on backend; bitrate via mode + compression_level
sf.write("output_mp3_CBR.mp3", y, sr, bitrate_mode='CONSTANT',  compression_level=0.5)
sf.write("output_mp3_VBR.mp3", y, sr, bitrate_mode='VARIABLE',  compression_level=0.5)

print("Saved in FLAC, OGG, WAV (16/24-bit), and MP3 formats.")
Notes:

Choice of sample rate depends on downstream models and storage needs.
Lossless formats suit archival and training data preparation; lossy formats suit distribution.
3) Create a Mel spectrogram
Convert power to decibels for better visualization.
Use an adequate number of Mel bands (e.g., 128–256) based on task.
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

fig, ax = plt.subplots()
librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel', ax=ax)
ax.set(title='Mel Spectrogram')
plt.show()
4) Compare voice, music, and ambient noise
Load short segments of voice and music.
Create filtered noise to simulate ambience.
Visualize normalized Mel spectrograms side by side using a consistent color scale.
import numpy as np
import matplotlib.pyplot as plt
import librosa, librosa.display
from IPython.display import Audio, display
from scipy.signal import butter, filtfilt

duration = 5
sr = 22050
t = np.linspace(0, duration, int(sr * duration))

voice = librosa.load('LJ037-0171.wav', sr=sr)[0][:len(t)]
music = librosa.load('piano.mp3', sr=sr)[0][:len(t)]

noise = np.random.normal(0, 0.1, len(t))
b, a = butter(3, 0.1)
ambient = filtfilt(b, a, noise)

display(Audio(voice, rate=sr))
display(Audio(music, rate=sr))
display(Audio(ambient, rate=sr))

fig, axes = plt.subplots(3, 1, figsize=(10, 6.5))
for i, (audio, title) in enumerate([(voice, "Voice"), (music, "Music"), (ambient, "Ambient Noise")]):
    mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=256)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    librosa.display.specshow(mel_db, sr=sr, x_axis='time', y_axis='mel',
                             ax=axes[i], vmin=-60, vmax=0, cmap='magma')
    axes[i].set_title(title)
plt.tight_layout(); plt.show()
Observed patterns:

Voice: clear harmonics, formant bands, intermittent energy.
Music: rich harmonic content across bands, structured rhythms.
Ambient noise: broad, less structured distribution, often lower energy.
Takeaways
Keep original sample rate with sr=None when preservation is required; choose task-appropriate target rates otherwise.
Use lossless formats for training and archival; lossy formats for delivery where size matters.
Mel spectrograms provide compact, perceptually aligned features widely used in audio ML.
Consistent normalization and color scales enable fair visual comparison across signals.
Be mindful of mono vs stereo behavior in librosa.load; set mono=False if channel separation is needed.






Dive into some basic sound processing techniques using Librosa, a Python library for sound manipulation. We'll start by loading a sound file. We first import Librosa and the audio class, which will allow us to listen to the sound directly here in the Jupyter Notebook. We specify the file name and load it with its native sample rate. The variable y now contains the sound samples as a numpy array, and sr is the sample rate inferred from the file. We print the shape, sample rate, and duration of the sound signal. Finally, we use the audio widget to play it back right in the Notebook. Let's hear it. The examination and testimony of the experts enabled the commission to conclude that five shots may have been fired. Next, let's see how to convert between different sample rates. We load the same file at 16 kilohertz and 44.1 kilohertz, and we let Librosa handle the sample rate conversion. We print out the number of samples and sample rates for each version, so you can see how this operation changes the data. As expected, resampling from the original to 16 kilohertz roughly halves the number of samples while up sampling to 44.1 kilohertz roughly doubles it. Now, let's talk about saving in different formats. For that, we use a separate library called sound file. We import sound file SSF, and now we can save our data in many different formats such as FLAC, OGG, and WAV, with both 16 bit and 24 bit depth. For MP3, we use the compression level to control the beat rate since a sound file doesn't let us set it directly. This shows how easy it is to convert between formats using Python. Moving on to feature extraction, we create a Mel Spectrogram. We use Librosa Mel Spectrogram function, converted to decibels and plotted using Matplotlib. A Mel Spectrogram is a way to visualize how the energy in a sound signal is distributed across different frequencies over time. But instead of using a linear frequency scale, it uses the mel scale, which better matches how humans here pitch. To make a Mel Spectrogram, Librosa splits the signal into short frames, calculate the energy at each frequency, and then map those frequencies onto the mel scale. The result is a 2D plot like this one. Time runs along the x axis. Mel scale frequency is on the y axis, and color shows the intensity or energy. Mel Spectrograms are widely used in sound and speech processing because they highlight the features that are most important for human perception and for machine learning models. To make things more interesting, let's compare the Mel Spectrogram for different types of signals. : voice, music, and ambient noise. Let's get one example for each. For voice, we use our original file. For music, we load a piano sample. For noise, we generate wide noise and apply a simple low pass filter to simulate ambient noise. Let's hear the piano. We now let's hear the noise. We then plot the Mel Spectrograms for all three signals on the same scale so you can easily compare them. Let's look at the results. Voice shows clear harmonic structure with energy concentrated in these regularly spaced intervals. The piano music has rich harmonics and rhythmic patterns while noise is more spread out and less structured. In summary, we've covered loading sound files, converting formats and sample rates, creating Mel Spectrograms, and comparing different signal types. Mel Spectrograms are especially useful for machine learning applications as they capture the most important features of audio in a compact form. This concludes our demo today, thanks for following along.