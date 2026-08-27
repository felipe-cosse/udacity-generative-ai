This demo builds a small, practical multimodal workflow:

Fetch an image and generate captions using two approaches: an API-based model (Gemini) and an open-source model from Hugging Face.
Transcribe an audio file using an open-source speech recognition model (Whisper).
Real-world use case: prototype a captioning and transcription utility, compare cost, speed, and control between a managed API and local/open-source models, and practice safe credential handling.

Summary of the flow
Configure secrets with .env and avoid committing credentials.
Load an image from a URL and display it.
Generate a caption with Gemini (API-based).
Generate a caption with an open-source VLM (Hugging Face Transformers).
Transcribe an audio file with Whisper.
Compare outputs and latency, then display results.
Step-by-step instructions
To use the Udacity workspace:

At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l1/demos/1-showcase/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Secure credentials with .env

Never hardcode credentials in source files. Define in .env file.
Ensure .env is listed in .gitignore if using git for your work.
Load credentials in code:
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
Fetch and display an image
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

def get_image_from_url(image_url: str) -> Image.Image:
    return Image.open(BytesIO(requests.get(image_url).content)).copy()

def display_image_with_caption(image: Image.Image, caption: str):
    plt.figure(figsize=(10, 6))
    plt.imshow(image)
    plt.axis('off')
    plt.title(caption, wrap=True, fontsize=14, pad=20)
    plt.tight_layout()
    plt.show()

image_url = "https://picsum.photos/400/300"  # random image each call
image = get_image_from_url(image_url)
prompt = "Describe this image briefly"
Caption the image with Gemini (API-based)
Use the Gemini SDK.
Resize image to reduce token cost.
Set thinking budget to 0 for faster, cheaper responses.
    from google import genai
    from google.genai import types
    from io import BytesIO
    
    def analyze_image_with_gemini(img: Image.Image, prompt: str) -> str:
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )
    
    img.thumbnail((600, 600))
    image_bytes = BytesIO()
    img.save(image_bytes, format='JPEG')
    image_part = types.Part.from_bytes(
        data=image_bytes.getvalue(),
        mime_type='image/jpeg'
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[prompt, image_part],
        config=config
    )
    return response.text
    
    caption = analyze_image_with_gemini(image, prompt)
    display_image_with_caption(image, caption)
Caption the image with an open-source VLM (Hugging Face)
Load processor and model locally.
Use chat template to format image+text input.
Use EOS token to stop generation cleanly.
    import torch
    from transformers import AutoProcessor, AutoModelForImageTextToText
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    model_path = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"
    processor = AutoProcessor.from_pretrained(model_path)
    model = AutoModelForImageTextToText.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto"
    )
    
    messages = [
    {"role": "user", "content": [
        {"type": "image", "image": image},
        {"type": "text", "text": prompt},
    ]}
    ]
    
    inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    ).to(model.device, dtype=torch.float16)
    
    generated_ids = model.generate(
    **inputs,
    do_sample=False,
    max_new_tokens=512,
    eos_token_id=processor.tokenizer.eos_token_id,
    pad_token_id=processor.tokenizer.eos_token_id
    )
    
    generated_texts = processor.batch_decode(
    generated_ids[:, inputs['input_ids'].shape[1]:],
    skip_special_tokens=True,
    clean_up_tokenization_spaces=True
    )
    
    caption = generated_texts[0]
    display_image_with_caption(image, caption)
Transcribe audio with Whisper
ffmpeg must be installed on the system.
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3-turbo"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
).to(device)

asr = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

result = asr("LJ025-0076.wav")
print(result["text"])
Takeaways
Secrets must live in .env and never in source files; include .env in .gitignore.
API-based models offer quick integration and managed scaling; costs are per use.
Open-source models offer control and offline use; speed depends on hardware.
Reducing image resolution lowers token usage and latency for vision models.
Proper input formatting (chat templates, media parts) is essential for correct outputs.
EOS and padding tokens prevent runaway generations and simplify decoding.






In the next few minutes, we're going to look at some of the exciting things we can do today with multimodal AI. Let's start with an important but often overlooked element, handling your credentials securely. When using APIs or open source systems like Hugging Face, you need to provide credentials. Never put your credentials directly in your code, it's a severe security violation and makes your code hard to maintain. A simple solution is dot ENV files. These are text files you place where your code runs that can be easily loaded. Their content becomes environment variables you can reference in your code. For example, if we have a dot ENV file with our Gemini credentials, we can load it like this and then use that variable in our code. Obviously, never print these environment variables or they'll end up in your Jupyter Notebook and should be considered compromised. After these quick intron credentials, let's jump into the multimodal AI stuff. Here I have defined some utility functions to get test data and generate plots. Note that this URL generates a new image every time we execute this cell, so your results will differ from mine. Next, we define a prompt describing what we want the multimodal AI to do. Since we're using Hugging Face later, we also define this messages data structure, passing the image and prompt in the specific format Hugging Face expects. Now, for our first exciting result, here's a short function to use Google Gemini through their Pythons decay. We start by creating a client with lightweight configuration. Next, we resize the image to at most 600 by 600 pixels to prevent large images from causing problems. We then transform the image into a format that can be sent to Gemini by creating a part class instance, finally, we call Gemini. Passing our prompt image and configuration, then extract and return the generated text. If we execute this, we get something like this. The model clearly recognizes many elements in the image and provides a detailed caption describing its content. This is called image captioning, and it was incredibly easy with this foundational model, we can do the same using open source models. Here, I'm leveraging Hugging Face transformers and one of the small VLM 2 models. We start by defining the exact model from the Hugging Face model hub. Each model comes with its processor, which formats input and output data as the model expects, plus the model itself. We call the from pre trained method of the appropriate processor and model classes to get respectively the processor and the model instances. Now we apply the chat template we created earlier to format our inputs properly and move them to GPU if available. We generate the response by calling the generate method with our formatted inputs, then translate the generated tokens back to readable text using the processors batch decode method. When you first execute this, you'll see progress bars as Hugging Face downloads the model weights and other necessary data. This is clearly more work than calling an API, but the result is pretty good considering this model size. Only 500 million parameters versus Gemini several billions. The generated caption is more verbose than Gemini, but quite accurate. These models aren't limited to vision and text, they can process audio and much more. Let me show you one more thing. We'll take a simple audio file containing speech and generate transcripts using an open source model called Whisper. Here I'm using the same Hugging Face library, and the steps are very similar to image captioning. Creating processor and model instances using appropriate classes, then running them to get results. Instead of manual pre processing, inference and post processing, I'm leveraging Hugging Faces, pipeline functionality available for specific tasks and models, which handles everything in a simple call, and here's the transcribed text, which is exactly right. This concludes our quick overview of these models capabilities. We've only scratched the surface, but I hope I've piqued your interest.