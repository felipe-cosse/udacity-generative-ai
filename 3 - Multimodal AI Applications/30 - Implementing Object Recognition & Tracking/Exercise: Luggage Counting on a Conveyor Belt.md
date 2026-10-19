In this exercise, you will create an application that counts bags on an airport conveyor belt using a real sample video (bags.mp4). You’ll run a YOLO model for object detection, then track the detected objects with ByteTrack and count crossings using a line counter. The process involves applying padding, resizing, and inverse transforms to ensure correct box placement, followed by using Non-Maximum Suppression during the model’s post-processing stage. Finally, you’ll produce an annotated output video displaying bounding boxes, track IDs, and a live count overlay.

Prerequisites:
Classroom workspace with Python 3.9+ and the following installed: PyTorch, OpenCV, Hydra, torchvision, PIL, numpy, tqdm, supervision, ffmpeg.
GPU optional (CUDA or Apple MPS). CPU works but slower.
Objectives:
By the end of this exercise, you will be able to:

Configure and run YOLO inference on video frames with correct preprocessing and post-processing.
Enable multi-object tracking with ByteTrack and convert detection outputs into the expected structure.
Count luggage crossings using a vertical line counter and export an annotated video.
Steps:
Open the exercise notebook or script in the classroom workspace
To use the Udacity workspace:
In the navigation pane on the left (below the table of contents), click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l4/exercises/1-object-counting/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Review helper functions and environment setup
get_fps_and_video_size(video_path) extracts FPS and frame dimensions.
get_model_instance(input_video) loads configuration via Hydra, selects device (CUDA/MPS/CPU), initializes the YOLO InferenceModel, and calls model.setup.
preprocess_frame(...) pads and resizes frames, returns batch_of_one and rev_tensor for inverse transforms.
Complete YOLO inference on one frame (fill TODOs)
In run_inference_on_one_frame(...):
Replace outputs = ... with:
outputs = model(batch_of_one)
Replace predicts = ... with:
predicts = model.post_process(outputs, rev_tensor)
This ensures correct NMS and reverse mapping of boxes to original image coordinates.
Run YOLO over the whole video for a quick validation
Call results, class_list = run_inference_on_video(input_video).
Confirm it iterates through frames and returns per-frame detections.
Instantiate the counter with tracking and counting (fill TODOs)
In YOLOVideoObjectCounter.__init__:
Create the tracker with the video FPS:
self.byte_tracker = sv.ByteTrack(frame_rate=fps)
The LineZone and annotators are already prepared for drawing and counting.
Implement the per-frame processing with tracking (fill TODOs)
In run_on_one_frame(self, frame, index):
Run YOLO on the current frame:
detections = self._yolo_inference(frame)
Update tracker with current detections:
detections = self.byte_tracker.update_with_detections(detections)
If a LineZone is provided, filter for bag classes and trigger the line:
self.line_zone.trigger(bag_detections)
Labels combine class name, tracker ID, and confidence; visualization draws boxes and labels. LineZoneAnnotator overlays the counting line and aggregated counts.
Define the counting line for the conveyor belt
Use the midpoint vertical line across the frame:
START = sv.Point(image_width // 2, 0)
END = sv.Point(image_width // 2, image_height)
Set triggering_anchors=[sv.Position.CENTER] so counts occur when the box center crosses the line.
Process and export the annotated video
Create a YOLOVideoObjectCounter with the specified line_zone.
Use sv.process_video(...) with the processor.run_on_one_frame callback to write the annotated output to output_detected.m4v.
Convert to MP4 using ffmpeg for broad compatibility.
Troubleshooting and validation
Empty output or few detections: confirm autocast is used and model.setup was called; ensure correct device selection message appears.
Misaligned boxes: verify PadAndResize is used and post_process receives rev_tensor.
No counts: confirm line_zone is passed to the counter and bag class filter (24, 26, 28) matches the model’s label set.
Slow processing: use GPU if available; reduce output resolution or frame rate if needed.
