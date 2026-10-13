In this walkthrough, we demonstrate a small but complete audio command recognizer that converts short spoken commands into structured, machine-ready outputs. The exercise demonstrates how to:

Structure outputs with Pydantic for predictable parsing.
Use Gemini via Pydantic AI for speech understanding.
Prepare raw audio for multimodal input and handle both single and batch processing.

Solution Overview
Environment setup with a Gemini API key.
Definition of a strict RobotCommand schema using Pydantic.
Construction of a Pydantic AI Agent wrapping Gemini, configured for fast, concise outputs.
Audio preprocessing with librosa and soundfile, then packaging as BinaryContent.
Inference on a single file and iterating over multiple samples.
Structured results containing action, optional target_object, and a brief rationale.
Step-by-Step Instructions
Prepare environment
To use the Udacity workspace:
In the navigation pane on the left (below the table of contents), click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/exercises/3-robot-commands/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Copy and edit the env file:
cp ../env.example ../.env
Set GEMINI_API_KEY in ../.env.
Load environment and enable asyncio in notebooks
Code already includes:
assert load_dotenv("../.env")
assert os.getenv("GEMINI_API_KEY")
import nest_asyncio; nest_asyncio.apply()
Define the command schema
Use the RobotCommand model to enforce valid actions and include target_object and rationale.
Configure the agent
Set model="gemini-2.5-flash-lite"
Use output_type=RobotCommand to force structured responses.
Keep thinking_budget small for faster runs.
Prepare audio samples
Place .mp3 files in ../samples.
Use format_audio_for_gemini to convert each file to BinaryContent('audio/wav').
Run single-file recognition
Select a sample, display it for playback (optional), and call:
command_agent.run_sync(["Analyze this audio for robot commands.", audio_content])
Run batch recognition
Iterate over samples, format each audio, and call the agent to collect consistent structured results.
Interpret results
action: one of the eight allowed labels or unknown.
target_object: filled for object-related instructions, otherwise None.
rationale: short explanation validating the decision.
Core schema and agent configuration
The schema enforces a constrained action set and adds clarity with a rationale:

class RobotCommand(BaseModel):
    action: Literal[
        "move_forward", "move_backward", "turn_left", "turn_right",
        "pick_up", "put_down", "stop", "unknown"
    ] = Field(description="The recognized robot action command")
    target_object: Optional[str] = Field(default=None, description="Object mentioned in the command, if any")
    rationale: str = Field(description="Brief explanation of why this command was recognized")
The agent binds Gemini to that schema and reduces thinking overhead for responsiveness:

settings = GoogleModelSettings(google_thinking_config={"thinking_budget": 0})

command_agent = Agent(
    model="gemini-2.5-flash-lite",
    output_type=RobotCommand,
    instructions="""
    You are a robot command recognition system. Listen to the audio and identify:
    1. The primary action command (movement, manipulation, or control)
    2. Any objects if the action involves manipulating an object, otherwise leave empty
    3. A rationale for your decision

    Commands include:
    - Movement
    - Manipulation
    - Control

    Remember that clockwise means towards the right, and counterclockwise means towards the left.

    If the audio or the command is unclear or not a robot command, use "unknown" action.
    Be precise and focus on actionable commands.
    """,
    model_settings=settings,
)
Audio preparation for multimodal input
Load audio, resample consistently, and wrap bytes for Gemini:

def audio_to_bytes(audio_array, sample_rate):
    buffer = io.BytesIO()
    sf.write(buffer, audio_array, sample_rate, format='WAV')
    buffer.seek(0)
    return buffer.getvalue()

def format_audio_for_gemini(file_path: Path):
    audio_array, sample_rate = librosa.load(file_path, sr=None, mono=True)
    audio_bytes = audio_to_bytes(audio_array, sample_rate)
    audio_content = BinaryContent(data=audio_bytes, media_type='audio/wav')
    return audio_array, sample_rate, audio_content
Running inference
Single sample:

result = command_agent.run_sync(
    ["Analyze this audio for robot commands.", audio_content]
)
print(result.output.action, result.output.target_object, result.output.rationale)
Multiple samples:

for sample_path in samples:
    _, _, audio_content = format_audio_for_gemini(sample_path)
    result = command_agent.run_sync(["Analyze this audio for robot commands.", audio_content])
Remember
This solution applies a typed LLM workflow to audio commands:

Strict Pydantic schema guarantees predictable, safe robot actions.
Gemini processes speech via BinaryContent and returns validated outputs.
The same pattern supports single and batch runs with minimal code changes.







This exercise, you learned how to build an audio command recognition system for a robot using pedantic AI and Google Gemini. The idea is to use the model to translate a free-form command from the user to an exact command that the robot understands. This makes for a much more natural interaction between the robot and the user because the user does not need to stick to exact terms and commands to control the robot. Let's walk through the solution step by step. We started by importing all the necessary libraries. In particular, we import a dot and V to load the API key for Gemini from the.env file, and then a few classes from Pedantic and Pedantic AI. We also load sound file to be able to load samples, as well as the audio class to be able to listen to the audio samples here in the notebook. The environment variables were loaded from a.env file, and we made sure the Gemini API key was present. To enable asynchronous code execution in Jupyter, we applied nest-asyncio. This is necessary to use pidantic AI in Jupyter in a non-asynchronous way. Next, you defined the schema for the robot command output. Using pidantic base model, you created a model with three fields. Action, which is a restricted set of valid robot commands, target object, and optional string for any object mentioned in the command. Rationale, a string explaining the reasoning behind the recognized command. For the action, you used literal to specify exactly the allowed values for this field. In this case, this included all the available commands for our robot. After that, you set up the agent for command recognition. We imported the model settings class and configured it to avoid thinking in order to avoid unnecessary delays. You then created the agent with the Gemini model, the output type set to your robot command schema, and a detailed prompt instructing the model to listen to audio and identify the command, any object involved and the rationale. In my experiment, I also found that I had to clarify the meaning of directional terms like clockwise and counterclockwise, and how to handle unclear audio. This is the kind of fixes that you need to do at the prompt engineering step. Moving on, we then load some audio samples for testing. We also provide two helper functions. One to convert an audio array to bytes, and the other one to format an audio file, so Gemini can understand it. Let's look at the second helper function more closely. First, we load the file using Librosa. We specifically force the audio to be loaded with only one channel because we have no need for stereo data for this application. We then convert it to a bytes string using the other helper function. Finally, we create a binary content instance with the data we just created, and we set the media type to Audio Wave. This is how you pass audio to Gemini inline. Now to the fun part to test single command recognition, we format the first file and display the audio so we can play it later. Then you run the agent to analyze the audio. Let's listen to the command. Grab the blue bottle from the table. The audio file does not contain a command expressed in exactly the way that the robot understands. However, Gemini can recognize that the user is asking to perform the pick up action and apply it to a bottle as target object. It works. We are now ready to apply this to all samples. For each audio file, you formatted the audio and ran the agent. We then display the audio and print the results. Let's hear the samples, skipping the first one, which we processed in the cell above. Make a left turn here. The woman is asking to make a left, which is recognized by Gemini. Place the metal tool on the shelf. Another woman is asking the robot to put down a metal tool, again, recognized correctly. Back up a little bit. The user, this time is asking the robot to back up, which Gemini correctly translates to the move backward command. Rotate clockwise now. Here's a tricky one. The user is asking the robot to rotate clockwise. Gemini originally did not understand this command reliably. But with a little bit of prompt engineering, I was able to make it work. Now it does recognize that this means to rotate right. Let's listen to one more, which is actually an audio that does not contain any command. This coffee tastes quite bitter. The model understands that there is no command here, and so it correctly answers with unknown. Perfect. Congratulations in completing this exercise, and see you at the next.