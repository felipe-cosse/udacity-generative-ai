This demo shows how Pydantic AI and Gemini 2.5 Flash can generate structured descriptions of video content. The workflow turns raw video into clean, consistent JSON that fits downstream needs such as search, tagging, accessibility, moderation, and content management.

Process Overview
Environment prepared and credentials loaded from .env.
Response schema defined using Pydantic models.
Gemini-backed Agent configured with structured output.
Helper function created to load videos as BinaryContent.
Video bytes submitted to the Agent with a concise instruction.
Structured JSON returned and printed.
For longer videos, the File API used instead of raw bytes.
Step-by-Step Instructions
1) Environment and Credentials
To use the Udacity workspace:
Click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l4/demos/2-video-understanding-with-fm/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the environment named the same as this activity’s directory.
Copy and configure the environment file:
cp env.example .env
# Edit .env and set GEMINI_API_KEY=...
2) Define the Structured Output
A Pydantic model ensures consistent, machine-friendly results.

from pydantic import BaseModel, Field
from typing import List
from typing_extensions import Literal

class VideoDescription(BaseModel):
    summary: str = Field(description="A concise 2-3 sentence summary of what happens in the video")
    quality: Literal["poor", "ok", "good"] = Field(description="Overall technical quality")
    main_subjects: List[str] = Field(description="Key people, objects, or animals visible")
    setting: str = Field(description="Location/environment where the video takes place")
    visual_style: str = Field(description="Lighting, colors, camera work, etc.")
3) Configure the Pydantic AI Agent
Model settings avoid long-thinking modes to reduce latency.
Agent configured to output the VideoDescription schema.
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModelSettings

settings = GoogleModelSettings(google_thinking_config={"thinking_budget": 0})

video_agent = Agent(
    model="gemini-2.5-flash-lite",
    output_type=VideoDescription,
    instructions="""
    You are an expert video content analyzer. Watch the provided video carefully and provide:
    1. A clear summary of what happens
    2. Identification of main subjects (people, objects, animals)
    3. Description of the setting/environment
    4. Key actions taking place
    5. Visual style characteristics
    6. Overall mood and tone
    7. Duration estimate
    8. Any notable or interesting details
    Be detailed but concise. Focus on what you can actually observe in the video.
    """,
    model_settings=settings,
)
4) Prepare Video Bytes for Analysis
BinaryContent packages raw bytes with a media type.

from pydantic_ai import BinaryContent

def load_video_for_analysis(video_path: str) -> BinaryContent:
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    return BinaryContent(data=video_bytes, media_type="video/mp4")
5) Run an Analysis
Load the file, then send a short instruction and the BinaryContent.
from pprint import pprint

video_path = "dog.mp4"  # Replace with actual path
video_content = load_video_for_analysis(video_path)

result = video_agent.run_sync(
    ["Please provide a detailed description of this video.", video_content]
)

pprint(result.output.model_dump(), width=80, depth=None)
Expected output: a JSON-like object matching the VideoDescription schema, including summary, quality, subjects, setting, and visual style.

6) Handling Longer Videos
For longer assets, use the File API.

# Example (requires a client instance and environment that supports file uploads)
myfile = client.files.upload(file="path/to/video.mp4")
result = video_agent.run_sync(
    ["Please provide a detailed description of this video.", myfile]
)
Takeaways
Structured outputs with Pydantic greatly simplify post-processing.
Gemini 2.5 Flash Lite provides fast, multimodal understanding suitable for video description.
BinaryContent is the simplest path for small to medium files; the File API is suited for larger media.
Clear, bounded schemas reduce variability and improve reliability across videos.
Disabling extended “thinking” lowers latency for iterative experimentation.







Today, for a quick demo, we're going to learn how to analyze video content using Pydantic AI and the Gemini model from Google. We'll see how to extract structured information from videos automatically. Let's get started. Before we begin, make sure you've set up your environment properly. You'll need to copy the Example environment file to create your own.env file. Then edit it and add your Google Gemini API Key. This is essential for authentication with the Gemini API. We start by importing all our necessary libraries. We're bringing in os and dotenv for environment management, pydantic for defining our data models, pydantic AI for the agent framework, and some display utilities for showing videos in the notebook. We then load the environment variables and assert that both the dotenv file loaded successfully and that our Gemini API key is present. Finally, we apply nest_asyncio, which is needed to run pydantic code properly within Jupyter notebooks without using asyncio explicitly. Let's define our response schema. This is one of the most powerful features of using pydantic AI. We can structure exactly what information we want to extract from data like videos. We create a video description class that inherits from base model. This class has several fields, a summary field that will hold a concise 2-3 sentence description of what happens in the video, a quality field that's a literal type limited to poor, okay or good to assess the technical quality, a main subjects field that's a list of strings identifying key people, objects, or animals, a setting field describing the location, and a visual style field describing lighting, colors, and camera work. Each field has a description parameter that guides the model on what to extract. This structured approach ensures we get consistent machine readable output that can be easily used in downstream applications like content management systems. Next, we create our pydantic AI agent. First, we configure the Google model settings. We set the thinking budget to zero. This disables the model's extended reasoning mode to avoid long wait times and expensive interactions, which we don't need in this demo. We then instantiate the agent using the Gemini 2.5 flashlight model, specify our video description class as the output type, and provide the detailed instructions. These instructions tell the agent, it's an expert video content analyzer, and should watch the video carefully to provide a summary, identify subjects, describe the setting, note key actions, analyze visual style, assess mood and tone, estimate duration, and highlight notable details. We emphasize being detailed but concise and focusing on observable content. Finally, we pass in our model settings. Now we need a helper function to load videos. We define load video for analysis, which takes a video path as input. Inside the function, we open the video file in binary read mode and read all the bytes. We then create a binary content object from pydantic AI, passing in the video bytes as data and specifying the media type as video MP4. This formats the video properly for the agent to process. The function returns this video content object. Note at the end of the notebook, there's information about using the file API for longer videos, which we can't demonstrate here due to testing environment limitations. Finally, let's analyze a video, first display the original video in the notebook so we can see what we're analyzing. We then load the video using our helper function, which reads the video and formats it as binary content. Next, we call the agents run sync method, passing in a list containing our prompt. For example, please provide a detailed description of this video and the video content object. The agent processes the video and returns structured results. We then print out the analysis results using pprint, which gives us a nicely formatted dictionary showing all the extracted information, the summary quality assessment, main subjects setting description and visual style. Let's first watch the video and then see the results. In this example, the model correctly identifies that there's a dog running through yellow cones on a grassy field with a person in the background, rates the quality as good, describes the outdoor agility equipment setting, and notes the daylight with clear focus. This structured output can now be used for video cataloging, search, indexing, content moderation, or any other application, where you need to understand video content at scale. This concludes our quick demo for today. Thanks for watching.