In this hands-on exercise, you will build a voice-command recognizer for a robot control system using Pydantic AI with Google Gemini. Audio samples from the workspace will be converted to structured commands that a robot can safely use. This mirrors common industry workflows in robotics, voice assistants, and warehouse automation where reliable command parsing is essential.

Prerequisites:
Google Gemini API key set in ../.env (environment variable GEMINI_API_KEY)
Python 3.12+ with packages: pydantic, pydantic-ai, python-dotenv, numpy, librosa, soundfile, IPython, nest_asyncio
Internet access to call the Gemini model
If running locally: system libsndfile installed (e.g., macOS: brew install libsndfile; Debian/Ubuntu: sudo apt-get install libsndfile1)
Objectives:
By the end of this exercise, you will be able to:

Define a strict Pydantic schema for command recognition with Literal constraints
Convert audio to bytes and package as BinaryContent for multimodal inputs
Run single and batch recognition, and interpret structured outputs for robotic control
Steps:
Prepare environment and credentials
To use the Udacity workspace:
In the navigation pane on the left (below the table of contents), click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/exercises/3-robot-commands/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Copy environment file: cp ../env.example ../.env
Edit ../.env and set GEMINI_API_KEY
Review imports and helpers
Confirm imports for Agent, BinaryContent, librosa, soundfile, and dotenv
Note the helper functions:
audio_to_bytes: converts a numpy array to WAV bytes
format_audio_for_gemini: loads an MP3, converts to mono, and returns (audio_array, sample_rate, BinaryContent)
Define the RobotCommand schema (fill TODOs)
action: use Literal with allowed values:
"move_forward", "move_backward", "turn_left", "turn_right", "pick_up", "put_down", "stop", "unknown"
target_object: Optional[str], description provided
rationale: str with a short explanation of how the action was inferred
Validation goal: any unrecognized or ambiguous command should map to "unknown" with a clear rationale
Create the command recognition Agent (fill TODO)
Use model "gemini-2.5-flash-lite"
Use GoogleModelSettings with google_thinking_config={"thinking_budget": 0}
Provide concise instructions in the prompt, for example:
Transcribe the audio if needed
Map to exactly one action from the allowed set or "unknown"
Extract a simple object noun if present (e.g., "box", "tool")
Keep rationale brief and specific
Avoid adding fields not in the schema
Set output_type=RobotCommand and pass model_settings=settings
Load the sample dataset
Run the cell that lists ../samples/*.mp3
Confirm a non-empty list; if empty, verify path and workspace sync
Single-audio command recognition
Use format_audio_for_gemini(samples[0]) to get audio_array, sample_rate, and audio_content
Display playback with Audio(audio_array, rate=sample_rate) to hear the sample
Run the agent synchronously:
command_agent.run_sync([short analysis instruction string, audio_content])
Print result.output.action, result.output.target_object, result.output.rationale
Acceptance: action is one of the allowed values; rationale references words heard or lack of clarity
Batch command analysis
Loop over each sample path
Call format_audio_for_gemini(sample_path)
Optional: play each sample to correlate output and audio
For each, run command_agent.run_sync([instruction string, audio_content])
Print fields in a consistent format; ensure no exceptions occur
Acceptance: no crashes across files, reasonable mapping to "unknown" when unclear
Quality checks and adjustments
If false positives occur, make instructions stricter:
Require "unknown" when confidence is low or when no action verb matches
Ask for the simplest possible target_object (single noun) or None
If outputs are verbose, instruct the agent to keep rationale under one sentence
Optional enhancements (stretch)
Add a confidence: float field (0–1) to RobotCommand and prompt for a calibrated estimate
Add synonyms in the prompt mapping, e.g., "forward/go ahead" => move_forward
Log results to JSON for later evaluation
