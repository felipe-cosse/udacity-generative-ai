In this hands-on exercise, you will build a simple image-to-image search engine using CLIP (Contrastive Language–Image Pre-training) from Hugging Face. The workflow follows the preceding concept: load a pre-trained multimodal model, embed images, and retrieve visually similar items via cosine similarity. Real data from the “xai-org/RealworldQA” test split (765 diverse images) is used. This capability powers product search, visual recommendations, and duplicate detection in industry.

Prerequisites:
Classroom workspace with internet access
Python 3.8+ with packages: transformers, datasets, torch, torchvision, pillow, matplotlib, tqdm, numpy
Optional GPU for speed (CUDA)
Basic familiarity with Jupyter/Notebook execution
Objectives:
By the end of this exercise, be able to:

Load and use a pre-trained CLIP model and processor
Create normalized image embeddings in batches
Implement image-to-image search using cosine similarity and visualize results
Steps
Open the notebook and verify environment

To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l2/exercises/2-clip/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Run helper: grid display

Execute the display_grid helper in Step 1 to visualize images in a grid.
This function resizes, crops, and displays images without manual tensor handling.
Load CLIP model and processor

In Step 2, complete the TODOs to load the model and processor:
processor = CLIPProcessor.from_pretrained(model_name)
model = CLIPModel.from_pretrained(model_name)
Optional (if using device): model.to(device)
Load the dataset

In Step 3, complete the TODO to load the RealworldQA test split from Hugging Face Datasets:
dataset = load_dataset("xai-org/RealworldQA", split="test")
Visualize a sample grid:
images = dataset["image"]; display_grid(images[:25], nrow=5)
Note: This dataset is small and diverse, suitable for rapid experimentation.
Batch image embeddings

In Step 4, complete the TODOs to preprocess images and extract embeddings in batches:
inputs = processor(images=batch, return_tensors="pt", padding=True)
Optional: if using device, move inputs to it (e.g., inputs = {k: v.to(device) for k, v in inputs.items()})
with torch.no_grad(): image_features = model.get_image_features(**inputs)
Normalization is already included in the code (unit-length embeddings). This makes cosine similarity equivalent to a dot product.
Implement image-to-image search

In Step 5, complete the TODOs inside search_images:
Preprocess the query image:
inputs = processor(images=[query_image], return_tensors="pt", padding=True)
Optional device move as above
Extract features:
with torch.no_grad(): query_image_features = model.get_image_features(**inputs)
Normalize the query features (already shown in the code).
Compute cosine similarities via matrix multiplication:
similarities = torch.matmul(query_image_features, image_embeddings.T)
Sort in descending order and take the top_k indices (already scaffolded).
Optional: enable plot=True to see retrieved images in a grid with scores.
Run searches and interpret scores

In Step 6, run:
street_image = images[222]
indices, scores = search_images(image_embeddings, street_image, top_k=5, plot=True)
Explanation: the first result is the query image itself (present in the dataset), hence a score of 1 due to identical normalized vectors.
Try another image:
query_image = images[0]
indices, scores = search_images(image_embeddings, query_image, top_k=5, plot=True)
Inspect retrieved images. Observe how visually similar images cluster due to embedding proximity.
Optional enhancements (if time permits)

Change top_k to return more results.
Swap to a different CLIP variant (e.g., openai/clip-vit-base-patch16) for quality/speed trade-offs.
Cache embeddings to disk (torch.save / torch.load) to avoid recomputation.
Add device handling to accelerate with GPU and ensure inputs/features are kept on the same device.
