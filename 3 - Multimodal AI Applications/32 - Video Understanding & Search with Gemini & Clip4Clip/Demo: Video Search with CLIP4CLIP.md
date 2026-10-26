THis demo shows how CLIP4CLIP enables semantic search across a collection of videos by bringing both text and video into a shared embedding space. Real-world uses include media asset search, content discovery, sports highlight retrieval, and enterprise knowledge archives. This demo shows how to:

Convert videos into embeddings with a frame-based pipeline
Encode text queries in the same space
Compute similarities and return the most relevant videos

Workflow Summary
Import libraries and set up preprocessing transforms.
Sample and preprocess frames from each video (resize, crop, normalize).
Load CLIP4CLIP vision and text encoders plus tokenizer.
Create embeddings:
Per-video: encode frames, normalize per-frame, average, normalize final vector.
Per-query: tokenize, encode, normalize.
Build an embedding database for all videos.
Search:
Encode query text.
Compute cosine similarity (dot product on normalized vectors).
Return top-k matches with scores.
Step-by-Step Instructions
Step 1: Setup
To use the Udacity workspace:

Click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l4/demos/3-clip4clip/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the environment named the same as this activity’s directory.
Step 2: Frame preprocessing and sampling
Purpose: Convert each video into a tensor of normalized frames.

def preprocess_frame(size, n_px):
    return Compose([
        Resize(size, interpolation=InterpolationMode.BICUBIC),
        CenterCrop(size),
        ToTensor(),
        Normalize((0.48145466, 0.4578275, 0.40821073),
                  (0.26862954, 0.26130258, 0.27577711)),
    ])(n_px)

def video2frames(video_path, frame_rate=1.0, size=224):
    cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps < 1:
        raise IOError(f"ERROR: problem reading video file: {video_path}. No frames found.")
    total_duration = (frameCount + fps - 1) // fps
    frames_idx = np.floor(np.arange(0, total_duration*fps, fps/frame_rate))
    images = np.zeros([len(frames_idx), 3, size, size], dtype=np.float32)
    last_frame = 0
    for i, idx in enumerate(frames_idx):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        last_frame = i
        images[i] = preprocess_frame(size, Image.fromarray(frame))
    images = images[:last_frame+1]
    cap.release()
    return torch.tensor(images)
Step 3: Load CLIP4CLIP models
Purpose: Prepare encoders for vision (frames) and text.

model_name = "Searchium-ai/clip4clip-webvid150k"
vision_model = CLIPVisionModelWithProjection.from_pretrained(model_name).eval()
text_model   = CLIPTextModelWithProjection.from_pretrained(model_name).eval()
tokenizer    = CLIPTokenizer.from_pretrained(model_name)
Step 4: Embedding functions
Purpose: Produce normalized vectors for videos and text.

@torch.no_grad()
def get_video_embedding(video_frames: torch.Tensor) -> torch.Tensor:
    visual_output = vision_model(video_frames)
    embeddings = visual_output["image_embeds"]
    embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)
    video_embedding = embeddings.mean(dim=0)
    return video_embedding / video_embedding.norm(dim=-1, keepdim=True)

@torch.no_grad()
def get_text_embedding(text_query: str) -> torch.Tensor:
    inputs = tokenizer([text_query], padding=True, return_tensors="pt")
    text_output = text_model(**inputs)
    e = text_output.text_embeds
    return (e / e.norm(dim=-1, keepdim=True)).squeeze(0)
Step 5: Build the embedding database
Purpose: Convert all videos into a searchable tensor.

video_paths = glob.glob("videos/*")
video_embeddings = []
for p in tqdm(video_paths, desc="Embedding videos"):
    try:
        frames = video2frames(p)
        video_embeddings.append(get_video_embedding(frames))
    except Exception as e:
        print(f"Error processing {p}: {e}")
video_embeddings_tensor = torch.stack(video_embeddings)  # shape: [N, D]
Step 6: Search function and queries
Purpose: Return top-k most similar videos for a text query.

def search_videos(query_text, video_embeddings_tensor, video_paths, top_k=3):
    text_embedding = get_text_embedding(query_text)
    similarities = torch.matmul(text_embedding, video_embeddings_tensor.T)
    top_indices = similarities.argsort(descending=True)[:top_k]
    return [(video_paths[i], float(similarities[i])) for i in top_indices]

# Example queries
queries = ["animal playing", "I love motor sports!", "airport life"]
for q in queries:
    results = search_videos(q, video_embeddings_tensor, video_paths, top_k=3)
    print(f"\n{q}")
    for rank, (path, score) in enumerate(results, 1):
        print(f"{rank}. {path}  sim={score:.3f}")
Takeaways
Text and videos can be aligned in one vector space, enabling natural-language search over visual content.
Proper frame sampling and normalization strongly affect retrieval quality and speed.
Cosine similarity on unit-normalized embeddings is simple, fast, and effective.
For production systems, consider:
Frame-rate tuning, keyframe extraction, or scene detection
Larger or domain-adapted models
Hybrid retrieval (metadata + embeddings)
Caching, ANN indices (e.g., FAISS), and re-ranking to scale to large catalogs
Robust error handling and logging are essential for real datasets with varied formats and quality.






In the next few minutes, we're going to learn how to build a video search system using CLIP4CLIP. This model can understand both video content and text descriptions, allowing us to search through videos using natural language queries. Here we go. We begin by importing all the necessary libraries. We're using PyTorch for the deep learning framework, OpenCV for video processing, and the transformers library to load our CLIP4CLIP model. We also import some utilities for visualization and progress tracking. Next, we define our video processing functions. The first function pre process frame creates a composition of transformations that will be applied to each video frame. We resize the frame, center crop it, to make it square, convert it to a tensor, and then normalize it using the specific mean and standard deviation values that clip was trained with. The second function video to frames is where the actual video processing happens. We open the video file using OpenCV, get its frame count and frames per second, then calculate which frames we want to extract based on our desired frame rate. Here we are using a simple uniform frame extraction technique, but more advanced techniques are also available. We extract these frames one by one, convert them from the BGR color space used by OpenCV to the RGB color space, apply our pre processing function, and store them in a tensor. If we exit the loop early, we truncate the tensor to avoid black frames at the end. Now, let's load the CLIP4CLIP models. Here's something interesting. We actually load the model twice once as a vision model and once as a text model. This slightly awkward way of doing things is currently the suggested way to use this model within the hugging face library. CLIP4CLIP brings both videos and text into the same embedding space, so we can compare them directly. We're using the vision model with projection and the text model with projection, which means they both output embeddings in the same dimensionality. We also load the tokenizer which we'll use to process text queries. We then define our video embedding function. This takes the pre processed frames and passes them through the vision model. We wrap everything in torch, no grad because we don't want to compute gradients during inference, which would slow things down unnecessarily. After getting the embeddings for each frame, we normalize them at the frame level so that all frames contribute equally to the final embedding for the video. Then crucially, we take the mean across all frames to get a single embedding vector for the entire video. This is important. We are combining the embeddings for each frame into one global embedding for the video. We then normalize again this final embedding as well. The text embedding function works similarly. We tokenize the text query using the tokenizer. We then pass these through the text model to get our text embedding, normalize it, and squeeze out the extra dimension to get a one dimensional vector. Now that we have our model and processing functions ready, let's load some sample videos. We use globe to find all video files in our videos. In this case, we have three videos, one showing luggage at an airport, one showing motocross racing, and one showing a dog playing. Let's watch them. Let's process all these videos and create our embeddings database. We look through each video path, convert the video to frames using our video to frames function, then get the embedding using our video embedding function. We collect all these embeddings and stack them into a single tensor. This gives us a tensor of shape 3/512, meaning three videos each, represented by a 512 dimensional embedding vector. Now for the fun part, the search function. We take a text query and convert it to an embedding using our text embedding function. Since both our text and video embeddings are normalized, we can calculate cosine similarity by simply doing a product. We use matrix multiplication between the text embedding and the transposed video embeddings, tensor to get similarity scores for all videos at once. We then sort these similarities in descending order and grab the top k results. Let's try it out with some queries. First, we search for animal playing. The system correctly ranks the dog video first. Notice how it's using semantic understanding, not just keyword matching. Next, we search for I love motor sports. The motocross video comes out on top. Again, the model understands that motocross is a motor sport, even though those exact words don't appear together. Finally, we search for Airport life, and the luggage video ranks first. The model correctly associates luggage with airports. Before we finish, let me note that when implementing a real video search system, there are many choices to make, which embedding model to use, how to sample frames, which similarity metrics to apply. Real systems often include hybrid searches that combine metadata with embeddings, searches across multiple embedding types, and additional re ranking steps to improve results. This concludes our demo for today, thanks for watching.