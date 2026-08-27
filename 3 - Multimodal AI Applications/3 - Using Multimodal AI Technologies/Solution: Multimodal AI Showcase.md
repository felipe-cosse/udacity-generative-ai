This is a walkthrough of a multimodal workflow: image understanding and audio transcription using one hosted model (Gemini) and two open-source models (SmolVLM2 and Whisper). The exercise demonstrates how to prepare inputs for different APIs, manage model configurations, and compare performance and outputs across approaches.

Step-by-Step Instructions
1) Environment and credentials
To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l1/exercises/1-showcase/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Copy the example environment file and add the Gemini API key in the parent folder:
    cp env.example .env
Edit .env:
    GEMINI_API_KEY=[your key]
Load credentials from the parent folder:
    from dotenv import load_dotenv
    load_dotenv("../.env")
2) Utilities and data
Helper for downloading and displaying images using requests, PIL, and matplotlib.
Random image source:
    image_url = "https://picsum.photos/400/300"
    image = get_image_from_url(image_url)
The image changes on every run.
3) Standardize a Hugging Face “messages” payload
Build a messages list with both an image and a text prompt for VLM models:
    def get_huggingface_messages(img, prompt):
      return [{
          "role": "user",
          "content": [
              {"type": "image", "image": img},
              {"type": "text", "text": prompt},
          ]
      }]
4) Image analysis with Gemini
Prepare the client and config, reduce image size to save tokens, and send prompt + image bytes:
    from google import genai
    from google.genai import types
    import os
    from io import BytesIO

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    config = types.GenerateContentConfig(
      thinking_config=types.ThinkingConfig(thinking_budget=0)
    )

    image.thumbnail((600, 600))
    b = BytesIO(); image.save(b, format="JPEG")
    image_part = types.Part.from_bytes(b.getvalue(), mime_type="image/jpeg")

    response = client.models.generate_content(
      model="gemini-2.5-flash-lite",
      contents=["List all objects that are present in this image as a comma-separated list.", image_part],
      config=config
    )
    caption = response.text
Display the image with the returned description.
5) Image analysis with SmolVLM2 (local)
Load the processor and model with half-precision and automatic device mapping:
    from transformers import AutoProcessor, AutoModelForImageTextToText
    import torch

    model_name = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForImageTextToText.from_pretrained(
      model_name, torch_dtype=torch.float16, device_map="auto"
    )
Prepare inputs using the chat template and generate:
    inputs = processor.apply_chat_template(
      get_huggingface_messages(image, "List all objects in the image."),
      add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt",
    ).to(model.device, dtype=torch.float16)

    generated_ids = model.generate(**inputs, max_new_tokens=16)

    generated_texts = processor.batch_decode(
      generated_ids[:, inputs["input_ids"].shape[1]:],
      skip_special_tokens=True, clean_up_tokenization_spaces=True
    )
    result = generated_texts[0]
Display the image with the model’s output.
Tips:

Increase max_new_tokens if output truncates.
GPU provides large speedups; CPU works but is slower.
6) Audio transcription with Gemini
Create an audio part using WAV bytes and call the same generate_content API:
    audio_bytes = open("../LJ025-0076.wav", "rb").read()
    audio_part = types.Part.from_bytes(audio_bytes, mime_type="audio/wav")

    response = client.models.generate_content(
      model="gemini-2.5-flash-lite",
      contents=["Transcribe this audio file.", audio_part],
      config=config
    )
    text_transcript = response.text
7) Audio transcription with Whisper (open-source)
Build a Hugging Face pipeline for ASR:
    import torch
    from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "openai/whisper-large-v3-turbo"

    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
      model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    ).to(device)

    pipe = pipeline(
      "automatic-speech-recognition",
      model=model,
      tokenizer=processor.tokenizer,
      feature_extractor=processor.feature_extractor,
      torch_dtype=torch_dtype,
      device=device,
    )

    result = pipe("../LJ025-0076.wav")
    transcript = result["text"]
Remember: standardize input formatting (messages, MIME, sizes) and manage generation settings (token limits, precision, device) to get fast, reliable multimodal results across both hosted and open-source models.






Let's look at the solution of this exercise. First, you had to set up the dotenv file with your Gemini credentials, then execute the first cell to load them. A successful load returns through as shown here. We then had some boilerplate code with utility functions. The first function receives a URL, downloads the image using requests, and creates a bytes IO proxy that can be opened with pillow. The other function just generates a plot. Moving on, we get a random image from this website. Since it's random, your image will look different than mine each time you run this. Then we had the first part you completed formatting the image and prompt for hugging phase transformers. It's a list with a single dictionary element containing a user role, and content with both image and text components will use this function later. Now the fun part. Here you completed key pieces to work with Gemini. We have our prompt asking the model to list recognizable objects as a comma separated list. You had to generate a client instance using the client class with our API key from the environment variable. With our client ready, we set configuration, resize the image to 600 by 600 max, and generate an image part for Gemini using a byte cyotric to avoid saving to disc. Let's move on to the actual call to Gemini. We call generate content specifying Gemini 2.5 flashlight, the fastest and cheapest model available. We pass our prompt encoded image and configuration. The response contains the text we return. Finally, we call our function and display the result. As you can see here, Gemini recognized the main objects and return them in our requested format. It worked quite well. We can do the same with open source models. Here, you completed pieces to use the small VLM two model from hugging phase. First, you created the processor instance using from pre-trained. This handles input pre-processing and output post-processing. Second, you loaded the model itself from pre-trained, including two additional parameters from the documentation to speed up inference on GPU. Third, you completed the first argument to apply chat template. That data structure we set up earlier with prompt an image. Fourth, you implemented the generate call, passing our pre-processed inputs with the unpacking operator and setting max new tokens for output length control. Finally, you added post processing using batched decode, slicing the generated IDs to avoid decoding our own input prompt. After all the work, we get our caption displayed on the image. The model does a great job generating a relevant object list. The second part applied these same techniques to audio instead of images. We can go quickly since we only need small changes. For Gemini, we change the part type from image_JPEG to audio_wave and obviously update the prompt for transcription. We pass the audio part instead of image part to Gemini. With these three changes, including the prompt, we now have an audio transcription system. Executing this gives us an exact transcription. For the open source solution, we use the whisper model for audio processing. We generate the processor and model using from pre trained methods for transcription specific classes. Then we leverage the pipeline system. Since speech transcription is a standard ML task, Hugging phase provides a pipeline that handles all the manual steps we did earlier, encoding formatting, model inference, and output formatting. We pass the task name model, tokenizer, feature extractor, and efficiency arguments. Finally, we call the pipeline on our input file and get accurate results. This concludes our exercise. You've learned the basics of using Gemini and open source solutions for useful multimodal tasks. Congratulations.