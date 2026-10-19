This demo shows end-to-end object detection on a traffic clip using an MIT-licensed YOLOv9 implementation. The workflow progresses from frame-by-frame detection to multi-object tracking and counting. The focus is a common real-world use case: monitoring road traffic to detect vehicles, keep identities across frames, and count those that cross a line for analytics.

Process Summary
Part 1: Run YOLOv9 on each frame, draw boxes, export annotated media
Part 2: Track objects with ByteTrack to keep identities consistent
Part 3: Fix small-object drop-offs using overlapping slicing
Part 4: Count vehicles crossing a defined line
To use the Udacity workspace:

In the navigation pane on the left (below the table of contents), click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l4/demos/1-yolo/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Part 1 — Frame-by-frame Detection
Steps
Set input/output paths; read FPS and frame size using OpenCV.
Load YOLOv9 via Hydra; choose device (CUDA/MPS/CPU) and set default device for tensors.
Preprocess each frame (pad and resize), run the model in autocast, and post-process predictions (NMS).
Draw bounding boxes and export annotated frames to a media file.
Core Code Snippets
Paths and FPS/size:

input_video = "cars_on_bridge.mp4"
output_video = "output_detected.m4v"

import cv2

def get_fps_and_video_size(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return fps, (frame_width, frame_height)

fps, frame_size = get_fps_and_video_size(input_video)
Load YOLOv9 (Hydra + device setup):

from hydra import compose, initialize_config_module
from omegaconf import DictConfig
import torch
from yolo.tools.solver import InferenceModel

def get_model_instance(input_video: str):
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    torch.set_default_device(device)
    with initialize_config_module(config_module="yolo.config", version_base=None):
        cfg = compose(
            config_name="config",
            overrides=[
                "task.task=inference",
                "model=v9-s",
                f"task.data.source={input_video}",
                "use_wandb=false",
                f"device={device}",
            ],
        )
    model = InferenceModel(cfg).to(device)
    model.eval()
    model.setup(cfg.task.task)
    return model, cfg

model, cfg = get_model_instance(input_video)
Run inference across frames (autocast required for good results):

from yolo.tools.data_augmentation import PadAndResize
from torch.amp import autocast
from tqdm import tqdm
import numpy as np, torch

def run_inference_on_video(model, input_video):
    cap = cv2.VideoCapture(input_video)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pad_and_resize = PadAndResize(cfg.image_size)
    results = []
    with torch.no_grad():
        with autocast(model.device.type):
            for _ in tqdm(range(n_frames), total=n_frames):
                ret, frame = cap.read()
                if not ret: break
                # preprocess + model(...) + model.post_process(...)
                # returns (original_frame, predictions)
                untransformed_frame, predicts = run_inference_on_one_frame(
                    model, frame, pad_and_resize
                )
                results.append([untransformed_frame, predicts])
    cap.release()
    return results

results = run_inference_on_video(model, input_video)
Visualize and export:

from yolo.tools.drawer import draw_bboxes

def visualize(results, class_list):
    return [draw_bboxes(f, p, idx2label=class_list) for f, p in results]

frames = visualize(results, cfg.dataset.class_list)

def frames_to_video(frames, output_name='output.mp4', fps=5):
    import numpy as np, cv2, PIL.Image
    first_frame = frames[0]
    width, height = first_frame.size
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video = cv2.VideoWriter(output_name, fourcc, fps, (width, height))
    for frame in frames:
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        video.write(frame)
    video.release()
    print(f"Video saved as {output_name}")
    return output_name

video_file = frames_to_video(frames, fps=fps, output_name="output.mp4")
Part 2 — Multi-object Tracking with ByteTrack
ByteTrack associates detections across frames using high-confidence matches first, then recovers missed ones using lower-confidence matches. This stabilizes identities through occlusions and brief misses.

Steps
Wrap YOLO inference into a class with a ByteTrack instance.
For each frame: run YOLO, convert outputs to supervision.Detections, update tracker, draw boxes and labels.
Process input with sv.process_video and save output.
Usage Snippet
import supervision as sv

processor = YOLOVideoTrackerBasic(video_file=input_video)

sv.process_video(
    source_path=input_video,
    target_path=output_video,
    callback=processor.run_on_one_frame,
    show_progress=True,
)

# Optional: convert container for playback
!ffmpeg -i {output_video} -c:v libx264 -tag:v avc1 cars_on_bridge_detected_orig.mp4 -y
Part 3 — Handling Small Objects with Slicing
Small distant cars may be missed. A practical fix: split each frame into overlapping tiles, run inference per tile, then merge detections. supervision.InferenceSlicer handles slicing and merging.

Usage Snippet
processor = YOLOVideoTrackerWithSlicing(
    video_file=input_video, with_slicing=True
)

sv.process_video(
    source_path=input_video,
    target_path=output_video,
    callback=processor.run_on_one_frame,
    show_progress=True,
)

!ffmpeg -i {output_video} -c:v libx264 -tag:v avc1 cars_on_bridge_detected_2.mp4 -y
Part 4 — Counting Objects Crossing a Line
Define a line and count tracked objects that cross it. Filter by class to count only cars and trucks, for example.

Usage Snippet
# Define a horizontal line
_, image_size = get_fps_and_video_size(input_video)
START = sv.Point(0, image_size[1] // 4)
END = sv.Point(image_size[0], image_size[1] // 4)
line_zone = sv.LineZone(
    start=START, end=END, triggering_anchors=[sv.Position.CENTER]
)

processor = YOLOVideoObjectCounter(
    video_file=input_video,
    with_slicing=True,
    line_zone=line_zone
)

sv.process_video(
    source_path=input_video,
    target_path=output_video,
    callback=processor.run_on_one_frame,
    show_progress=True,
)

!ffmpeg -i {output_video} -c:v libx264 -tag:v avc1 cars_on_bridge_detected.mp4 -y
Apply the same steps to another traffic clip by redefining input paths and the line if needed.

Takeaways
Frame-by-frame detection provides boxes and classes; tracking adds stable identities across frames.
Autocast on the chosen device is crucial for good inference with this implementation.
Overlapping slicing significantly improves detection of small distant objects.
Line-based counting enables practical traffic analytics such as throughput estimation.
The MIT-licensed YOLOv9 workflow transfers to other YOLO variants with similar steps.







Today, we have a fan demo. We're going to learn how to perform object detection and tracking on videos using YOLO. We'll start with basic frame by frame detection, then move to tracking objects across frames. Finally, we'll tackle one of the most common real world applications, counting objects as they cross a boundary. Let's get started. Before we dive in, a quick note about licensing. We're using a fully open source implementation of YOLO here, specifically YOLOv9. Now, there are many YOLO versions floating around and many of them require enterprise licenses if you want to use them commercially. This version is currently the best open one available, although it is a bit dated. It's up to you to decide what fits your use case best. But the good news is the usage is always similar so what you learn here will apply no matter which version you end up choosing. With that out of the way, let's get to the code. We start by defining our input and output video paths. In this case, we're working with the video of cars crossing a bridge. The output video path is the path for the video we will generate that will contain the results of our inference annotated on the frames. First, we need the utility function to extract some basic information from our video. This function uses OpenCV to open the video file and grab two critical pieces of information. The frames per second, which tells us how fast the video plays and the frame size, which is just the width and height of each frame in pixels. We make sure to release the video capture object when we're done to free up resources. Now, let's talk about loading the YOLOv9 model. This particular implementation requires a bit more setup than some of the pre packaged versions you might find, but it gives us more control. We start by checking what device we have available. We then set this as our default device. This is actually critical for this specific YOLO implementation. If we don't do this, we'll run into issues with tensors being on different devices. Next comes the configuration loading. We're using hydra, which is a configuration management tool. The way this works is we load the default YOLO configuration, then override specific parameters. We tell it, we want to run inference, not training. We specify we want the v9S model, which is the smallest variant faster, but potentially less accurate than the larger models. We pointed to our video file, disable weights and biases tracking since we're just doing inference and specify our device. Once the configuration is set, we create an inference model instance and put it in evaluation mode. We then call setup with the task type which configures the post processing step, including non maximum suppression. This is important, NMS removes duplicate detections of the same object. Now for the actual inference. We need a pre processing function that takes each frame and gets it ready for YOLO. The model expects a specific input size, so we use a pad and resize transform, which, as the name suggests, pad the image to give it the right aspect ratio, and then resizes it to the size expected by YOLO. Because we are using OpenCV, we need to also do this transformation. OpenCV uses a peculiar channel ordering, namely blue green red, BGR, instead of the normal red green blue RGB, expected by YOLO. We go from BGR to RGB, then apply the transform. Because the transform can also work on ground root boxes during training, we pass in a dummy tensor of zeros. We don't have ground root during inference. The transform returns the processed frame, and some metadata will need later to reverse the transformation. We convert everything to tensors, add a batch dimension and move to our device. The inference function itself is straightforward. We preprocess the frame, run it through the model, then post process the outputs. The post processing applies non maximum suppression and transforms the detections back to the original image coordinates, using that reverse transformation metadata. We make sure to use torch dot no grad to avoid computing gradients, which would slow us down unnecessarily. To run inference on the entire video, we use OpenCV to loop through frames. We get the total frame count for our progress bar, create our transform object, and then iterate through every frame. For each frame, we read it, run inference, and store the results. One critical detail here, we wrap everything in an autocs context manager. This is absolutely necessary for good performance with this YOLO version. Without it, you'll get poor results because of how the model was trained. The autocast context manager converts some model weights from float 32 precision to float 16 precision on the fly. This is called mixed precision, and it is very useful during training to reduce GPU load and memory requirements. Since the model was trained that way, but saved in full precision, we need to do this here. After running inference, we need to visualize the results. We take our detections and use YOLO's built in drawer function to overlay bounding boxes on each frame. We provide the class list so the boxes can be labeled with the object names. Finally, we convert these frames back to a video. We grab the dimensions from the first frame, create a video writer with the AVC 1 coded, then write each frame after converting from RGB back to BGR. There we have it a video with all objects detected frame by frame. Let's look at it. We can see it's working, but notice how cars disappear once they get far enough away on the bridge. This is a classic YOLO problem. We'll fix it later.






Detection frame by frame is useful, but in many applications, we want to track objects across frames. Maintain their identity as they move through the video. This is where ByteTrack comes in. ByteTrack is a multi object tracking algorithm. It works in two main steps. First, it matches high confidence detections with existing tracks using similarity measures. Basically, it looks at how much the boxes overlap and uses motion prediction based on previous frames to guess where objects should be. Second, and this is clever, it recovers tracks using low confidence detections that were initially ignored. This helps handle brief occlusions. The algorithm starts new tracks for unmatched high confidence detections and keeps tracks alive briefly, even when unmatched, which helps handle temporary occlusions. If a track goes unmatched for too long, it gets deleted. To implement this, we create a class that encapsulates our tracking logic. We initialize it with the video file path, load our Yolo model, get the video FPS, and create a ByteTrack instance with that frame rate. We also create annotators for drawing boxes and labels. We need the converter function because ByteTrack expects detections in a specific format. We take yolos output tensor and reorganize it into a detections object with the box coordinates, confidence scores, and class IDs. For each frame, we run Yolo inference, convert the outputs to the ByteTrack format, then update the tracker with the new detections. This is where the magic happens. The tracker associates detections across frames. We then create labels that include not just the class name and confidence, but also the tracker ID. This idea is what maintains object identity across frames. We annotate the frame with boxes and labels, then process the entire video using supervisions convenient process video function, which handles all the frame reading and writing for us. Let's look at the results. When we look at the results, we can see objects now keep their identity through the video. The same car keeps the same ID number as it moves, but we still have that problem with small objects disappearing. If you look at our bridge video, you'll notice something. Cars are detected well when they're close. But as they move away and get smaller, the detections become unstable and eventually disappear. This is a classic problem with object detection models. They struggle with small objects. Here's a simple but effective trick. We divide the image into overlapping sub images. Run yolo on each independently, then remove redundant detections. It's like giving the model a closer look at different parts of the image. Supervision makes this easy with the inference slicer class. We tell it to slice our image into sections that are half the width and height of the full image with an overlap of one sixth on each side. Overlap is important. It ensures objects near slice boundaries are properly detected. We pass our inference function as a callback. The slicer will call this function on each slice automatically. The slicer handles all the complexity of splitting the image, running our callback on each piece, adjusting coordinates back to the full image space, and removing duplicate detections with non maximum suppression. In our tracking class, we add A with slicing parameter. If true, we wrap our inference function with the inference slicer. Otherwise, we use the inference function directly. This makes it easy to compare results with and without slicing. Everything else remains the same. We just replace our direct inference code with the slicer code. When we run this on our bridge video, the difference is dramatic. Let's see it. Cars are now detected consistently even when they're far away on the bridge. This slicing gives yolo a much better chance to detect those small objects.






That our detections are high quality, let's tackle a common real world application. Counting objects crossing a boundary. Imagine you're doing traffic planning and want to count how many vehicles cross a bridge in an hour. We define a line in our video, in this case, a horizontal line across the bridge. Supervisions line zone class handles the counting logic. We give it a star point and endpoint for the line, and we tell it to trigger the count when the center of a bounding box crosses the line. In our tracking class, we add the line zone and create an annotator to visualize it. On each frame, after updating the tracker, we filter detections to only include cars and trucks, Classes 2 and 7 in the Coco data set. We then trigger the line zone with these detections. The line zone internally checks if any tract objects cross the line since the last frame. When annotating, we add the line zone annotation, which draws the line on the video and displays the in and out counts. The in count is objects crossing the line in one direction, out is the other direction. We can see this working on the bridge video. The counts update as cars cross our line, let's try it on another video with two lane traffic. We place a horizontal line across the middle of the highway. Now, we're counting cars going both directions. Vehicles traveling toward the camera, increment the out count, vehicles going away, increment the in count, the results are good. It's not perfect in a production system, you'd want to tune parameters like the confidence threshold, the tracking parameters, maybe adjust the line position. For a quick demo with default settings is working quite well. Before we wrap up two things to keep in mind, the slicing technique comes with a performance cost since we're running inference multiple times per frame. You'll need to balance accuracy and speed for real time work also, this field moves fast. New Yolo versions drop constantly, so when building real applications, stay current, evaluate your options, and don't forget about licensing. This concludes our demopho today. You now know how to detect objects in videos frame by frame, track them across frames to maintain identity, handle small objects using slicing and count objects crossing boundaries. These are the building blocks for countless computer vision applications, surveillance, traffic monitoring, retail analytics, sports analysis and more. Thanks for watching.