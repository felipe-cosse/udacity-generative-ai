Build a simple, practical image search that matches natural language queries to images. This mirrors real-world use cases such as product search, media library search, creative discovery, and content organization. Learn how CLIP links text and images, how to create embeddings, and how to rank images by similarity.

What this covers:

Loading a pre-trained CLIP model and processor from Hugging Face
Preparing images and text for the model
Creating normalized embeddings
Computing cosine similarity to retrieve top matches
Visualizing search results

Step-by-Step Instructions
Configuration
To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l2/demos/2-clip/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Load the CLIP model and processor by name (“openai/clip-vit-base-patch32”).
Load a small test dataset (RealworldQA) and preview a grid of images to verify inputs.
Create image embeddings:
Batch the images to improve speed.
Use CLIP’s image preprocessor.
Compute image features with no gradient.
L2-normalize embeddings for cosine similarity.
Search with text:
Tokenize text using the processor.
Get text features and L2-normalize.
Compute cosine similarity via matrix multiplication between text and image embeddings.
Sort and return top_k indices and scores.
Optionally visualize matches.
Try several queries and compare results.
Code Used in the Demo
1) Helper: Display Image Grid
import torch
import torchvision
import torchvision.transforms as T
import matplotlib.pyplot as plt
from PIL import Image
from typing import List

def display_grid(images: List[Image.Image], *args,* *kwargs):
    transform = T.Compose([T.Resize(256), T.CenterCrop(256), T.ToTensor()])
    tensors = [transform(img) for img in images]
    grid = torchvision.utils.make_grid(tensors, *args,* *kwargs)
    _, sub = plt.subplots(dpi=300)
    sub.imshow(grid.permute(1, 2, 0))
    sub.axis("off")
    plt.show()
2) Import and Load CLIP
from transformers import CLIPProcessor, CLIPModel

model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name, fast_processor=True)

print("Model loaded successfully!")
3) Load Dataset
from datasets import load_dataset
from tqdm import tqdm

dataset = load_dataset("xai-org/RealworldQA", split="test")
images = dataset["image"]
display_grid(images[:50], nrow=5)
4) Create Image Embeddings (Batched + Normalized)
import numpy as np

def get_image_embeddings_batch(images, batch_size=32):
    all_embeddings = []
    for i in tqdm(range(0, len(images), batch_size), total=int(np.ceil(len(images) / batch_size))):
        batch = images[i : i + batch_size]
        inputs = processor(images=batch, return_tensors="pt", padding=True)
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        all_embeddings.append(image_features)
        if (i + batch_size) % 100 == 0 or (i + batch_size) >= len(images):
            print(f"Processed {min(i + batch_size, len(images))} images...")
    return torch.cat(all_embeddings, dim=0)

print("Creating embeddings for all batches of images...")
image_embeddings = get_image_embeddings_batch(images)
print(f"Created embeddings with shape: {image_embeddings.shape}")
5) Text-to-Image Search with Cosine Similarity
def search_images(
    image_embeddings: List[torch.Tensor],
    query_text: str,
    top_k: int = 5,
    plot: bool = False,
):
    inputs = processor(text=[query_text], return_tensors="pt", padding=True)
    with torch.no_grad():
        text_features = model.get_text_features(**inputs)
    print(f"Text has been transformed to embedding vector of shape {text_features[0].shape} ...")

    text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    similarities = torch.matmul(text_features, image_embeddings.T)

    top_indices = similarities[0].argsort(descending=True)[:top_k]
    scores = similarities[0][top_indices]

    if plot:
        for i, score in zip(top_indices, scores):
            print(f"{i+1} - {score:.3f}")
        display_grid([images[int(i)] for i in top_indices], nrow=5)

    return top_indices, scores
6) Example Searches
indices, scores = search_images(image_embeddings, "An animal", top_k=3, plot=True)
search_images(image_embeddings, "A picture of a toy", top_k=3, plot=True)
search_images(image_embeddings, "A city road on a rainy day", top_k=3, plot=True)
Takeaways
Building a basic image search with CLIP requires only a few components: preprocessing, embeddings, normalization, and cosine similarity.
The same workflow scales to larger collections by storing embeddings in a vector database.
Clear separation of offline (image embedding) and online (query embedding + search) steps improves performance.
Visualization helps verify search quality and debug issues.
This forms a foundation for more advanced systems with re-ranking, hybrid search, and metadata filters.





Today we're going to try out the CLIP model. We'll see how it can create embeddings for both images and text, linking them in a multimodal space. This allows us to build interesting applications like an image search system. Let's get started. First, we define a helper function to display many images in a grid. It's going to come useful later. Then we import the CLIP processor and the CLIP model classes from Hugging Face transformers and we instantiate them. Remember, the processor is responsible for preparing the data before they can get fed into the model. Since CLIP handles both images and text, the processor can operate on both modalities. Next, let's load some images so we have a dataset to play with. I've picked this real world dataset from Hugging Face. It contains 765 images that are pretty diverse and will work well for our demo. We now look at a few of those images to get an idea of what this dataset contains. We can see street images, appliances, pets, food, objects, as promised, it's a pretty varied dataset. Now that we have the model and the data, let's create the embeddings. We want to create an image search system where the user inputs a text string, and we find the most relevant images within our dataset for that string. We need to pre compute the embeddings for all the images so that when we get a text query, we can generate the embeddings for that text query and match it with the images, then return the most relevant results. I wrote a function to help us do that. We look over our dataset in batches. For each batch, we preprocess it with the processor, then we extract the embeddings using the get image features method. Then we normalize the embeddings so that their norm is one. This is a key choice. We're going to use the cosine similarity metric, which requires both the query embedding and the image embeddings to have a norm of one. We precomputed this normalization here instead of having to recompute it every time there's a new query. At the end, we concatenate all embeddings in one single tensor. The result has a shape equal to the number of images in the dataset times the size of the embedding vector for one image. In our case, we have 765 images. The embedding size for this version of CLIP is 512 so every image is represented by an embedding vector of size 512. Now that we have our image embeddings, we can create our search function. Given image embeddings and a text query, this function returns the first K most relevant images. We first pre process the text using the processor for CLIP. Among other things, this tokenizes our text. Then we get the embeddings from the model, this time, calling get text features instead of get image features. Then we compute the cosine similarity between the text embedding and the embeddings of all the images. The formula for cosine similarity is A.B divided by the product of the norms of the two vectors. Since we already normalize the image embeddings to have a norm of one, we can do the same with the text embedding and then just do a matrix multiplication. Finally, we sort the similarities in descending order and take the index of the first k results. These are the indices of the images whose embedding is closest to our text embedding. Now let's test it out on some text queries. First, let's look for animals. We can see that indeed we get animals in return. Note that there are only a few images of animals in the data set, so our search is really working. Let's also try with toys, which again, returns good results, and then with a city road on a rainy day. As you can see, our system is working well. In a real world scenario, a real image search engine is a lot more complicated than this. When you have a lot of images, you cannot compute all the cosine similarities between all images and the text vector for every query, so you use approximate searches and vector databases instead. You typically add hybrid searches when you also use image metadata, as well as re ranking techniques to improve performance. We just scratch the surface of how a real system works. But even with this basic example, we can already obtain good and useful results. Good job getting to the end of this demo. See you next time.