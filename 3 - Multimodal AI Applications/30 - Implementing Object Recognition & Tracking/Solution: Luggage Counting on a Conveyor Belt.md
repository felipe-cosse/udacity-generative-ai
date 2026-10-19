Object counting in a moving scene requires three parts: detection, tracking, and an event that triggers a count. This solution builds a complete pipeline to count luggage on a conveyor belt using:

YOLO for object detection
ByteTrack for multi-object tracking
A vertical line trigger for counting when bags cross

Step-by-Step Instructions
Prepare environment
To use the Udacity workspace:
In the navigation pane on the left (below the table of contents), click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l4/exercises/1-object-detection/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Initialize model and helpers
Use get_model_instance(input_video) to prepare YOLO and config.
Create PadAndResize(cfg.image_size).
Run frame-level inference
For each frame: preprocess, model(batch_of_one), model.post_process(..., rev_tensor=rev_tensor).
Convert detections for tracking
Map YOLO tensor to sv.Detections with xyxy, confidence, and class_id.
Set up tracker and line counter
Create sv.ByteTrack(frame_rate=fps).
Define a vertical sv.LineZone at the belt center with triggering_anchors=[sv.Position.CENTER].
Count bag classes
Filter class_id in {24, 26, 28}.
Call line_zone.trigger(bag_detections) each frame.
Annotate and export
Draw boxes, labels, and line counter overlays.
Use sv.process_video with a callback that runs the per-frame pipeline and returns the annotated frame.
Code Snippets
1) Model setup and configuration
Device selection (CUDA, MPS, or CPU) and default device set for tensors.
Hydra used to load YOLO configuration and override parameters for inference and video source.
Model initialized, switched to eval mode, and post-processing prepared.
device = ("cuda" if torch.cuda.is_available() else
          "mps" if torch.backends.mps.is_available() else "cpu")
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
Why it matters: correct device handling prevents tensor mismatch issues; model.setup prepares NMS and related steps.

2) Frame preprocessing for YOLO
Frames padded and resized to the model’s expected input size using PadAndResize.
A dummy fake_boxes tensor provided to satisfy the transform API.
Two outputs from preprocessing:
batch_of_one: ready for inference
rev_tensor: metadata to reverse transforms back to original coordinates
transformed_frame, _, transform_info = pad_and_resize(frame, fake_boxes)
batch_of_one = to_tensor(transformed_frame)[None].to(device)
rev_tensor = transform_info[None].to(device)
Why it matters: consistent input shape and reversible transforms preserve geometric accuracy.

3) Run inference on one frame
Model called on the batch to get raw detections.
Post-processing (including NMS) applied with rev_tensor to map boxes back.
outputs = model(batch_of_one)
predicts = model.post_process(outputs, rev_tensor=rev_tensor)
untransformed_frame, predicts[0].detach().cpu()
Output format per detection: (class_id, x1, y1, x2, y2, score).

4) Inference across the video
OpenCV reads frames sequentially.
Autocast on the model’s device ensures good numeric behavior for this YOLO version.
Results stored per frame.
with torch.no_grad():
    with autocast(model.device.type):
        for _ in tqdm(range(n_frames), total=n_frames):
            ret, frame = cap.read()
            if not ret: break
            untransformed_frame, predicts = run_inference_on_one_frame(
                model, frame, pad_and_resize
            )
            results.append([untransformed_frame, predicts])
Why it matters: torch.no_grad() and autocast improve speed and stability.

5) Tracking and counting with Supervision and ByteTrack
ByteTrack initialized with video fps to maintain consistent tracking.
YOLO outputs converted to sv.Detections (xyxy, confidence, class_id).
Tracker updated per frame; line zone used to count luggage types crossing the line.
self.byte_tracker = sv.ByteTrack(frame_rate=fps)

detections = sv.Detections(
    xyxy=yolo_outputs[:, 1:5],
    confidence=yolo_outputs[:, 5],
    class_id=yolo_outputs[:, 0].astype(int),
)

detections = self.byte_tracker.update_with_detections(detections)

bag_detections = detections[
    (detections.class_id == 24) |  # backpack
    (detections.class_id == 26) |  # handbag
    (detections.class_id == 28)    # suitcase
]
self.line_zone.trigger(bag_detections)
Notes:

Class IDs follow the model’s class_list. Here, 24, 26, and 28 represent bag types.
The line zone triggers when the chosen anchor (e.g., center) crosses the line.
6) Visualization and output
Bounding boxes and labels drawn using Supervision annotators.
Line zone annotator shows the counting line and current totals.
annotated = self.bounding_box_annotator.annotate(scene=frame.copy(), detections=detections)
annotated = self.label_annotator.annotate(scene=annotated, detections=detections, labels=labels)
annotated = self.line_zone_annotator.annotate(annotated, line_counter=self.line_zone)
Remember: Accurate counting depends on correct post-processing (with rev_tensor) and consistent tracking (ByteTrack with the correct fps).







Come to the solution walk-through for the object counting exercise. Today, we're tackling a practical problem, counting bags on an airport conveyor belt. This combines object detection with tracking to maintain counts as objects move through the frame. The approach here generalizes to many real-world scenarios like traffic monitoring, crowd counting, or inventory management. We begin with a set of helper functions that handle the boilerplate code. These functions take care of loading the YOLO model, pre-processing video frames, and extracting metadata like frame rate and video dimensions. The key thing to understand here is that YOLO requires frames to be padded and resized to match its expected input resolution. We also need to keep track of the transformations so we can reverse them later. Now, we move to the first part where you had to complete some code. The function here runs YOLO on a single frame and returns the detections. First, we preprocess the frame to get it ready for the model, which gives us the transformed frame, the reverse transformation information, and the original untransformed frame. Next, you had to run YOLO on the pre-processed frame. This is straightforward. You just call the model on the batch containing one frame. The model returns raw outputs that need further processing. After getting the raw outputs, you had to reformat them and apply non-maximum suppression to remove duplicate detections. You needed to call the model's postprocess method, passing in both the outputs and the reverse tensor. The reverse tensor is crucial here because it allows the post-processor to convert the bounding boxes back to the original image coordinates. Without this, your boxes would be in the wrong positions. The rest of this function just extracts the first element from the batch, since we're processing one frame at a time. We then have a function that runs inference on the entire video. It loads the model, opens the video with OpenCV, and loops through all frames. For each frame, it calls the function we just discussed and collects all the results. Note the use of auto cast here; this is essential for good performance with this version of YOLO. Without it, you'll see significantly degraded results. Let's test this first part to make sure the detection is working correctly before we add tracking and counting. Now we get to the heart of the exercise. The class that handles tracking and counting. In the initialization, we load the model and get the video metadata. Here, you had to create an instance of the bi-track tracker. The key parameter is the frame rate, which you needed to set to match your video's FPS. The tracker uses this information to make better predictions about object motion between frames. We also initialize some visualization utilities that will help us see what's happening in the output video. The method that converts Yolo outputs to supervision format is already provided. It reorganizes the detection data into the structure expected by the BYTETrack tracker, bounding box coordinates, confidence scores, and class IDs. Now, we come to the main method that processes each frame. This is where most of your work was concentrated. First, you had to run YOLO on the frame using the inference method we created earlier. This gives you the detections in the supervision format. Next, you had to update the tracker with these new detections. The tracker maintains object identities across frames by calling its update method with the detections. This is what gives each object a persistent ID as it moves through the video. After tracking, we filter the detections to find only bags. We're looking for three classes, backpacks, handbags, and suitcases, which have specific class IDs in the COCO data set. Then you had to trigger the line zone with the bag detections. The line zone keeps track of objects crossing the counting line. When you call its trigger method with the bag detections, it updates the count based on which objects have crossed from one side to the other. The rest of the method handles visualization, drawing bounding boxes, labels with tracker IDs, and annotating the frame with the line and counts. Finally, we test the complete system. We define a vertical line in the middle of the frame, which acts as our counting boundary. Configure it to trigger when the center of a bounding box crosses the line. We then instantiate our processor and use supervisions process video function to handle the video processing loop. This function reads frames, calls our callback for each one, and writes the annotated frames to the output video. The result is a video showing detected bags with their tracker IDs and the count displayed on the line showing how many bags have passed through. Let's see it. If you got all the parts right, you should see each bag getting a consistent ID as it moves across the belt, and the count incrementing each time a bag crosses the line. This concludes our walk-through of the object counting exercise. The key concepts we've covered are running object detection with YOLO, tracking objects across frames with BYTETrack, and using line zones for counting. Thanks for following along.