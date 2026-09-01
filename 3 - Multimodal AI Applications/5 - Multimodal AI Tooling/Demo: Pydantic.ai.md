Pydantic.ai connects large language models (LLMs) with Pydantic schemas to produce reliable, typed outputs. This demo shows how to:

Analyze images with Gemini through Pydantic.ai.
Enforce structured outputs using Pydantic models.
Adjust behavior at runtime using dependencies.
Reuse the same patterns for audio analysis.
Real-world uses include automated tagging, content moderation, cataloging, metadata extraction, and routing based on structured model outputs.

Objectives
Environment setup and async handling in notebooks.
Building an Agent and sending multimodal inputs.
Designing Pydantic schemas to constrain model outputs.
Switching behavior with dynamic system prompts via dependencies.
Applying the same approach to audio.
Step-by-step instructions
1) Environment setup
To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l1/demos/2-pydantic-ai/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Copy environment template and add a Gemini API key.
Load environment variables in Python.
Commands and code:

cp env.example .env
GEMINI_API_KEY=[your key]
from dotenv import load_dotenv
load_dotenv()
2) Async in Jupyter
Apply nest_asyncio in notebooks to avoid RuntimeError about the running event loop.
import nest_asyncio
nest_asyncio.apply()
Note: use run_sync in notebooks; use await run(...) inside async codebases or scripts.

3) Utilities and sample image
Simple helper to show an image and model-generated caption.
from PIL import Image
import matplotlib.pyplot as plt

def display_image_with_caption(image: Image.Image, caption: str):
    plt.figure(figsize=(10, 6))
    plt.imshow(image); plt.axis('off')
    plt.title(caption, wrap=True, fontsize=8, pad=20)
    plt.tight_layout(); plt.show()

image = Image.open("matterhorn.png")
4) Image analysis (vanilla)
Create an Agent with a Gemini model.
Send a text prompt and a binary image as input.
Receive a free-form string output.
from pydantic_ai import Agent
from pydantic_ai.messages import BinaryContent
from io import BytesIO

prompt = "List as many objects as you can that are present in this image and return them as a comma-separated list."
agent = Agent('google-gla:gemini-2.5-flash-lite')

def analyze_image_with_pydantic_ai(img: Image.Image, prompt: str) -> str:
    img.thumbnail((600, 600))
    buf = BytesIO(); img.save(buf, format='JPEG')
    result = agent.run_sync([prompt, BinaryContent(data=buf.getvalue(), media_type='image/jpeg')])
    return result.output

caption = analyze_image_with_pydantic_ai(image, prompt)
display_image_with_caption(image, caption)
5) Structured output with Pydantic
Define a schema to lock the model’s response to a predictable structure.
Create an Agent with output_type.
Use the structured result directly in code (fields, dicts, JSON).
from pydantic import BaseModel
from typing import Literal

class ImageAnalysis(BaseModel):
    main_objects: list[str]
    image_type: Literal["city", "nature", "other"]
    scene_description: str
    estimated_location: str

agent = Agent(
    'google-gla:gemini-2.5-flash',
    output_type=ImageAnalysis,
    system_prompt="You are an expert image analyst. Analyze images and provide structured output."
)

def analyze_image_with_structured_output(img: Image.Image) -> ImageAnalysis:
    img.thumbnail((600, 600))
    buf = BytesIO(); img.save(buf, format='JPEG')
    result = agent.run_sync([BinaryContent(data=buf.getvalue(), media_type='image/jpeg')])
    return result.output

analysis = analyze_image_with_structured_output(image)
print(analysis.image_type)
print(analysis.model_dump())
print(analysis.model_dump_json(indent=4))

if analysis.image_type == "nature":
    print("let nature be your teacher")
elif analysis.image_type == "city":
    print("when the lights go down in the city...")
else:
    print("What is this?")
6) Dynamic behavior with dependencies
Add a dataclass for options (dependencies).
Generate the system prompt at runtime based on options.
Pass deps to run_sync without changing the agent code.
from dataclasses import dataclass
from pydantic_ai import RunContext
from typing import Literal

class ImageAnalysis(BaseModel):
    main_objects: list[str]
    image_type: Literal["city", "nature", "other"]
    scene_description: str
    estimated_location: str

agent = Agent('google-gla:gemini-2.5-flash', output_type=ImageAnalysis, retries=5)

@dataclass
class OptionsDeps:
    description_verbosity: Literal["brief", "verbose"] = "brief"

@agent.system_prompt
def dynamic_prompt(ctx: RunContext[OptionsDeps]) -> str:
    sp = "You are an expert image analyst. Analyze images and provide structured output."
    if ctx.deps.description_verbosity == "brief":
        sp += " Keep the description very brief, use a max of 5 words."
    elif ctx.deps.description_verbosity == "verbose":
        sp += " Provide an extremely detailed description."
    return sp

def analyze_image_with_structured_output(img: Image.Image, deps: OptionsDeps) -> ImageAnalysis:
    img.thumbnail((600, 600))
    buf = BytesIO(); img.save(buf, format='JPEG')
    result = agent.run_sync([BinaryContent(data=buf.getvalue(), media_type='image/jpeg')], deps=deps)
    return result.output

brief = analyze_image_with_structured_output(image, OptionsDeps("brief"))
print(brief.model_dump_json(indent=4))

verbose = analyze_image_with_structured_output(image, OptionsDeps("verbose"))
print(verbose.model_dump_json(indent=4))
7) Not only images: audio analysis
Reuse the same workflow for audio via BinaryContent with audio media type.
from pydantic import BaseModel
from typing import Literal
from pydantic_ai import Agent
from pydantic_ai.messages import BinaryContent

class AudioAnalysis(BaseModel):
    transcription: str
    audio_type: Literal["speech", "music", "environment"]

agent = Agent(
    'google-gla:gemini-2.5-flash',
    output_type=AudioAnalysis,
    system_prompt="You are an expert sound analyst. Analyze sounds and provide structured output."
)

def analyze_sound_with_structured_output(audio_bytes: bytes, prompt: str) -> AudioAnalysis:
    result = agent.run_sync([prompt, BinaryContent(data=audio_bytes, media_type='audio/wav')])
    return result.output

audio_bytes = open("LJ025-0076.wav", "rb").read()
caption = analyze_sound_with_structured_output(audio_bytes, "Analyze this audio")
print(caption.model_dump_json(indent=4))
Takeaways
Structured outputs reduce post-processing and make downstream logic safer.
Dependencies enable runtime control without editing agent code.
Multimodal inputs (image, audio) are supported with the same API shape.
Thumbnails reduce token usage and improve efficiency.
Use run_sync in notebooks; use await run(...) in async applications.








In this demo, we're going to look at how to leverage Pydantic AI. AI models are often components of larger applications. Pydantic AI allows you to specify an output schema for your interaction with the model in a model agnostic way. This makes it much easier to use the AI models output downstream in your application. Let's see how this is done. We first start by loading our credentials using the.env file. Since Pydantic AI uses asyncio, we need to allow for nested event loops if we want to use it within Jupyter. If you have no idea what I just said, don't worry. Just know that in the Jupyter environment, you need to run this. Finally, we define a simple function to display an image and its caption, which we'll use later and load a sample image for our experiments. With that out of the way, let's jump into the interesting part. Let's start with the vanilla example, where we use a simple prompt and run it through Gemini using Pydantic AI. This vanilla example, we serve as our foundation that we'll improve later. We start with the prompt, asking the model to list as many objects as it can in the provided image. In Pydantic AI, the main class we're going to leverage is the agent class. You create an instance by passing in the name of the model you want. Since Pydantic AI supports many vendors, OpenAI, Google, AWS, and others, you need the vendor and the model. Here, we're using Google Gemini 2.5 flashlight, the smallest model in the Gemini 2.5 family. Now, we create our simple function to execute our prompt. We receive a pillow image instance and our prompt as input. We first make sure the image is at most 600 by 600 pixels to avoid issues with larger images. We then use the bytes iotric to convert it to a bytes string in JPEG format without writing it to disc. Then we wrap it in the binary content container, specifying its a JPEG image by providing the appropriate mime type. Finally, we call the ransing method of the agent, passing in our prompt and our image wrapped in this binary content class. The result contains an output attribute with the string we want. Let's execute it and see what happens. We can see that everything worked and we got a list of objects contained in this image. Great. Now, let's build upon this foundation by introducing the key element that makes Pydantic AI useful, structured output. You're familiar with the Pydantic Python library, this will look very familiar. If not, follow along. The idea is simple. We define this schema, also called data model, which I called image analysis, that inherits from the Pydantic base model class. Don't get confused by the term model here. In the Pydantic context, base model is a data model, not an AI model. Confusing, I know. Similar to a Python data class, we specify the data elements that are part of this schema. Here we have a list of strings called main objects, a string literal, with only three possible values, CT nature or other, a seen description as a string, and an estimated location as another string. This is what we're asking the model to provide. Pydantic AI will force the AI model to output these four pieces of information and give us back an instance of the image analysis class. Now that we have our output schema, we can do exactly what we did before, but we add the output type option when we create the agent and provide our schema. Everything else stays the same. When I execute this cell, we get an instance of the image analysis data model. We can access the four elements using the dot operator, convert it to dict using model dump, or pretty printed using model dump, Jason. Why is this important? Because now we know exactly what the result contains. Downstream code can use it without dealing with free form text. For example, we can write simple if statements to handle CT versus nature images, or we could do something different depending on the objects that are detected in the list. This allows you to chain together standard software and AI in a structured way. Let's conclude with the functionality that Pydantic AI has, which can be useful in practice. Often, you define an agent instance that might have parameters. Pydantic AI offers a mechanism to control your agent's behavior at run-time or reuse the same agent with different settings in different parts of your code. This is achieved through the dependency injection system. Here we have the same agent as before with our output schema defined. However, we're not specifying the system prompt because we'll generate it dynamically depending on the settings. We add this option depth object. In this case, we're declaring a setting that controls the verbosity of the description and can only take two values, brief or verbose. Using the agent system prompt decorator, we create a function to generate the system prompt at run time, which receives the special context parameter containing our dependency, our options. We can then use the value of the description verbosity to append the appropriate instruction to the system prompt. Dependencies can also be used in other parts of the agent, but that goes beyond the scope of what we're going to cover today. With all of these in place, the rest of the code is largely the same, but we need to pass our options to the function and also as depths to the run sing core. Now, we can run the function twice with the two different verbosity settings, and we can see that our agent changes behavior depending on the setting we choose. Congratulations on reaching the end of this introduction to Pydantic AI. We've seen how to use it to code API-based models in a vendor independent way, how to add structured output, which is useful when AI models are part of larger systems, and how to add options with the dependency injection system. Great job.