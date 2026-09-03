This demo shows how to:

Load and sample computer vision datasets with Hugging Face Datasets
Inspect images, labels, and dataset features
Preprocess images using AutoImageProcessor and custom Pillow operations
Understand pixels, channels, color spaces, and memory trade-offs
Compare image compression formats (PNG vs. JPEG) and visualize differences
Run quick image classification with a Transformers pipeline
Real-world use: fast experimentation for an image classifier (e.g., Food-101) covering data access, preprocessing, and inference, with visual diagnostics to guide choices before training or deployment.

To use the Udacity workspace:

At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l2/demos/1-vision-processing/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Summary of the demo workflow
Load Food-101 with different strategies (full split, subset, streaming).
Explore items, labels, and visualization with matplotlib.
Apply preprocessing with AutoImageProcessor and map over the dataset.
Build a custom preprocessing function using Pillow (rotate, blur, thumbnail).
Inspect pixels and channels; convert to grayscale; compare memory and histograms.
Convert and visualize color spaces (RGB, HSV, LAB, YUV).
Save and compare image formats (PNG, JPEG quality 95 and 30), visualize differences.
Run a Transformers image-classification pipeline on sample images.
Code used in the demo
Load datasets
from datasets import load_dataset

# Entire dataset by name
dataset = load_dataset("food101")

# Streaming mode (on-demand, slower I/O tradeoff)
dataset_stream = load_dataset("food101", streaming=True)

# Load only a split
val = load_dataset("food101", split="validation")

# Subset of a split (first 5)
val5 = load_dataset("food101", split="validation[:5]")

# Shuffle and select 5 samples deterministically
val5_shuffled = (
    load_dataset("food101", split="validation")
    .shuffle(seed=42)
    .select(range(5))
)
Inspect images and labels
import numpy as np
import matplotlib.pyplot as plt

# Single image as PIL
img0 = val5_shuffled['image'][0]

# Iterate and inspect shapes
for image in val5_shuffled['image']:
    arr = np.array(image)
    print("Image shape:", arr.shape)

# Visualize with labels
fig, sub = plt.subplots(1, 5, dpi=75)
for i, row in enumerate(val5_shuffled):
    img = row['image']
    label_idx = row['label']
    label = val5_shuffled.features['label'].int2str(label_idx)
    sub[i].imshow(img)
    sub[i].set_title(label, fontsize=6)
    sub[i].axis("off")
plt.tight_layout()
plt.show()
Preprocess with AutoImageProcessor
from transformers import AutoImageProcessor

processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")

def preprocess_function(examples):
    images = [image.convert("RGB") for image in examples["image"]]
    inputs = processor(images, return_tensors="pt")
    examples["pixel_values"] = inputs["pixel_values"]
    return examples

ds = val5_shuffled.map(preprocess_function, batched=True)

# Confirm tensor shape
import numpy as np
np.array(ds['pixel_values'][0]).shape  # e.g., (3, 224, 224)
Custom preprocessing with Pillow
from PIL import ImageFilter

def custom_preprocess(examples):
    processed = []
    for image in examples['image']:
        image = (
            image.convert("RGB")
                 .rotate(10)
                 .filter(ImageFilter.GaussianBlur(5))
        )
        # Note: some Pillow methods act in-place and return None
        image.thumbnail((224, 224))
        processed.append(image)
    examples["preprocessed_images"] = processed
    return examples

ds_custom = val5_shuffled.map(custom_preprocess, batched=True)
sample_aug = ds_custom['preprocessed_images'][0]
Pixels and channels
import cv2

sample_image = val5_shuffled[0]['image']        # PIL
sample_array = np.array(sample_image)           # H x W x 3
class_label = val5_shuffled[0]['label']
class_name = val5_shuffled.features['label'].int2str(class_label)

# Grayscale conversion and memory comparison
grayscale = cv2.cvtColor(sample_array, cv2.COLOR_RGB2GRAY)
print("RGB memory:", sample_array.nbytes, "bytes")
print("Grayscale memory:", grayscale.nbytes, "bytes")

# Visualization helper (provided)
plot_pixels_and_channels(sample_array, grayscale, f"{class_label} ({class_name})")
Color spaces
rgb_image = sample_array
hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
lab_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2LAB)
yuv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2YUV)

assert hsv_image.shape == lab_image.shape == yuv_image.shape == rgb_image.shape
plot_color_spaces(rgb_image, hsv_image, lab_image, yuv_image)
Image formats and compression
from PIL import Image
import io

test_image = np.array(val5_shuffled['image'][1])[:328, :328, ...]

def get_image_size_and_quality(image_array, format_type, quality=None):
    pil_image = Image.fromarray(image_array)
    buffer = io.BytesIO()
    if format_type == 'PNG':
        pil_image.save(buffer, format='PNG')
    elif format_type == 'JPEG':
        pil_image.save(buffer, format='JPEG', quality=quality)
    size = buffer.tell()
    buffer.seek(0)
    reconstructed = np.array(Image.open(buffer).convert('RGB'))
    return size, reconstructed

original_size = test_image.nbytes
png_size, png_reconstructed = get_image_size_and_quality(test_image, 'PNG')
jpeg_high_size, jpeg_high_reconstructed = get_image_size_and_quality(test_image, 'JPEG', quality=95)
jpeg_low_size, jpeg_low_reconstructed = get_image_size_and_quality(test_image, 'JPEG', quality=30)

sizes = [original_size, png_size, jpeg_high_size, jpeg_low_size]
plot_compression_comparison(test_image, png_reconstructed, jpeg_high_reconstructed, jpeg_low_reconstructed, sizes)
Quick inference with a Transformers pipeline
from transformers import pipeline

clf = pipeline("image-classification", model="google/vit-base-patch16-224")
preds = clf(val5_shuffled[0]['image'])
preds[:3]
Takeaways
Hugging Face Datasets provides flexible loading (full, split, subset, streaming) and easy iteration.
AutoImageProcessor ensures model-aligned transforms (resize, normalization) and integrates cleanly with map.
Custom Pillow transforms enable augmentation and image cleanup; watch for in-place operations.
Grayscale reduces memory but loses color information; distributions clarify pixel intensity behavior.
HSV/LAB/YUV separate luminance and chrominance in useful ways for preprocessing and robustness.
Compression choices impact size and visual fidelity; artifacts become visible at low JPEG quality.
Transformers pipelines enable fast inference to validate preprocessing choices before training.






Come to this quick introduction to computer vision fundamentals. We look at how computers see images, different color spaces, and how to work with data sets. Let's jump into it. After a few imports, we define some helper functions for plotting purposes. Now, let's get into the interesting part. First, we need some images to play with. A powerful library we can leverage is the data sets library from Hugging Face. It gives you access to all data sets on the hub, that's 0.5 million data sets as of today. Here we load the food 101 data set. We start by importing the load data set function, and then we simply call it with the name of the data set. For large data sets or when we only want a small sample, we can use the streaming parameter. Instead of downloading everything at once, the library will download things the first time you try to access them. Can also load only a split of the data set or even a subset of a split. We can do more advanced things like taking a precise split, shuffling its order, and selecting the first five elements. Once we have a data set instance, we can operate on it easily. A data set has columns, in this case, an image column. We can take the first image like this. We can also iterate over the images. Images are instances of pillow images and can be easily converted to NumPy arrays. The width and height vary, but they all have three channels, corresponding to the RGB channels. Many data sets on the hub are labeled data sets. They contain not only images, but also ground root labels. We can display images and their labels together. It's typical that we need to apply pre processing before feeding an image to an AI model. Let's look at how that's done. Many models on Hugging Face provide not only the model, but also the pre processor. Here we're loading the pre processor for this vision transformer model. We can then apply that processor on the entire data set. We define the pre process function, which takes in a batch of examples. We first make sure they are in RGB format, which is always a good idea to avoid surprises. We then apply the processor, making sure we instruct it to return PyTorch tensors. Using the.map method of the data set, we can apply this function to the entire data set and pre compute the transformations. For streaming data sets, this function will be loaded lazily and only executed when we try to access a specific image. Given a processor, we can look at what it does. In this case, we see that we are normalizing, rescaling, and resizing. Images are resized to 224 by 224 pixels. We can also define our own pre processing function. Here I'm defining a function that converts images to RGB, rotates them by 10 degrees, smooths them with a Gaussian blur filter, and resizes them to 224 by 224. We can apply this custom function in the same way we applied the predefined processor. Now, let's look deeper at pixels and channels. An image is represented as a tensor with three dimensions, height, width, and channels. Typically, they are in RGB format, red, green, and blue channels. Each channel is just a matrix of values one per pixel between zero and 255. This image has 504 by 512 by 3 pixels, around 774,000 values. For gray scale images, we only have around 260 values with the memory reduction of 67%. So in the rare case where an algorithm can work with gray scale images, you should exploit that. Images can be represented in different color spaces, not just RGB. Thanks to Open CV, we can easily convert between different color spaces. Some computer vision algorithms work better in specific color representations. HSV separates hue, saturation, and value, making it easier to isolate colors regardless of lighting. LAB is designed to match human perception, while YUV separates luminance from color information. The choice of color space can make or break certain computer vision tasks. While most algorithms run on RGB images, some object detection tasks might work better in HSV. While compression algorithms often leverage YUV's separation of brightness and color. Moving to compression, we need to understand how different image formats affect our data. Lossless algorithms, like PNG can compress and then restore the image exactly. Loss algorithms like JPEG instead can dramatically reduce file sizes by discarding redundant or unimportant information, but introduce artifacts in return. The quality setting controls the trade off between the severity of the artifacts and the file size. These compression differences matter for machine learning. For example, if a model was trained exclusively on uncompressed images, and then it is used on images with say JPEG artifacts, it could behave differently than expected. Understanding these aspects helps you make informed decisions about data quality versus storage constraints. Thanks for staying with me up to now. This concludes this quick introduction on some fundamental aspects of computer vision. See you next time.