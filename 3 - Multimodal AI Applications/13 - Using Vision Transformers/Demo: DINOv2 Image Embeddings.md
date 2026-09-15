This is a hands-on walkthrough of extracting image embeddings with DINOv2 (Vision Transformer, self-supervised). The demo shows how a ViT turns an image into tokens, how to read the CLS embedding (global image representation), how to compare images using cosine similarity, and how to use DINOv2 as a frozen backbone for a small classifier. Real-world uses include image search and retrieval, deduplication, clustering, and as a strong starting point for classification, detection, and segmentation.

Note: DINOv3 is a small upgrade trained with more data/compute. Concepts and steps here transfer. Access to DINOv3 requires registration with Meta’s Hugging Face organization.

Process overview (what happens)
Load DINOv2 model and processor from Hugging Face.
Load and display sample images.
Inspect ViT patch size and token structure (CLS, registers, patches).
Extract embeddings and validate shapes.
Compute cosine similarity between images using CLS tokens.
Optional: fine-tune a small classifier with a frozen DINOv2 backbone.
Step-by-step instructions
1) Imports and helper
import torchvision
import torchvision.transforms as T
import matplotlib.pyplot as plt
from PIL import Image
from typing import List
import torch, numpy as np

def display_grid(images: List[Image.Image], *args,* *kwargs):
    transform = T.Compose([T.Resize(256), T.CenterCrop(256), T.ToTensor()])
    tensors = [transform(img) for img in images]
    grid = torchvision.utils.make_grid(tensors, *args,* *kwargs)
    _, sub = plt.subplots(dpi=300)
    sub.imshow(grid.permute(1, 2, 0))
    sub.axis("off"); plt.show()
2) Load DINOv2 model
from transformers import AutoImageProcessor, AutoModel

model_name = "facebook/dinov2-with-registers-base"
processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.eval()

print(f"Model loaded: {model_name}")
print(f"Embedding dimension: {model.config.hidden_size}")
3) Load images and visualize
image_list = {
    'cat': 'images/cat.jpg',
    'dog': 'images/dog.jpg', 
    'car': 'images/car.jpg',
    'truck': 'images/truck.jpg',
    'food': 'images/food.jpg'
}
images = {name: Image.open(path) for name, path in image_list.items()}
display_grid(images.values(), nrow=5)
4) Understand ViT patches and tokens
patch_size = model.config.patch_size
h, w = processor.crop_size['height'], processor.crop_size['width']
patches_per_side = h // patch_size

print(f"Patch size: {patch_size}")
print(f"Processor size: {w} x {h}")
print(f"Patch tokens per image: {patches_per_side**2}")  # ViT/14 -> 256
print(f"CLS dim: {model.embeddings.cls_token.shape[-1]}")
print(f"Register tokens (count, dim): {model.embeddings.register_tokens.shape[1:]}")
5) Extract embeddings (CLS, registers, patches)
def get_embeddings(batch: List[Image.Image]):
    inputs = processor(images=batch, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    hs = outputs[0]  # [B, 1 + R + P, D]
    n_reg = model.config.num_register_tokens
    cls = hs[:, 0, :].numpy()
    regs = hs[:, 1:1+n_reg, :].numpy()
    patches = hs[:, 1+n_reg:, :].numpy()
    return cls, regs, patches

cls_tokens, register_tokens, patch_embeddings = get_embeddings(list(images.values()))
print("CLS:", cls_tokens.shape)
print("Registers:", register_tokens.shape)
print("Patches:", patch_embeddings.shape)
Expected for base model with 5 images:

CLS: [5, 768]
Registers: [5, 4, 768]
Patches: [5, 256, 768] (for 224×224 with ViT/14)
6) Similarity between images (using CLS)
def cosine_similarity_matrix(embeddings: np.ndarray):
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    e = embeddings / norms
    return e @ e.T

sim = cosine_similarity_matrix(cls_tokens)
print(np.round(sim, 2))  # higher values = more similar
Optional: plot with matplotlib or scikit-learn’s ConfusionMatrixDisplay for a matrix view.

Optional: fine-tune a small classifier with a frozen DINOv2 backbone
Binary “dog vs not_dog” example using Oxford Pets.

from datasets import load_dataset
from transformers import AutoImageProcessor, AutoModelForImageClassification, TrainingArguments, Trainer
import evaluate

dataset = load_dataset("enterprise-explorers/oxford-pets", split="train")
def to_binary(ex): ex['labels'] = 1 if ex['dog'] else 0; return ex
dataset = dataset.map(to_binary).remove_columns(['label','dog'])
dataset = dataset.train_test_split(test_size=0.3, seed=42, stratify_by_column="labels")

labels = ["not_dog","dog"]
id2label = {i:l for i,l in enumerate(labels)}
label2id = {l:i for i,l in enumerate(labels)}

image_processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base", use_fast=True)
def preprocess(ex): ex["pixel_values"] = image_processor(ex["image"], return_tensors="pt").pixel_values; return ex
processed = dataset.map(preprocess, batched=True, remove_columns=["image"])

model = AutoModelForImageClassification.from_pretrained(
    "facebook/dinov2-base",
    num_labels=2, id2label=id2label, label2id=label2id,
    ignore_mismatched_sizes=True
)
for p in model.dinov2.parameters(): p.requires_grad = False

metric = evaluate.load("accuracy")
def compute_metrics(ev): preds = np.argmax(ev[0], axis=1); return metric.compute(predictions=preds, references=ev[1])

args = TrainingArguments(
    output_dir="./dinov2-dog-detection-finetuned",
    per_device_train_batch_size=128,
    per_device_eval_batch_size=128,
    num_train_epochs=3,
    eval_strategy="epoch"
)

trainer = Trainer(model=model, args=args,
                  train_dataset=processed["train"],
                  eval_dataset=processed["test"],
                  compute_metrics=compute_metrics)
trainer.train()
trainer.save_model("./dinov2-dog-detection-finetuned")
Takeaways
CLS embeddings from DINOv2 serve as strong global image representations.
Patch token count equals (image_size / patch_size)²; ViT/14 at 224 gives 256 patches.
Register tokens improve learning dynamics; no need at inference for most tasks.
Cosine similarity is a simple and effective way to measure image relatedness.
A frozen DINOv2 backbone enables efficient fine-tuning with limited labeled data.







In the next few minutes, we're going to learn how to load the DINOv2 model, understand its output, get class and patch embeddings, and leverage them to compare images. As we were preparing this content, Meta released a Vtri model, which is a larger version, trained on more data, and hence slightly improved. However, at the moment that requires Meta registration, so we stick with the openly available DINOv2 here. However, everything we discuss applies to DINOv3 as well. Let's jump in. First, we define a helper function that displays images in a nice grid. It'll come in handy later. Now, let's load the DINOv2. It's as simple as calling the pretrained method from auto image processor for pre-processing and auto model for the model itself. Since we're not training, we set the model to even mode. Let's check the embedding dimension. Using the smallest DINOv2 model, VIT base, the embedding size is 768. When we feed an image to the model, we get a vector with 768 numbers. For this demo, we're using sample images. Here we load and display them. We have a cat, a dog, a car, a truck, and some food. Let's dive into vision transformers. DINOv2 is a VIT-trained, self-supervised, meaning without labels. A VIT divides images into patches. The original paper, an image is worth 16-by-16 words, used 14-by-14 pixel patches on 224-by-224 images, giving 16 patches per side or 256 total patches. Here we get the patch size, image dimensions, and compute patches per side. As promised, patch size is 14, images resize to 224 by 224. We have 256 patches. Overlaying them on the cut image, every red square is a patch that becomes a transformer token and gets fed into a normal transformer, just like the ones used in natural language processing. A typical VIT adds a class token at the sequence beginning, learned during training, and then fixed during inference. Here's what DINOv2 learned. It doesn't mean much to humans but shows the class token exists and is fixed in input. It's appended at the beginning of the sequence before all 256 patch tokens. This class token gets transformed while going through the transformer heads and blocks, accumulating through self-attention with the patch tokens, more and more semantic information about the image content. At the end of the transformer, when the last class token is output by the last block, It contains the most meaningful global representation of the image. In recent years, it's been discovered that self-supervised transformers like our DINOv2 benefit from additional scratch space, additional learned tokens, just like the CLS token, where the model can store information during training. These are called register tokens. They are useful during training, but then discarded during inference. We can see that the model we're using has four of them each of length 768, just like the CLS token. Let's put this to use. Here we define a function getting embeddings from image batches. We pre-process images using our loaded processor, then pass them to the model wrapped in torch dot no grad, since we're not training. The outputs first element contains everything we need. Let's unpack it step by step. First, the class token, the outputs first token. The batch dimension is first, sequence dimension second, and embedding dimension third with size 768. Here's how we extract it. Next, register tokens. We need four in this model, extracting from the second to fifth elements. Finally, everything remaining corresponds to 256 patch tokens. We return everything. Let's verify our results. We got five class tokens of size 768, 1 per image. Got four registered tokens of size 768 for each image, and we got 256 patch embeddings of size 768 per image. Everything checks out. Before we move on, let me clarify an important point. In general, we talk about image embeddings to indicate the global representation of a piece of data. In the context of vision transformers, the image embeddings that people typically refer to are simply the class token for each image. In this context, embedding and class token are equivalent. Now with embeddings for each image, let's compute the cosine similarity matrix. Each element represents a similarity between row and column images. We skip the diagonal since every image perfectly matches itself. The matrix is symmetrical because the similarity of a to b equals obviously the similarity of B2A. Looking at the first row, the cat on the row is most similar to the dog on the column, since they're both animals in similar contexts. The car row shows highest similarity to the truck and negative similarity to animals and food because car and truck are related concepts, and so on. This clearly shows intuitively that the embeddings carry semantic meaning. Let's finish with an important note. DINOv2's typical use is as a backbone for fine-tuned models. You take our DINOv2 and attach a small piece on top using class and patch embeddings for tasks like classification, segmentation, or detection. Since DINOv2 embeddings are already meaningful, you need very little data for good performance versus training from scratch. Here's an example. Training a simple cat versus dog classifier on Oxford Pat's dataset. After loading data, processor, and model, we freeze the entire DINOv2 part and train just a small classification head on top for three epochs. Very little training accomplished in 15 minutes on my laptop. We achieve extremely good performance that would take much longer and more data starting from scratch. This means that using solutions like these in your enterprise use cases, when you need to train a model yourself can save you a lot of money and time because often data collection and training are the most expensive and time-consuming parts in producing a machine learning model. Thanks for sticking with me until now. This concludes our DINOv2 demo, see you next time.