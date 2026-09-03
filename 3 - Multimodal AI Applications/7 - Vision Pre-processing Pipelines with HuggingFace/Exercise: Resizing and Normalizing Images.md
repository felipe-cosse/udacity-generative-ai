In this hands-on exercise, you will apply practical image preprocessing used in computer vision workflows:

Load the public osunlp/MagicBrush dataset (dev split) in streaming mode.
Convert images to RGB and resize to 256×256 using Pillow.
Visualize results with torchvision.
Initialize a Transformers preprocessor for google/siglip-base-patch16-224 to standardize resizing and normalization.
Compare manual preprocessing with model-defined preprocessing for model readiness.
Why this matters: consistent resizing and normalization are standard steps in industry pipelines to ensure inputs match model expectations and to achieve reproducible results.

Prerequisites:
Classroom workspace (VS Code) with internet access
Packages: datasets, pillow, numpy, torch, torchvision, transformers, matplotlib
If needed: pip install -U datasets pillow numpy torch torchvision transformers matplotlib
No Hugging Face token required for the public dataset (streaming mode reduces local storage needs)
GPU optional (CPU is sufficient)
Objectives:
By the end of this exercise, be able to:

Load a streaming dataset split using Hugging Face Datasets
Implement manual RGB conversion and resizing with Pillow
Use a model’s AutoImageProcessor to normalize images and output PyTorch tensors
Visualize image grids and safely normalize for plotting
Steps:
Configure the workspace

To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l2/exercises/1-vision-processing/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Load the dataset

Complete the TODO in load_dataset:
name: "osunlp/MagicBrush"
split: "dev"
stream: True
Implement manual preprocessing with Pillow
In preprocess_function, iterate over examples["source_img"].
Convert each image to RGB: image.convert("RGB").
Resize to 256×256 using one of the two strategies:
Aspect-ratio preserving (safer geometry, in-place):
img = image.convert("RGB")
img = img.copy() (avoid mutating the original object)
img.thumbnail((256, 256)) (fits within 256×256, may not be exact size)
image = img
Forced size (exact 256×256, may distort):
image = image.convert("RGB").resize((256, 256))
Append to images and set examples["preprocessed_image"] = images.
Notes:
.thumbnail mutates in place and returns None. Always work on a copy or a temporary variable.
If exact 256×256 with preserved aspect ratio is required, consider ImageOps.fit (not required here).
Apply the manual preprocessing and visualize
Map in batches: ds_custom = ds.map(preprocess_function, batched=True, batch_size=9).take(9)
Build a grid of the preprocessed PIL images: - grid = make_grid([ToTensor()(img) for img in ds_custom["preprocessed_image"]], nrow=3) - Plot: sub.imshow(grid.permute(1, 2, 0)); sub.axis('off')
Interpretation:
ToTensor() converts PIL images to float tensors in [0, 1].
The grid shows resized outputs from the manual pipeline.
Initialize a model-defined preprocessor
Use AutoImageProcessor for Google’s SigLIP base model: - processor = AutoImageProcessor.from_pretrained("google/siglip-base-patch16-224")
Inspect transforms to understand resizing, cropping, and normalization:
print(processor)
Implement preprocessing with AutoImageProcessor
In the new preprocess_function, prepare RGB images: - images = [image.convert("RGB") for image in examples["source_img"]]
Apply the processor to return PyTorch tensors:
inputs = processor(images=images, return_tensors="pt")
Store the output:
examples["pixel_values"] = inputs["pixel_values"]
Notes:
The processor handles resizing to the model’s expected input (e.g., 224×224), center crops if needed, and normalizes channels using model-specific mean/std.
Apply the processor and visualize normalized tensors
Map and take a small sample: - ds_processed = ds.map(preprocess_function, batched=True, batch_size=9).take(9)
Create a grid from pixel_values (already tensors):
grid = make_grid([img for img in ds_processed["pixel_values"]], nrow=3)
Normalize only for plotting:
grid -= grid.min(); grid /= grid.max()
Plot:
sub.imshow(grid.permute(1, 2, 0)); sub.axis('off')
Important:
This min–max scaling is solely for visualization. Do not apply it before feeding tensors to downstream models.
Optional extension: test on a local image
Load: from PIL import Image; img = Image.open("path/to/image.jpg").convert("RGB")
Apply manual resizing or processor(images=[img], return_tensors="pt").
Visualize or check tensor shape and dtype to confirm correctness.
