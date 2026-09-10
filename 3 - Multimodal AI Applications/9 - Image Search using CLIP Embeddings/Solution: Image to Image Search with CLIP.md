This solution walkthrough demonstrates an image-to-image search system using CLIP to match a query image against a gallery. The exercise demonstrates how to load a pre-trained model, create embeddings for images, and retrieve the most similar images using cosine similarity.

This walkthrough emphasizes:

Using a pre-trained CLIP model and processor from Hugging Face
Creating batched image embeddings efficiently
Implementing cosine similarity search through matrix multiplication
Explaining why self-matches score 1.0

Step-by-Step Instructions
To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l2/exercises/2-clip/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
1) Helper: display images in a grid
A small utility shows images in a grid to inspect results.

Converts PIL.Image to tensors using a transform
Resizes and center-crops to 256x256
Uses torchvision.utils.make_grid and matplotlib to display
Snippet:

def display_grid(images, *args,* *kwargs):
    transform = T.Compose([T.Resize(256), T.CenterCrop(256), T.ToTensor()])
    tensors = [transform(img) for img in images]
    grid = torchvision.utils.make_grid(tensors, *args,* *kwargs)
    _, sub = plt.subplots(dpi=300)
    sub.imshow(grid.permute(1, 2, 0)); sub.axis("off"); plt.show()
2) Import and load CLIP
Load the model and processor:

CLIPProcessor handles preprocessing for images (and text if needed).
CLIPModel provides get_image_features for embeddings.
from transformers import CLIPProcessor, CLIPModel
model_name = "openai/clip-vit-base-patch32"
processor = CLIPProcessor.from_pretrained(model_name)
model = CLIPModel.from_pretrained(model_name)
# Optional: model.eval()
3) Load a small, diverse dataset
Use the test split of xai-org/RealworldQA. This split contains ~765 images, which is convenient for a fast prototype.

from datasets import load_dataset
dataset = load_dataset("xai-org/RealworldQA", split="test")
images = dataset['image']
display_grid(images[:25], nrow=5)
4) Create image embeddings in batches
Generate feature vectors for every image:

Preprocess with processor(images=..., return_tensors="pt", padding=True)
Compute embeddings with model.get_image_features(**inputs)
Normalize embeddings so each vector has unit length
Concatenate batches into a single tensor of shape [num_images, embed_dim]
def get_image_embeddings_batch(images, batch_size=32):
    all_embeddings = []
    for i in range(0, len(images), batch_size):
        batch = images[i: i + batch_size]
        inputs = processor(images=batch, return_tensors="pt", padding=True)
        with torch.no_grad():
            feats = model.get_image_features(**inputs)
        feats = feats / feats.norm(dim=-1, keepdim=True)
        all_embeddings.append(feats)
    return torch.cat(all_embeddings, dim=0)

image_embeddings = get_image_embeddings_batch(images)
Why normalization matters:

Cosine similarity for normalized vectors reduces to a dot product.
This simplifies retrieval to a matrix multiplication.
5) Implement image-to-image search
Given a query image:

Preprocess the image with the same processor
Get query_image_features = model.get_image_features(**inputs)
Normalize the query vector
Compute similarity via torch.matmul(query_image_features, image_embeddings.T)
Sort and take top_k indices and scores
Optionally visualize matches
def search_images(image_embeddings, query_image, top_k=5, plot=False):
    inputs = processor(images=[query_image], return_tensors="pt", padding=True)
    with torch.no_grad():
        q = model.get_image_features(**inputs)
    q = q / q.norm(dim=-1, keepdim=True)
    similarities = torch.matmul(q, image_embeddings.T)  # cosine for normalized vectors
    top_indices = similarities[0].argsort(descending=True)[:top_k]
    scores = similarities[0][top_indices]
    if plot:
        display_grid([images[int(i)] for i in top_indices], nrow=5)
    return top_indices, scores
Shapes to expect:

q: [1, d]
image_embeddings: [N, d]
similarities: [1, N]
6) Run searches and interpret results
Use an image from the dataset (e.g., images[222]) as the query.
Expect the first result to be the same image with score 1.000.
Reason:

The exact same image appears in the gallery.
With normalization, cosine similarity cos(x, x) = 1 because a vector has maximum similarity with itself.
indices, scores = search_images(image_embeddings, images[222], top_k=5, plot=True)
Try another query:

search_images(image_embeddings, images[0], top_k=3, plot=True)
Remember:

Normalize embeddings before cosine similarity; then similarity equals the dot product.
Use the same preprocessing for both gallery and query to ensure meaningful matches.






Let's look together at the solution for the exercise about CLIP and image search. After the helper functions, you had to load the CLIP model using the Hugging Face transformers library. This is done with the from_pretrained methods of the CLIP processor and model classes. Next, you had to load the test split of the Realworld Q/A dataset. This is done by providing the name of the dataset and the split to the load dataset function from the Hugging Face datasets library. The code then displays some of the images which are pretty diverse, including street images, pets, and other things. Now, to the critical part of the exercise, you had to complete this function. Here, we're processing batches of images, and we need to run the CLIP pre-processor on the batch. This is done by calling the processor, providing the batch, the return of tensors option, as well as padding equals True to make sure the images are appropriately sized. Next, within a no_grad context manager, we need to call the CLIP model. Since here we're embedding images, we call the get_image_features method and provide our pre-processed inputs. After that, the code normalizes the embeddings and stores them. Let's keep moving. Next, you had to implement the image to image search by completing this function. First step, just like before, we need to pre-process the query image by running the pre-processor on it. Note that the pre-processor expects batches of images, not one image, so we pass in a batch of one, that is a list of one image. Then just like before, you had to call the get_image_features from CLIP. Now, you had to compute the cosine similarity between the query_image and the images we have in our dataset. The code normalizes the features we just obtained and reminds you that the embeddings of the images in the dataset have already been normalized. All you need to do now is take the matrix multiplication of the embedding of the query_image and the pre-computed image_embeddings. The code then sorts the scores, takes the first k and returns them. That we've done all the work, let's have some fun testing our image to image search. If we start from a street level image like this and then run our search, we end up with similar street level images. The first image of any result is always the image we provide because we're using queer images that belong to the dataset. The first result is the image itself, which is obviously identical to itself. Let's try with one more example. This time, video game consoles are our query, and let's see what we get. We get an audio soundboard and boxes of electronics, which kind makes sense. This concludes the exercise, good job completing it and see you next time.