This walkthrough explains how the solution structures, analyzes, and extracts standout moments from motocross footage using Pydantic AI with Gemini. The main premise: define a reliable schema for moments, guide a model with clear instructions, and produce consistent, structured outputs that power highlights, thumbnails, and chapter markers.

The approach centers on a nested schema:

SalientMoment: a single moment with a timestamp, type, description, and visual cues.
VideoSalientMoments: an aggregate containing a short summary, a list of moments, pacing notes, and an optional most significant timestamp.
The agent (pydantic_ai.Agent) is configured to:

Use gemini-2.5-flash-lite.
Produce output that conforms to VideoSalientMoments.
Follow instructions that emphasize action peaks, transitions, reveals, and strong visuals.
A helper function reads the motocross clip as bytes and wraps it in BinaryContent so the agent can analyze it. The agent then returns structured data that can be printed, logged, or fed into downstream tooling (highlight reels, automated editing, or UX controls).

Step-by-Step Instructions
Prepare environment
To use the Udacity workspace:
Click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l4/exercises/2-salient-moments/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the environment named the same as this activity’s directory.
Copy and edit the .env file:
cp env.example .env
Set GEMINI_API_KEY in .env.
Load and check environment variables with dotenv.
Apply nest_asyncio for notebooks.
Import dependencies
pydantic, pydantic_ai, typing, typing_extensions.Literal
IPython.display for local media display (optional)
os, dotenv, and pprint for utilities
Define the schemas
Create SalientMoment with:
timestamp: string like HH:MM:SS
moment_type: limited categories via Literal for consistency
description: concise, specific explanation
visual_cues: array of visual elements (e.g., “slow-motion”, “jump”, “camera shake”)
Create VideoSalientMoments with:
video_summary
total_moments_found
moments: list of SalientMoment
most_significant_moment
pacing_analysis
Configure Gemini model and agent
Use GoogleModelSettings with reduced thinking to avoid latency.
Initialize Agent with:
model="gemini-2.5-flash-lite"
output_type=VideoSalientMoments
Clear instructions emphasizing action peaks, transitions, emotion, and reveals.
Load motocross media
Use load_video_for_moments_analysis("../cross.mp4").
Ensure media_type matches the file format (e.g., video/mp4).
Run analysis
Call:
result = moments_agent.run_sync([
    "Identify and analyze the salient moments in this video.", 
    video_content
])
Extract the structured output:
data = result.output.model_dump()
Interpret and use the output
Read video_summary for a concise overview of the clip.
Validate total_moments_found against len(moments).
Use moments to build:
Highlight cuts for jumps, scrubs, whoops sections, near-misses, and landings.
Thumbnails based on strong visual_cues.
Chapter markers using timestamp.
Check pacing_analysis to understand distribution (clustered vs. evenly spaced).
Code Snippets
Core schema (condensed)
class SalientMoment(BaseModel):
    timestamp: str
    moment_type: Literal[
        "action_peak", "emotional_highlight", "visual_transition",
        "climax", "scene_change", "other"
    ]
    description: str
    visual_cues: List[str]

class VideoSalientMoments(BaseModel):
    video_summary: str
    total_moments_found: int
    moments: List[SalientMoment]
    most_significant_moment: Optional[str]
    pacing_analysis: str
Agent setup (condensed)
settings = GoogleModelSettings(google_thinking_config={"thinking_budget": 0})

moments_agent = Agent(
    model="gemini-2.5-flash-lite",
    output_type=VideoSalientMoments,
    instructions="""
    You are an expert analyst identifying salient moments...
    Provide approximate timestamps and be specific about why.
    """,
    model_settings=settings,
)
Media loading helper
def load_video_for_moments_analysis(video_path):
    with open(video_path, 'rb') as f:
        video_bytes = f.read()
    return BinaryContent(data=video_bytes, media_type='video/mp4')
Remember:

Structured schemas plus clear instructions produce consistent, automation-ready moment lists.
Moment types, timestamps, and visual cues together enable fast highlight creation and content navigation.







Welcome to this solution. Today, we're building a video analysis system that can automatically identify the most impactful moments in any video. We'll be using pedantic AI combined with Google's Gemini to create structured actionable insights from video content. Let's dive in. We start with the usual imports and environment setup. Make sure your Gemini API Key is in the.env file before running this. Now comes the interesting part defining the structure for our salient moments. We're building a nested schema architecture where a video level object contains a list of individual salient moment objects. First, you had to define the salient moment schema. This represents a single important moment in the video. You needed to create four fields. A timestamp as a string for when the moment occurs, a moment type, which is a literal type that classifies the moment into categories like action peak, emotional highlight, visual transition, climax, scene change, or other. Then a description field to explain what makes this moment significant. Finally, visual cues as a list of strings to capture the visual elements that make this moment stand out. Next, you had to build the video salient moments schema, which is the top level structure. This contains a video summary for a brief overview, total moments found as an integer count. Then the critical part, you had to define the moments field as a list of salient moment objects. This creates the nested structure where each video analysis contains multiple individual moments. The schema also includes a most significant moment field to optionally highlight the single, most important timestamp, and a pacing analysis field to describe how these moments are distributed throughout the video. With our schemes defined, we now set up the agent that will analyze the videos. We start by creating model settings that disable the thinking feature to avoid time outs. Then you had to configure the agent itself. You needed to set the model to GMII 2.5 flashlight, which is optimized for multi modal analysis. Critically, you had to set the output type to video salient moments. This connects the agent to the schema you built, ensuring the model returns, structured data in exactly the format we expect. You also had to write the instructions that guide the model's behavior. The instructions tell the model to act as an expert video analyst, focusing on identifying key moments that capture viewer attention, represent turning points, show pak action, or emotion, and have strong visual impact. These instructions shape how the model interprets what makes a moment salient. Finally, you had to pass in the model settings. We define a helper function that reads the video file and wraps it in a binary content object for pedantic AI. Now we see everything in action. We load the video using our helper function, then call the agents run sync method, passing it a text prompt and the video content. The agent processes the video through Gemini, applies our schemas, and returns a structured video salient moments object. Let's look at the video first. The results show exactly what we designed. A summary describing motocross riders on a dirt track, account of three salient moments, and detailed information about each moment, including timestamps, classifications, descriptions, and visual cues. The model identified an action peak at two seconds showing a jump, another action peak at three seconds with a sharp turn, and a scene change at five seconds where the camera pans to show the full track. It also identified the jump as the most significant moment and provided an analysis of how these moments are distributed throughout the video. This approach makes it easy to build automated video editing tools. You could analyze hours of footage, identify the best moments, and cut them into highlight reels. The combination of Geminize video understanding with Pideanic structured output gives you categorized time stamped data that's immediately usable in your code. This concludes our demo for today, thanks for watching.