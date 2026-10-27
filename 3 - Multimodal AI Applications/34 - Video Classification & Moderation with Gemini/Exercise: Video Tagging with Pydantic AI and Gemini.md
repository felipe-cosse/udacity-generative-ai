In this hands-on exercise, you will build a structured tagging pipeline for short MP4 clips using Pydantic AI with Gemini 2.5 Flash Lite. The task simulates labeling a small collection of clips to support planning for a robotic hand learning basic object manipulations. Labels include a detailed description, a quality rating, actions, and objects present (e.g., candle, container, cotton swabs, basket, box, tape, board game, mug, jar, slipper, scarf, smartphone, pen). This mirrors real-world workflows used by QA and applied AI teams to pre-label datasets for downstream evaluation.

Prerequisites:
Classroom workspace with Python 3.12+ and JupyterLab (or local environment)
Packages: pydantic-ai with Google extras, python-dotenv, nest_asyncio, IPython
Gemini API access and a valid API key set in .env as GEMINI_API_KEY
Objectives:
By the end of this exercise, be able to:

Design a Pydantic model with Literal constraints for consistent tagging
Configure a Pydantic AI Agent for Gemini 2.5 Flash Lite with deterministic settings
Load MP4 content as BinaryContent and run structured analysis at scale across a directory
Steps:
Prepare workspace and credentials
To use the Udacity workspace:
Click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l4/exercises/3-video-tagging/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the environment named the same as this activity’s directory.
Create a .env file from the example:
cp env.example .env
Edit .env and set GEMINI_API_KEY=<your_key>.
Install and verify dependencies
In a terminal or notebook cell:
pip install "pydantic-ai[google]" python-dotenv nest_asyncio ipython
Restart the kernel if needed.
Confirm imports: pydantic, pydantic_ai, dotenv, nest_asyncio, IPython.display.
Understand the tagging schema requirements
Required fields in the Pydantic model:
description: str (detailed summary of what happens in the clip)
quality: Literal["poor", "ok", "good"]
actions: List[Literal["move sideways", "move vertically", "put object 1 into object 2", "pull object 1 out of object 2"]]
objects_involved_in_the_action: int
objects_present: List[Literal["candle", "container", "cotton swabs", "basket", "box", "tape", "board game", "mug", "jar", "slipper", "container", "scarf", "smartphone", "pen"]]
Add Field descriptions to guide the model.
Implement the Pydantic schema (complete the TODOs)
Set quality to Literal["poor", "ok", "good"] with a Field description.
Set actions to List[Literal[...]] using the four allowed actions.
Keep objects_involved_in_the_action as int with a clear description.
Verify objects_present uses the provided Literal options list.
Configure deterministic Gemini settings
Use GoogleModelSettings with:
google_thinking_config={"thinking_budget": 0}
temperature=0
seed=42
This reduces randomness and speeds up responses for labeling.
Create the Agent (complete the TODO)
Instantiate Agent with:
model="gemini-2.5-flash-lite"
model_settings=settings
output_type=VideoTagging
instructions: concise guidance, for example:
"Analyze the MP4 and produce JSON matching the schema. Use only allowed actions and objects. Keep descriptions specific and factual. Rate quality as poor, ok, or good."
retries=5 (to mitigate transient failures)
Confirm no additional thinking or tool calls are required.
Prepare media loading
Use the provided helper load_video_for_analysis to read bytes and wrap as BinaryContent with media_type="video/mp4".
Note: For longer content, consider the File API pattern to avoid payload limits.
Run analysis over the dataset
Iterate over ../videos/*.mp4 and display each clip in the notebook (already scaffolded).
For each clip, call the agent with a prompt and the BinaryContent, for example:
result = video_agent.run_sync(["Provide a structured tagging summary for this clip.", video_content])
Print structured output via result.output.model_dump().
Validate and refine outputs
Check that:
quality is one of the allowed values
actions only use the four allowed labels
objects_present only includes allowed objects
objects_involved_in_the_action is a reasonable integer
If the model drifts:
Strengthen instructions (e.g., "Do not invent new labels")
Add few-shot examples if needed
Keep temperature=0 for consistency
Optional enhancements
Add a post-processing check that raises an error if any field violates the schema.
Extend actions or objects lists and test schema evolution.
Log outputs to a JSONL file for downstream QA review.
For longer or many clips, switch to the File API and add exponential backoff on rate limits.