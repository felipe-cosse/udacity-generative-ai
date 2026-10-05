This demo shows how CLAP (Contrastive Language–Audio Pre-training) enables:

Sound-to-sound search using acoustic similarity
Text-to-sound retrieval using natural language queries
Zero-shot audio classification without task-specific training
Real-world uses include sound effect library search, rapid audio tagging, content discovery for media production, and indexing large audio archives with text queries. The workflow covers model setup, dataset loading, embedding computation, similarity search, and classification.

Prerequisites and setup
ffmpeg < 8 is installed with dynamic library libavutil available
Python environment with transformers, datasets, librosa, numpy, pandas, scikit-learn
Step-by-step instructions
To use the Udacity workspace:

At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/demos/2-clap/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
1) Load model and dataset
model = ClapModel.from_pretrained("laion/clap-htsat-unfused")
processor = ClapProcessor.from_pretrained("laion/clap-htsat-unfused")

dataset = load_dataset("ashraq/esc50", split="train")
print(f"Loaded {len(dataset)} audio samples")
pd.Series(sorted(set(dataset["category"]))).to_frame("categories")
Tips:

CLAP expects 48 kHz audio at inference in this pipeline
ESC-50 provides short environmental sounds with labels
2) Define helper functions for embeddings
def get_audio_embedding(audio_array, sample_rate=22050):
    inputs = processor(audios=audio_array, sampling_rate=48000, return_tensors="pt")
    with torch.no_grad():
        audio_embed = model.get_audio_features(**inputs)
    return audio_embed.numpy()

def get_text_embedding(text):
    inputs = processor(text=text, return_tensors="pt")
    with torch.no_grad():
        text_embed = model.get_text_features(**inputs)
    return text_embed.numpy()
Note:

Audio is processed at 48 kHz inside the processor
torch.no_grad() avoids gradient computation for efficiency
3) Pre-compute embeddings for the dataset
def process_audio_batch(batch):
    audio_arrays = [audio['array'] for audio in batch]
    return {'embedding': get_audio_embedding(audio_arrays, sample_rate=22050)}

processed_dataset = dataset.map(
    process_audio_batch,
    batched=True,
    batch_size=32,
    input_columns=['audio'],
)
Why pre-compute:

Similarity search requires pairwise comparisons; pre-computation speeds up later steps
4) Sound-to-sound similarity search
Select a query sound and compute similarities against all embeddings:

random.seed(999)
query_idx = random.randint(0, len(dataset) - 1)
query_sample = dataset[query_idx]
query_audio = query_sample["audio"]["array"]
query_sr = query_sample["audio"]["sampling_rate"]

# Listen to the query if desired
display(Audio(data=query_audio, autoplay=False, rate=query_sr))

query_embedding = get_audio_embedding(query_audio, query_sr)

# Normalize embeddings and compute cosine similarities via dot product
A = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
B_ = np.vstack(processed_dataset["embedding"])
B = B_ / np.linalg.norm(B_, axis=1, keepdims=True)
similarities = np.matmul(A, B.T).squeeze()

ds_with_similarity = processed_dataset.add_column("similarity", similarities).sort(
    "similarity", reverse=True
)

# Top-3 similar (excluding the query itself at rank 0)
for row in ds_with_similarity.select(range(1, 4)):
    print(f"{row['filename']} ({row['category']}) - Similarity: {row['similarity']:.3f}")
    display(Audio(data=row['audio']['array'], autoplay=False, rate=row['audio']['sampling_rate']))
What happens:

Embeddings are L2-normalized
Cosine similarity reduces to a dot product
Results are ranked and listened to for validation
5) Text-to-sound search
Retrieve the most relevant sounds for a text description:

search_query = "A hike in the woods"
query_text_embedding = get_text_embedding(search_query)

similarities = cosine_similarity(
    query_text_embedding,
    np.vstack(processed_dataset["embedding"])
).squeeze()

ds_with_similarity = processed_dataset.add_column("similarity", similarities).sort(
    "similarity", reverse=True
)

for row in ds_with_similarity.select(range(1, 4)):
    print(f"{row['filename']} ({row['category']}) - Similarity: {row['similarity']:.3f}")
    display(Audio(data=row['audio']['array'], autoplay=False, rate=row['audio']['sampling_rate']))
What happens:

Text is embedded into the same space as audio
Cosine similarity ranks the most semantically relevant audio
6) Zero-shot audio classification
Classify arbitrary sounds using label descriptions without training:

import glob
from pathlib import Path

sounds = Path("sounds").glob("*.mp3")
ground_truth = [x.stem for x in sounds]
audio_arrays = [librosa.load(f, sr=48000)[0] for f in glob.glob("sounds/*.mp3")]

for audio, gt in zip(audio_arrays, ground_truth):
    print(f"Ground truth: {gt}")
    display(Audio(data=audio, autoplay=False, rate=48000))

category_descriptions = ["drill", "angle grinder", "jackhammer"]

audio_classifier = pipeline(
    task="zero-shot-audio-classification", model="laion/clap-htsat-unfused"
)
output = audio_classifier(audio_arrays, candidate_labels=category_descriptions, top_k=1)

df = pd.DataFrame.from_records([{x["label"]: x["score"] for x in y} for y in output])
df["winning_label"] = df.idxmax(axis=1)
df["ground_truth"] = ground_truth
df
What happens:

Candidate labels are plain text
The pipeline returns scores; highest score becomes the predicted label
Results are assembled into a table for inspection
Takeaways
A single model can align audio and text in a shared embedding space
Similarity search works for audio–audio and text–audio without manual feature engineering
Zero-shot classification supports new tasks and labels without retraining
These techniques accelerate audio search, tagging, and organization across large libraries








Next few minutes, we're going to explore how to use CLAP, a powerful multi modal model for audio understanding tasks like sound similarity, text to audio search, and zero-shot classification. Let's dive in. First, we set up our environment and load the CLAP model. For that, we use from pre-trained methods of the appropriate classes from hugging phase transformers. As usual, we load both the model and the processor. The processor prepares the data in the exact format expected by the model. The CLAP model is trained to understand both audio and text, learning a shared representation that lets us do some pretty interesting things. We'll use the ESC 50 data set, which contains a variety of environmental sounds. We use the load data set from hugging face to load it. We can see the categories of sounds it contains and see they are pretty diverse. After loading the data, we define two helper functions. The first one compute the embeddings for audio. We call the processor on the audio data, specifying the sampling rate needed by CLAP, which is 48 kilohertz. Then we get the audio features from CLAP, which are the embeddings. Finally, we convert them from PyTorch tensors to NumPy and return them. Function to produce text embeddings works very similarly. The only difference is that we give the text as input to the processor, instead of the sounds, and we call get text features from clap instead of get audio features. Great. Now we can compute embeddings for each audio clip. These embeddings are like fingerprints for each sound, capturing their unique characteristics in a way the model can understand. In order to do this, we define a little wrapper around get audio embeddings that we can use on batches of data. Then we use the map function from the hugging phase data set to automatically run it on our entire data set. Here, we specify that we want to do batches and the batch size. We also specified that we only need the audio column. Now that we have embeddings for our entire data set, we'll pick a random sound from the data set and use CLAP to find other sounds that are acoustically similar. No manual feature engineering needed. Let's get the random sample, and let's listen to it. Great. Now, we compute the cosine similarity between our query sound and all other sounds in the data set. Cosine similarity is the matrix multiplication of our query embeddings times all other embeddings transposed divided by the norms. Let's do this, then listen to the top matches. The results make a lot of sense. Next, we'll try searching for sounds using natural language. For example, we can type in a description like a hike in the woods and clap we'll find the most relevant audio clips. This shows how the model connects text and audio in a shared space, enabling intuitive search experiences. The only thing we need to do differently is the query embedding. We now generate the query embedding from the text instead of the sound as we did previously. Everything else stays the same. Let's see what the model selects. These are all sounds of people walking in the woods, which makes a lot of sense given our query text. Finally, we look at zero-shot audio classification. This means we can classify sounds using any set of text labels, even if the model hasn't seen them during training. We load some sample sounds and listen to them. They are sounds of tools. These are not in the CLAP training data set. Next, we define our classes, and let CLAP predict the most likely label for each sound. This time, we use the hugging face pipeline, which does this for us in a very convenient way. The results are displayed in a simple table so we can see how well the model performs. The first three columns give the class probabilities for our classes, the fourth column is the label with the highest probability, and the fifth column is the true label. As you can see, the model is working well. To sum up, CLAP makes it easy to find similar sounds, search audio with text, and classify sounds using natural language, all without manual feature engineering or retraining. Thanks for following along.