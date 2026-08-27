In this hands-on exercise, you will build end-to-end multimodal AI workflows: image understanding with Gemini, image-text generation with SmolVLM2 on Hugging Face, and audio transcription with Gemini and Whisper. The exercise mirrors industry use cases such as product recognition from images, content description for accessibility, and speech-to-text pipelines for notes, support, and media indexing.

Prerequisites
Classroom workspace with JupyterLab or a local Python 3.10+ environment
Packages: python-dotenv, requests, Pillow, matplotlib, transformers, torch, IPython, google-genai, huggingface-hub
System dependency: ffmpeg installed and on PATH
GPU optional (T4 or similar recommended). CPU supported with longer runtimes
Access to the provided notebook/code
Gemini API key stored in .env: GEMINI_API_KEY=[your key]
Internet access to pull Hugging Face models
Objectives
By the end of this exercise, it will be possible to:

Configure credentials and call Gemini for image and audio tasks using the Google AI Python SDK
Format multimodal inputs for open-source VLMs (SmolVLM2) and generate captions/analyses
Transcribe speech with Gemini and Whisper and compare outputs, speed, and cost factors
Manage device settings (GPU/CPU, float16), token budgets, and input size constraints for practical performance
Steps
Configure environment and credentials.
To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l1/exercises/1-showcase/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
In the parent folder of the notebook, copy the template and set the API key:
Run: cp env.example .env
Open .env and set GEMINI_API_KEY=[your key]. Leave other values unchanged.
Ensure required packages are installed.
Confirm that load_dotenv("../.env") finds the key by inspecting os.getenv("GEMINI_API_KEY") in a scratch cell (do not print secrets).
Load utilities and prepare data
Run the cell that imports requests, PIL, matplotlib, and defines:
get_image_from_url(image_url)
display_image_with_caption(image, caption)
Fetch a random image with the given image_url (picsum.photos). Expect a different image on each run.
Implement Gemini image analysis
In analyze_image_with_gemini:
Create the client with genai.Client(api_key=os.getenv("GEMINI_API_KEY")).
Keep the provided GenerateContentConfig with thinking_budget=0.
Ensure image resizing to thumbnail(600, 600) is executed to limit token usage.
Build image_part via types.Part.from_bytes(..., mime_type="image/jpeg").
Call client.models.generate_content with:
model="gemini-2.5-flash-lite"
contents=[prompt, image_part]
config=config
Execute the cell to render the image with the returned object list caption.
Experiment by changing the prompt (e.g., "Return a JSON array of detected objects." or "Describe the scene in 20 words.").
Prepare Hugging Face messages for SmolVLM2
Complete get_huggingface_messages(img, prompt) to return a list with a user role whose content contains:
an image entry {"type": "image", "image": img}
a text entry {"type": "text", "text": prompt}
This structure is required by the processor’s chat template.
Run SmolVLM2 for image-text generation
Create the processor with AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM2-500M-Video-Instruct")
Load the model with AutoModelForImageTextToText.from_pretrained(..., torch_dtype=torch.float16, device_map="auto")
Build inputs using processor.apply_chat_template(..., add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt"), passing the messages from Step 4. Move to model.device with dtype=torch.float16.
Generate with model.generate(**inputs, max_new_tokens=16). Increase tokens if output truncates.
Decode with processor.batch_decode, slicing generated_ids to exclude the prompt (e.g., generated_ids[:, inputs['input_ids'].shape[1]:]).
Display the image with the generated result. Compare outputs vs. Gemini for concise lists, descriptive captions, or structured formats.
Implement Gemini audio transcription
In analyze_audio_with_gemini:
Build audio_part via types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav").
Call client.models.generate_content with:
model="gemini-2.5-flash-lite"
contents=[prompt, audio_part]
config=config
Load audio bytes from ../LJ025-0076.wav, run the function, and print the transcription.
Optional prompt variations:
"Transcribe and normalize punctuation."
"Transcribe and translate to Spanish."
Transcribe audio with Whisper (open-source)
Ensure ffmpeg is installed (e.g., apt-get install -y ffmpeg or brew install ffmpeg).
Load processor and model: openai/whisper-large-v3-turbo, move model to device.
Build the pipeline("automatic-speech-recognition", model=..., tokenizer=processor.tokenizer, feature_extractor=processor.feature_extractor, device=...)
Run the pipeline on ../LJ025-0076.wav and print the resulting text.
Compare output with Gemini’s transcript and the known line. Note latency differences (GPU vs. CPU) and costs (local vs. API).
Iterate, measure, and document
Try longer outputs for SmolVLM2 (e.g., max_new_tokens=64) and more constrained prompts for Gemini (JSON schemas, bullet outputs).
Observe memory and speed trade-offs (image thumbnailing, float16, device_map="auto").
Capture short notes on accuracy vs. speed and cloud vs. local behavior.