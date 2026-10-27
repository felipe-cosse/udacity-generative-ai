This walkthrough shows you how to build a structured tagging pipeline for short clips using Pydantic AI and Gemini 2.5 Flash Lite, produce consistent labels—such as quality indicators, actions, and objects—for downstream robotics QA and analysis, and understand how a strict schema keeps the model’s output controlled, reliable, and unambiguous.

To use the Udacity workspace

Click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l4/exercises/3-video-tagging/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the environment named the same as this activity’s directory.
Step-by-step Instructions
Copy .env and set GEMINI_API_KEY.
Confirm libraries installed: pydantic, pydantic-ai, python-dotenv, and Google model support.
Apply nest_asyncio if running in a notebook.
Define VideoTagging with Literal[...] fields.
Configure GoogleModelSettings for deterministic, fast runs.
Create the Agent with output_type=VideoTagging and schema-aligned instructions.
Implement load_video_for_analysis using BinaryContent.
Loop through local media files, run the agent, and print structured results.
Adjust media_type, folder path, and object list as needed.
Code Snippets
1) Environment and libraries
Credentials are read from .env using dotenv. Assertions ensure proper setup:
.env present
GEMINI_API_KEY defined
nest_asyncio.apply() enables safe async within notebooks.
cp env.example .env
# Edit .env to set GEMINI_API_KEY=your_key
Common issues:

Missing .env or key triggers the assertions.
Notebook stalls without nest_asyncio.
2) Response schema with Pydantic
VideoTagging (the output schema) defines clear fields and strict value sets:

class VideoTagging(BaseModel):
    description: str = Field(
        description="A detailed description of the action performed in the video"
    )
    quality: Literal["poor", "ok", "good"] = Field(
        description="Overall technical quality of the video (e.g., resolution, stability)"
    )
    actions: List[
        Literal[
            "move object sideways",
            "move object vertically",
            "put object into another object",
            "pull object out of another object",
        ]
    ] = Field(description="Action classification")
    objects_involved_in_the_action: int = Field(
        description="Number of distinct objects involved in the action"
    )
    objects_present: List[
        Literal[
            "candle", "container", "cotton swabs", "basket", "box", "tape",
            "board game", "mug", "jar", "slipper", "container", "scarf",
            "smartphone", "pen",
        ]
    ] = Field(description="List of objects present in the video")
Notes:

Literal[...] ensures only allowed labels are used.
A duplicate container appears in the items list; de-duplication is harmless but preferred.
3) Model settings and agent
Gemini is configured for speed and stability:

settings = GoogleModelSettings(
    google_thinking_config={"thinking_budget": 0},
    temperature=0,
    seed=42,
)
Build the agent with output_type=VideoTagging. Ensure instructions align with the schema labels:

video_agent = Agent(
    model="gemini-2.5-flash-lite",
    output_type=VideoTagging,
    instructions="""
    You are an expert media content analyzer. Carefully review the provided clip and return:

    1. The overall technical quality: poor | ok | good
    2. The actions performed (choose from):
        - move object sideways
        - move object vertically
        - put object into another object
        - pull object out of another object
    3. The number of distinct objects involved in the action
    4. The objects present (use only from the allowed list)

    Rules:
    - Focus on the interaction with objects, not just hand motion.
    - Output must match the schema exactly.
    """,
    model_settings=settings,
    retries=5,
)
Why this matters:

Mismatched instructions (e.g., “push or pull”) cause schema validation errors.
output_type makes the model return structured data that pydantic can validate.
4) Load media data
The helper wraps raw bytes as BinaryContent with the right media_type:

def load_video_for_analysis(video_path):
    with open(video_path, 'rb') as f:
        video_bytes = f.read()
    return BinaryContent(data=video_bytes, media_type='video/mp4')
Tip:

Set media_type to match the actual format (e.g., video/quicktime for .mov).
5) Run analysis over a folder
Iterate over files, send a mixed input (text + binary), and print structured output:

from pathlib import Path
from pprint import pprint

videos = Path("../videos").glob("*.mp4")

for video_path in videos:
    media = load_video_for_analysis(video_path)
    result = video_agent.run_sync(
        ["Please provide a detailed description of this clip.", media]
    )
    pprint(result.output.model_dump(), width=80, depth=None)
Remember
Structured outputs make labeling reliable and easy to consume.

Keep instructions and allowed labels synchronized with the schema to avoid validation failures.








Today, we're building an automated video tagging system using Pydantic AI and Gemini. We will recognize actions in video, not just objects. This requires an understanding of the time dimension as the action unfolds over time. We're going to solve that problem by teaching an AI to watch videos and extract structured metadata automatically. We begin by importing the necessary libraries and loading environment variables. We're using Pydantic AI for structured outputs, the Gemini API for video understanding, and nest_asyncio to be able to use run_sync in Pydantic AI instead of async operations within Jupyter. Make sure your Gemini API key is properly configured in the.env file. Next comes the core of our solution, defining the response schema. You had to create a video tagging class using Pydantic base model. The first field you needed to define was a description string with an appropriate field description. Then you had to add a quality field using literal to restrict values to poor, okay, or good. This represents the technical quality of the video. For the actions field, you needed to create a list of literal values, representing different types of manipulations, moving objects sideways, moving them vertically, putting one object into another, or pulling objects out. You also had to define objects involved in the action as an integer to count distinct objects. Finally, objects present as a list of literal values containing all the possible objects that might appear in the videos, things like candles, containers, cotton swabs, baskets, and so on. We then move to creating the Pydantic AI agent. We first set up Google model settings to disable thinking mode and configure temperature and seed for consistent results. You had to create the agent using the agent class, specifying Gemini 2.5 flashlight as the model, video tagging as the output type, and providing clear instructions. Your instructions needed to tell the agent to analyze video quality, identify actions being performed, count objects involved, and list all objects present. In my experiments, I found that I got better results by including a rule telling the agent to focus on actual actions performed on objects rather than just hand movements. Next, we define a helper function that loads videos from disc and formats them as binary content for Pydantic AI. This wraps the video bytes with the appropriate media type so the model can process them. Finally, we put it all together in the analysis section. We iterate through all videos in the videos folder. Display each one, load it using our helper function, and run the agent on it. You had to call run_sync on the video agent, passing both a prompt, asking for a detailed description, and the video content itself. The agent returns structured results matching our video tagging schema, which we then display using P print. Let's look at a couple of examples. In this first example, the model correctly categorizes this action as pull object out of another object and also provides the correct number of objects, as well as other reasonable attributes. Let's look at the next. Once again, the action as well as the objects involved are correctly recognized. As you can see from the results, the model successfully identifies actions like pulling objects out of containers, moving objects sideways, and determines video quality based on resolution and stability. It correctly counts objects involved and lists what's present in each video. This demonstrates that foundation models as of today can recognize actions unfolding over time, and categorize them, as well as recognizing several attributes of the objects involved. That concludes our demo for today. Thanks for watching.