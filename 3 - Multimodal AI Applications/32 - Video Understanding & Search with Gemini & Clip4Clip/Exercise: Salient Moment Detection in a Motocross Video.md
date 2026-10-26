In this hands-on exercise, you will build a small system that detects salient moments in motocross footage using Pydantic AI with Google Gemini. The task mirrors common industry workflows such as sports highlight creation, automatic thumbnail selection, and chaptering for long-form content.

Prerequisites
Python 3.9+ environment (local or classroom workspace)
Google Gemini API key (store in .env as GEMINI_API_KEY)
Packages:
pydantic-ai, google-generativeai
pydantic, python-dotenv
typing_extensions, nest_asyncio
ipython, jupyter (if using notebooks)
Objectives
By the end of this exercise, you will be able to:

Define nested Pydantic models to structure salient-moment outputs
Configure a Gemini-backed agent in Pydantic AI for media understanding
Load an MP4 file as binary content and request structured analysis
Interpret model results and relate them to editing or analytics needs
Steps
Prepare the workspace
To use the Udacity workspace:
Click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l4/exercises/2-salient-moments/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the environment named the same as this activity’s directory.
Copy and edit environment file:
cp env.example .env
Set GEMINI_API_KEY=... in .env.
Load environment and verify credentials
Run the provided import cell and load_dotenv() call.
Confirm the assertions pass:
.env loads successfully.
GEMINI_API_KEY is present.
If an assertion fails, check the file path, spelling of the variable, and shell environment.
Complete the Pydantic schemas
In SalientMoment, add fields:
timestamp: str
moment_type: Literal["action_peak",...]
description: str
visual_cues: List[str]
In VideoSalientMoments, make moments a List[SalientMoment] with a Field(...) description such as “List of detected salient moments in chronological order.”
Keep most_significant_moment: Optional[str] and pacing_analysis: str as given.
Configure the Gemini model and agent
Use GoogleModelSettings with google_thinking_config={"thinking_budget": 0} as shown.
Create the agent:
model="gemini-2.5-flash-lite"
output_type=VideoSalientMoments (the schema defined above)
instructions are provided; reuse or lightly adjust for motocross emphasis
model_settings=settings
This configuration ensures structured output aligned with the schema.
Prepare the helper for media loading
Use the load_video_for_moments_analysis function as provided.
Confirm media_type='video/mp4' (works for .mp4 content).
This returns a BinaryContent object ready for the agent.
Load the motocross file
Ensure the sample file exists at ../cross.mp4 from the notebook’s working directory.
Adjust the path if needed (e.g., ./data/cross.mp4).
Optional: display the clip with IPython.display.Video to visually confirm it loads.
Run salient-moment detection
Call moments_agent.run_sync.
Pretty-print the result with pprint(result.output.model_dump()).
Expect a dictionary containing:
video_summary (short synopsis)
total_moments_found (count)
moments (list of SalientMoment objects)
most_significant_moment (optional timestamp)
pacing_analysis (distribution overview)
Interpret and use the results
Check that timestamps match notable motocross actions (jumps, landings, overtakes, crashes).
Review moment_type values for variety across action and transitions.
Use visual_cues to guide thumbnail selection or overlay graphics.
For highlight creation, select top moments by category or description and gather their timestamps.
Optional enhancements
Adjust instructions to bias toward “action_peak” or “visual_transition.”
Enforce a timestamp format convention (e.g., MM:SS).
Export the result to JSON for a downstream editing pipeline.
Add a confidence-like proxy by requesting stricter criteria in the instructions.
