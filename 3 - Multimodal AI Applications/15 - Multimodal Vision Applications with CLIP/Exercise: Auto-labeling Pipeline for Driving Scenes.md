In this exercise you will build an end-to-end auto-labeling pipeline for driving scenes. The workflow classifies time of day and weather using CLIP, detects vehicles and people using RT-DETR trained on COCO, and segments detections using SAM2.1. This mirrors the first pass of data curation used in self-driving development, where automated labels are later refined by human review.

Prerequisites
Workspace with Python 3.9+ (GPU recommended; CPU supported but slower)
Packages: torch (CUDA build if GPU), transformers >= 4.43, pillow, matplotlib, numpy
Models from the Hugging Face Hub (cached in Udacity workspace):
openai/clip-vit-base-patch32
PekingU/rtdetr_r50vd_coco_o365 (COCO-trained)
facebook/sam2.1-hiera-base-plus
Approximately 6–8 GB GPU VRAM for SAM2.1 base-plus; close other GPU jobs if limited
Objectives
By the end of this exercise, you will be able to:

Implement missing parts of a multi-model computer vision pipeline (classification, detection, segmentation)
Run auto-labeling on single and multiple driving images and visualize results
Tune thresholds and handle simple post-processing (dashboard removal via IoU)
Steps
Access the notebook in the classroom workspace

To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l2/exercises/4-grand-finale/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Validate data availability

Confirm that ../images/ contains PNG files (one.png, two.png, three.png, four.png).
If paths differ in the workspace, update the image paths in the notebook accordingly.
Review helper functions

Examine get_distinct_colors, visualize_detr_detections, and visualize_pipeline_results to understand expected inputs and outputs (boxes in xyxy format; masks as boolean arrays).
Load models

Run the “Load Models” cell to initialize:
CLIP (openai/clip-vit-base-patch32) for time-of-day and weather classification
RT-DETR (PekingU/rtdetr_r50vd_coco_o365) for detection (person, car, bus, truck)
SAM2.1 (facebook/sam2.1-hiera-base-plus) for segmentation
Confirm the device selection line sets device = "cuda" when available.
Complete classification (CLIP)

In classify_driving_conditions, fill the TODOs:
Prepare inputs for time-of-day:
time_inputs = clip_processor(text=TIME_OF_DAY_LABELS, images=image, return_tensors="pt", padding=True)
Run model:
time_outputs = clip_model(**time_inputs)
Probabilities are computed with softmax; no change needed.
Weather classification is already implemented in the template; verify symmetry with the time-of-day section.
Complete detection (RT-DETR)

In detect_vehicles_and_people, fill the TODOs:
Preprocess image:
inputs = detr_processor(images=image, return_tensors="pt")
Run model:
outputs = detr_model(**inputs)
Post-processing:
Keep labels for person=0, car=2, bus=5, truck=7.
Dashboard removal uses IoU of each box with the full image; keep boxes with IoU < 0.8 (configurable).
Complete segmentation (SAM2.1)

In segment_vehicles_and_people, fill the TODOs:
Prepare SAM inputs using detection boxes as prompts:
inputs = sam_processor(images=image, input_boxes=[boxes], return_tensors="pt").to(device)
Run model:
outputs = sam_model(**inputs)
Post-processing:
Use sam_processor.post_process_masks and iou_scores to select the best mask per box.
Notes:
Boxes must be in xyxy pixel coordinates aligned with the original image (RT-DETR output is suitable).
If no boxes are present, return an empty list.
Run the complete pipeline on a single image

Load one image:
image = Image.open("../images/one.png").convert("RGB")
Execute:
results = auto_label_driving_scene([image])
result = results[0]
Review printed summary: time of day, weather, number of detections, and mask count.
Visualize results

Call visualize_pipeline_results(image, result['time_of_day'], result['time_confidence'], result['weather'], result['weather_confidence'], result['masks'])
Inspect overlays: classification text, and colored masks over the scene.
Batch process multiple images

Use the provided glob-based loop to process all PNGs in ../images/.
Visualize each set of results to compare conditions across different scenes (e.g., day vs night, rain vs normal).
Tune thresholds and validate

Adjust detection_threshold in auto_label_driving_scene (e.g., 0.2–0.5).
Modify iou_threshold_for_dashboard_removal if false positives near the windshield appear.
Rerun and compare detection counts and mask quality.
