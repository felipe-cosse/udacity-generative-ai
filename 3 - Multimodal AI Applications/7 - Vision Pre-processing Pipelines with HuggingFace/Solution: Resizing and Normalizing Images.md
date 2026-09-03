This walkthrough demonstrates how to:

Load a Hugging Face dataset in streaming mode
Convert images to RGB and resize them consistently
Visualize processed images in a grid
Apply a model-specific preprocessor (AutoImageProcessor) that handles resizing, normalization, and tensor formatting
The main premise: ensure images are in the correct format and size for downstream models, either by writing simple preprocessing steps or by using a model’s predefined processor.

Two complementary approaches are shown:

Manual preprocessing with PIL:
Convert to RGB to avoid channel mismatches
Resize images to a fixed size using .thumbnail or .resize
Add the processed images back into the dataset and visualize them
Model-specific preprocessing:
Use AutoImageProcessor.from_pretrained("google/siglip-base-patch16-224")
Convert images to RGB, then call the processor with return_tensors="pt"
The processor standardizes pixel values (float tensors), ready for model input
To use the Udacity workspace:

At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l2/exercises/1-vision-processing/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Step-by-Step Instructions
1) Load the dataset
The data is downloaded in the Udacity workspace, but streaming can avoid downloading everything at once and works well for large datasets.
from datasets import load_dataset

ds = load_dataset("osunlp/MagicBrush", split="dev")
2) Define a manual preprocessing function (PIL)
Convert images to RGB.
Resize to 256×256. Two options:
.thumbnail((256, 256)): preserves aspect ratio, operates in-place, may not hit exact 256×256 if aspect ratio differs.
.resize((256, 256)): forces exact size, may distort.
def preprocess_function(examples):
    images = []
    for image in examples['source_img']:
        image = image.convert("RGB")
        # image = image.resize((256, 256))  # exact size, possible distortion
        image.thumbnail((256, 256))         # in-place, preserves aspect ratio
        images.append(image)
    examples["preprocessed_image"] = images
    return examples
Caution:

.thumbnail returns None and modifies the image in-place.
If the exact size is required, use .resize((256, 256)).
3) Apply preprocessing and take a small sample
Use batched=True for efficiency.
Materialize a small subset with .take(9) for quick checks.
ds_custom = ds.map(preprocess_function, batched=True, batch_size=9).take(9)
4) Visualize with torchvision and matplotlib
Convert PIL images to tensors for a grid view.
from torchvision.utils import make_grid
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt

grid = make_grid([ToTensor()(img) for img in ds_custom['preprocessed_image']], nrow=3)
fig, sub = plt.subplots(dpi=300)
sub.imshow(grid.permute(1, 2, 0))
sub.axis('off')
5) Initialize a model-specific preprocessor
AutoImageProcessor (image-only) or AutoProcessor (often for multimodal). Interface is the same for these steps.
from transformers import AutoImageProcessor

processor = AutoImageProcessor.from_pretrained("google/siglip-base-patch16-224")
print(processor)  # inspect resizing, normalization, and expected inputs
6) Preprocess with the model’s processor
Convert to RGB first to avoid channel issues.
Set return_tensors="pt" to get PyTorch tensors.
def preprocess_function(examples):
    images = [image.convert("RGB") for image in examples["source_img"]]
    inputs = processor(images, return_tensors="pt")
    examples["pixel_values"] = inputs["pixel_values"]
    return examples
ds_processed = ds.map(preprocess_function, batched=True, batch_size=9).take(9)
7) Visualize standardized tensors
Standardized tensors contain float values. Normalize to [0, 1] for display only.
grid = make_grid([img for img in ds_processed['pixel_values']], nrow=3)

grid -= grid.min()
grid /= grid.max()

fig, sub = plt.subplots(dpi=300)
sub.imshow(grid.permute(1, 2, 0))
sub.axis('off')
Important:

Do not normalize the tensors used for modeling. The processor already applied the correct transformations.
Remember: Use a model’s AutoImageProcessor to guarantee correct resizing and normalization; reserve manual resizing for quick checks or custom pipelines.






Look together at the solution for this exercise. In the first cell, you had to load the dev split of the specified dataset in streaming mode. This is done by importing the load dataset function, and then providing the name of the dataset, the split, and the keyword streaming equal to true. Next, you had to complete a custom pre processing function that includes some image manipulations. In particular, you had to convert to RGB and resize. Here, we need to call.convert to convert to RGB. Then I chose to use the thumbnail method instead of the resize method. The difference is that thumbnail does not introduce distortion, but crops, if necessary. While resize does not crop and distorts the image into the requested shape. Since thumbnail modifies the picture in place, we need to use it separately and without reassigning the return value. If instead we had chosen to use dot resize, we would have done it like this. The code then applies the function we just completed to the whole dataset by using the.map method, and then we take nine images from there. Note that because we loaded the data set in streaming mode, the images haven't been downloaded yet. They will be downloaded lazily, and the pre processing applied when we try to use them, which will happen in the next cell when we try to visualize them. Looking at these images, you can see that pairs that look very similar to each other actually have subtle differences. For example, in the images of the zebras, the animals don't change, but the background does. Next, you had to load a predefined processor instead of defining your own. This is done by using the from pre-train method of the appropriate processor class, which in this case, is auto image processor. Once we have the instance, we can simply print it to see what transformations it applies. For example, here, we see that we're normalizing rescaling, and resizing with the parameters reported there. Once you had your processor, you had to complete this helper function in order to apply it to the entire dataset. First, you needed to convert to RGB. This is often redundant, but some images do come in other formats, and failing to do this step might result in weird artifacts or silent failures down the line. Then you had to apply the processor, which is simply done by calling it on the batch and remembering to add return tensors equals PT to get PyTorch tensors in return. As we've done before, we call.map and then take to apply the processing and then take nine images. Just like before, these operations are evaluated lazily, and so they are actually triggered in the next cell when we plot the results. This concludes the presentation of the solution to this exercise. See you next time.