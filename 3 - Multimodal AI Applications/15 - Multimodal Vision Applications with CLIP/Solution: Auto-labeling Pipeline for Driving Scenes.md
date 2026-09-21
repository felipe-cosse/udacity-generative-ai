This walkthrough builds a practical auto-labeling pipeline for driving scenes, combining classification, object detection, and segmentation. The exercise demonstrates how to bootstrap dataset curation for self-driving applications by generating labels automatically, ready for later human review.

What this achieves:

Classifies each image by time of day and weather conditions.
Detects vehicles and people.
Segments each detected instance for precise masks.
Produces structured outputs and simple visualizations for quick inspection.

The pipeline stitches together three model families:

CLIP for zero-shot classification of scene attributes (time of day and weather) using text prompts.
RT-DETR for fast object detection of persons and vehicles (person, car, bus, truck).
SAM 2.1 for segmentation using detected boxes as prompts.
Flow Overview
Preprocess and load models and labels.
Classify the scene using CLIP with prompt lists: TIME_OF_DAY_LABELS and WEATHER_LABELS.
Detect relevant objects with RT-DETR, then filter and clean detections (remove dashboard-like large boxes via IoU).
Segment each detection using SAM 2.1, selecting the best mask per box by IoU score.
Aggregate results per image into a dictionary and visualize.
Step-by-Step Instructions
Setup and Helper
To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l2/exercises/4-grand-finale/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Import libraries and define visualization utilities:
import torch, numpy as np, matplotlib.pyplot as plt
from PIL import Image, ImageDraw
Use get_distinct_colors, visualize_detr_detections, and visualize_pipeline_results for overlays and summaries.
Load models and label prompts
from transformers import CLIPProcessor, CLIPModel
from transformers import RTDetrForObjectDetection, RTDetrImageProcessor
from transformers import Sam2Processor, Sam2Model

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

detr_processor = RTDetrImageProcessor.from_pretrained("PekingU/rtdetr_r50vd_coco_o365")
detr_model = RTDetrForObjectDetection.from_pretrained("PekingU/rtdetr_r50vd_coco_o365")

device = "cuda" if torch.cuda.is_available() else "cpu"
sam_model = Sam2Model.from_pretrained("facebook/sam2.1-hiera-base-plus").to(device)
sam_processor = Sam2Processor.from_pretrained("facebook/sam2.1-hiera-base-plus")

TIME_OF_DAY_LABELS = ["sunset or sunrise", "day", "night"]
WEATHER_LABELS    = ["normal", "rain", "fog", "clouds", "snow"]
Classify driving conditions with CLIP
Encode both text prompts and the image jointly, then read logits_per_image and softmax:
def classify_driving_conditions(image):
    time_inputs = clip_processor(text=TIME_OF_DAY_LABELS, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        time_probs = torch.softmax(clip_model(**time_inputs).logits_per_image[0], dim=-1)
    time_pred = TIME_OF_DAY_LABELS[int(torch.argmax(time_probs))]
    time_conf = float(torch.max(time_probs))

    weather_inputs = clip_processor(text=WEATHER_LABELS, images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        weather_probs = torch.softmax(clip_model(**weather_inputs).logits_per_image[0], dim=-1)
    weather_pred = WEATHER_LABELS[int(torch.argmax(weather_probs))]
    weather_conf = float(torch.max(weather_probs))

    return dict(time_of_day=time_pred, time_confidence=time_conf, weather=weather_pred, weather_confidence=weather_conf)
Tuning idea: adjust prompt phrasing for clearer separation (e.g., “bright daytime” vs “night streetlights”).
Detect vehicles and people with RT-DETR
Preprocess, infer, post-process, then filter to relevant COCO classes and remove oversized boxes (dashboard-like) via IoU:
def detect_vehicles_and_people(image, threshold=0.3, iou_threshold_for_dashboard_removal=0.8):
    inputs = detr_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = detr_model(**inputs)

    results = detr_processor.post_process_object_detection(outputs, target_sizes=torch.tensor([image.size[::-1]]), threshold=threshold)
    boxes, scores, labels = results[0]["boxes"], results[0]["scores"], results[0]["labels"]

    vehicle_classes = torch.tensor([0, 2, 5, 7])  # person, car, bus, truck
    mask = torch.isin(labels, vehicle_classes)
    boxes, scores, labels = boxes[mask], scores[mask], labels[mask]

    if len(boxes) > 0:
        img_w, img_h = image.size
        ious = ((boxes[:,2]-boxes[:,0])*(boxes[:,3]-boxes[:,1])) / float(img_w*img_h)
        keep = ious < iou_threshold_for_dashboard_removal
        boxes, scores, labels = boxes[keep], scores[keep], labels[keep]

    return boxes, scores, labels
Tuning ideas: raise threshold in cluttered scenes; adjust the IoU removal threshold for different camera placements.
Segment instances with SAM 2.1
Use detection boxes as prompts and choose the best mask per box using iou_scores:
def segment_vehicles_and_people(image, boxes):
    if len(boxes) == 0:
        return []
    inputs = sam_processor(images=image, input_boxes=[boxes], return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = sam_model(**inputs)
    masks = sam_processor.post_process_masks(outputs.pred_masks.cpu(), inputs["original_sizes"])[0]
    iou_scores = outputs.iou_scores.cpu()

    best_masks = []
    for i in range(masks.shape[0]):
        best_masks.append(masks[i, int(torch.argmax(iou_scores[0, i]))])
    return best_masks
Orchestrate the full pipeline and run
def auto_label_driving_scene(images, detection_threshold=0.3):
    if isinstance(images, Image.Image):
        images = [images]
    results = []
    for idx, img in enumerate(images):
        conditions = classify_driving_conditions(img)
        boxes, scores, labels = detect_vehicles_and_people(img, detection_threshold)
        masks = segment_vehicles_and_people(img, boxes)
        results.append(dict(
            image_idx=idx,
            time_of_day=conditions["time_of_day"],
            time_confidence=conditions["time_confidence"],
            weather=conditions["weather"],
            weather_confidence=conditions["weather_confidence"],
            num_vehicles_and_people=len(boxes),
            boxes=boxes, scores=scores, labels=labels, masks=masks
        ))
    return results
Usage:
image = Image.open("../images/one.png").convert("RGB")
result = auto_label_driving_scene([image])[0]
visualize_pipeline_results(image, result['time_of_day'], result['time_confidence'], result['weather'], result['weather_confidence'], result['masks'])
Remember: Combine complementary models (classification, detection, segmentation) to build a practical auto-labeling system that accelerates dataset creation for driving scenes.






Let's look together at the solution to this exercise. It brings together classification, object detection, and segmentation in one single pipeline for auto labeling of data for self driving cars. Self driving cars need accurate segmentation of the objects surrounding them. Such segmentation is used by path planning as well as behavior prediction, and it's a key sub-system in the self driving car system. Realistic scenario, an auto labeling pipeline like this is often followed by manual screening for additional QA. Sometimes it can also be used to produce a large data-set for pre training followed by a fine tuning phase with manually screened data. After some helper functions for visualization, we load all the models we're going to use, clip for classification, RT data, for object detection, and SAM 2.1 for segmentation. We also define here the classes we're going to use. We want to tackle images, so we know the time of day they were taken and also the weather at that time. In production use cases, we often use tags like these to sub-select the data down the line to say isolate failure cases or for other analysis. The first task for you was to complete the following function that classifies the driving conditions. You had to run the clip processor providing our time of day classes here, our image here, and specifying to return tensors and to use padding. Next, you had to invoke the clip model with the results of the pre processing. The code then takes the classification logics from the output and applies the softmax function to obtain class probabilities as normal in classification algorithms. We then do exactly the same for the weather classification. Finally, we return the results in a well formatted dictionary. The second task was for you to complete the function that runs object detection on the image in order to detect vehicles and people. You first had to apply the RT deter processor providing the image. Then you had to feed the results into the model like this. The code then applies the post processor and extracts some results, filtering also for people, cars, buses and trucks. Then we need to solve a little problem. The images are taken from inside our car. The object detection algorithm recognizes even our own car and provides a box that encloses the dashboard and the windshield. This is obviously not something we're interested in, so we filter it out by exploiting the fact that such a box covers a significant part of the image. In technical terms, we filter out boxes with an intersection over union larger than a threshold, which by default, we fix to 80%. Next, the third task. Here, you had to complete the function that segments the objects found by the object detection algorithm. You had to run the image through the SAM processor providing the boxes we found in the object detection stage. Then you had to feed the result into the SAM model. The code then runs the post processor to get the final masks. Remember that SAM returns multiple masks for every object. Here, we simply select the mask with the largest expected intersection over union. This, in practice, means that we are selecting the masks in which the model is the most confident. Since we are starting from our bounding boxes, these will likely also be the masks encompassing the entirety of the object of interest, instead of just one of its parts. The next cell defines the function that brings everything together. It receives as input one or more images we want to process, as well as the threshold to use for the significance of the detections. Let's look at what it does. First, we make sure we have a list of images even when the user only provided one image. Then we loop over the images, and we run the three functions we defined above. We first run the classifications with clip. Then we do object detection to detect vehicles and people, then we segment those objects. Finally, we compile the results. After the loop is done, we return what we have found. We're done with the hard part. Let's run it on a few images. Let's start with one. This is a scene of our car driving through the streets of San Francisco on a rainy day. There's quite a bit of traffic. Let's run the complete pipeline on this image, and let's see what we get. We got 18 objects, and our classifications determined that the image is taken during the day and in rainy weather, which is accurate. Let's visualize the result by using the helper function we defined at the beginning of the notebook. We can see that we detect all the cars close to us, and the segmentation masks seem of high quality. Now that we know the pipeline is working, let's run it on all images and see the results. The first image is taken during a foggy day and features one truck and two people. Our models provide the right tags and segment the objects accurately. The second image is taken during a sunny day. There are 12 cars visible. Again, the tags are correct, and the vehicles are segmented well. The third image is taken at sunset or sunrise because the sun is lower on the horizon, and the light is very diffuse. There are no vehicles nor people in sight. The answers from our pipeline are all correct. Finally, the fourth image is the same city image we've seen before, and the results are once again correct. Here you have it, a complete auto labeling pipeline for self driving images. This concludes the solution to this exercise. Congratulations for getting here and see you next time.