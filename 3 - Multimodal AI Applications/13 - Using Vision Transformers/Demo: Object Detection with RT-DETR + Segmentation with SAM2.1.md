This demo shows a practical two-stage computer vision pipeline:

Stage 1: Detect objects with RT-DETR (real-time transformer-based detector).
Stage 2: Segment each detected object with SAM 2.1 using the detected boxes.
This pattern is common in:

Robotics and autonomous systems
Retail analytics and inventory tracking
Medical and industrial inspection
Photo editing and content creation
You will see how to load pretrained models, run inference on a sample image, convert detections to segmentation masks, and visualize the results.

Workflow Summary
Define simple visualization helpers.
Load RT-DETR and a sample image from COCO.
Run detection and extract boxes, labels, and scores.
Pass the boxes to SAM2.1 and select the best mask per box using IoU scores.
Overlay masks on the image for easy interpretation.
Step-by-Step Instructions
1) Setup and helper functions
Install and import the required libraries: transformers, datasets, torch, PIL, matplotlib, numpy.

# Object Detection with RT-DETR + Segmentation with SAM2.1

# This notebook demonstrates:
# 1. Object detection using RT-DETR
# 2. Object segmentation using SAM2.1 starting from the boxes found by RT-DETR

import torch
from typing import List
import matplotlib.pyplot as plt
from PIL import ImageDraw, Image
import numpy as np
Helper functions for colors and detection visualization:

def get_distinct_colors(n_colors):
    if n_colors <= 10:
        cmap = plt.cm.tab10
    elif n_colors <= 20:
        cmap = plt.cm.tab20
    else:
        cmap = plt.cm.tab20
        # Cycle through colors if more than 20
    colors = [cmap(i % cmap.N) for i in range(n_colors)]
    return colors

def visualize_detr_detections(
    image: Image.Image,
    boxes: torch.Tensor,
    scores: torch.Tensor,
    labels: torch.Tensor,
    class_labels: List[str],
):
    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image, mode='RGBA')
    for box, score, label in zip(boxes, scores, labels):
        x1, y1, x2, y2 = box.tolist()
        label_id = int(label.item())
        draw.rectangle([x1, y1, x2, y2], outline="red", width=1)
        class_name = class_labels[label_id]
        text = f"{class_name}: {score:.2f}"
        draw.text((x1, y1 - 20), text, fill="red")
    fig, sub = plt.subplots(figsize=(12, 8))
    sub.imshow(draw_image)
    sub.set_title("RT-DETR Detections")
    sub.axis("off")
    plt.show(fig)
2) Load RT-DETR
Load the processor and model from the Hub.

from transformers import RTDetrImageProcessor, RTDetrV2ForObjectDetection

detr_processor = RTDetrImageProcessor.from_pretrained("PekingU/rtdetr_v2_r50vd")
detr_model = RTDetrV2ForObjectDetection.from_pretrained("PekingU/rtdetr_v2_r50vd")
3) Load a sample image (COCO)
Stream one validation image for a quick test and view it.

from datasets import load_dataset

dataset = load_dataset("detection-datasets/coco", split="val", streaming=True)
sample = next(iter(dataset))
image = sample["image"]

plt.figure(figsize=(10, 6))
plt.imshow(image)
plt.title("Original Image")
plt.axis("off")
plt.show()
4) Step 1: Object detection with RT-DETR
Preprocess, run inference, and post-process detections.

# Preprocess
inputs = detr_processor(images=image, return_tensors="pt")

# Inference
with torch.no_grad():
    outputs = detr_model(**inputs)

# Post-process to get boxes, scores, labels
results = detr_processor.post_process_object_detection(
    outputs, target_sizes=torch.tensor([image.size[::-1]]), threshold=0.5
)
boxes = results[0]["boxes"]
scores = results[0]["scores"]
labels = results[0]["labels"]

print(f"Detected {len(boxes)} objects")
visualize_detr_detections(
    image, boxes, scores, labels,
    dataset.info.features['objects']['category'].feature.names
)
5) Step 2: Segmentation with SAM2.1 (box prompts)
Feed the detected boxes to SAM2.1 and select the best mask for each box.

from transformers import Sam2Processor, Sam2Model

device = "cuda" if torch.cuda.is_available() else "cpu"
model = Sam2Model.from_pretrained("facebook/sam2.1-hiera-base-plus").to(device)
processor = Sam2Processor.from_pretrained("facebook/sam2.1-hiera-base-plus")

inputs = processor(
    images=image,
    input_boxes=[boxes],
    return_tensors="pt",
).to(device)

with torch.no_grad():
    outputs = model(**inputs)

masks = processor.post_process_masks(
    outputs.pred_masks.cpu(), inputs["original_sizes"]
)[0]

iou_scores = outputs.iou_scores.cpu()

best_masks = []
for i in range(masks.shape[0]):  # one set per box
    best_mask_idx = torch.argmax(iou_scores[0, i])
    best_masks.append(masks[i, best_mask_idx])
best_masks = torch.stack(best_masks)  # [n_objects, H, W]
print(f"Best masks shape: {best_masks.shape}")
6) Step 3: Visualize combined results
Overlay per-object colored masks over the image.

fig, sub = plt.subplots(1, 1, figsize=(18, 6))
sub.imshow(image.convert("L").convert("RGB"), alpha=0.5)

colors = get_distinct_colors(len(best_masks))
for i, mask in enumerate(best_masks):
    colored_mask = np.zeros((*mask.shape, 4))
    color_rgb = colors[i][:3]
    colored_mask[mask > 0, :3] = color_rgb
    colored_mask[mask > 0, 3] = 0.5
    sub.imshow(colored_mask)

sub.set_title("SAM2.1 Segmentations")
sub.axis("off")
plt.tight_layout()
plt.show()
Takeaways
RT-DETR provides fast and accurate object boxes suitable for real-time use.
SAM 2.1 can segment objects precisely using box prompts, producing high-quality masks.
Combining detection and segmentation forms a flexible pipeline useful for many applications.
Visualization with overlays helps verify detection quality and mask accuracy.
The workflow generalizes to custom images and datasets with minimal changes.







In the next few minutes, we're going to learn how to perform object detection and segmentation on images using two of the latest machine learning models for these tasks. Let's get started. We start by defining some helper functions for visualizations. We'll use them later. We then load our first model, which is called real time detection transformer, RT-DETR. This is a state of the art, real time object detection model, capable of detecting objects and multiple frames per second, and therefore, useful for real time applications like surveillance, monitoring, and counting. Let's get a sample image so I can show you how to use this model. We simply get the first image of the COCO data set. There are many objects and two people in this image. Now that we have the model, the pre processor, and the data, let's run the detection. As usual with computer vision models, we first run the processor, which transforms the image in the shape, normalization, and format expected by the model. We then run through the model, making sure to use torch.no_grad because we don't want to slow down inference by computing gradients unnecessarily. In the case of object detection, the processor is also used to take the raw results from the model and process them for further use. The post processor formats the boxes and filters them according to a confidence threshold. Note that the DETR family of models does not perform non maximum suppression, which is typically used by other object detection algorithms. We can now visualize our results. The model has detected 21 objects in our image, represented by the red boxes here. Now that we've seen how to perform object detection with RT-DETR, let's move to the segmentation part. We're going to take the objects detected in the first part and get their segmentation mask from SAM2.1. Let's start by loading the model and its processor using the from_pretrained method. We can then immediately preprocess the image. Note that here in the processor, we're passing in the boxes obtained with RT-DETR before. These are used as prompts for SAM2.1. SAM2.1 can also accept other types of prompts, such as points or even text. In this case, however, we're going to use the boxes found in the object detection stage. Once we have pre processed the inputs, we can pass them into the model. We then feed the output of the model in the post process masks method of the processor to get our final results. SAM 2.1 returns different candidate masks for every object with associated scores. SAM generates multiple mask predictions for each object because segmentation can be ambiguous. Should you segment just the person's head or their whole body or include their clothing? In our case, since we are prompting it with the boxes from the previous object detection stage, we can just select the mask with the highest score. We can finally display the results. Here, I grade out the image bit to highlight the segmentation masks found by SAM of all the objects found by RT-DETR. We can see that the objects are segmented very well, including tricky objects such as the chairs at the table, which present occlusions and other challenges. Before we finish, let me note that there are models that provide object detection and segmentation together within the same inference step. Depending on the application, using one of those could make more sense than doing it separately as we did here. In terms of accuracy, however, the pair presented today is very strong. This concludes our demo for today, thanks for watching.