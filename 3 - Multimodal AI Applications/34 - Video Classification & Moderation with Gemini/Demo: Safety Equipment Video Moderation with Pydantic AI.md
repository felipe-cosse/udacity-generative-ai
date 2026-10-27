This demo builds an automated safety compliance checker for workplace footage using Pydantic AI and Gemini. The system scans construction or factory recordings to determine if personnel wear required protective gear (hard hats and masks). It produces structured compliance reports with timestamps and triggers alerts when issues are detected.

Real-world uses: safety teams can automatically review uploaded clips, generate incident logs, and route alerts to supervisors without manual review. The workflow combines multimodal analysis, typed outputs, and lightweight automation that can be embedded into existing safety pipelines.

Process Summary
Load environment variables and enable async in notebooks
Define a strict policy schema with Pydantic (SafetyViolation and SafetyModerationResult)
Configure a Gemini-backed Agent with deterministic settings and clear instructions
Load MP4 content as BinaryContent and run analysis
Parse the structured result, print a report, and send alerts for each issue
Step-by-Step Instructions
1) Environment Preparation
To use the Udacity workspace:
Click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l4/demos/4-moderation-with-gemini/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the environment named the same as this activity’s directory.
Copy example environment file and set credentials:
cp env.example .env
Edit .env and set GEMINI_API_KEY
Notebook setup uses:
dotenv to load the API key
nest_asyncio to support async in notebooks
2) Define the Safety Policy Schema
Create structured outputs to enforce consistent parsing and automation
Include typed fields, timestamps, and policy categories
Core snippet:

from pydantic import BaseModel, Field
from typing import List
from typing_extensions import Literal

class SafetyViolation(BaseModel):
    violation_type: Literal["missing_hard_hat", "missing_mask"] = Field(
        description="Type of safety equipment violation detected"
    )
    timestamp_start: float = Field(
        description="Start time in seconds when violation begins"
    )
    timestamp_end: float = Field(
        description="End time in seconds when violation ends"
    )

class SafetyModerationResult(BaseModel):
    overall_compliance: Literal["compliant", "violations_detected"] = Field(
        description="Overall safety compliance status"
    )
    violations: List[SafetyViolation] = Field(
        description="List of all safety violations detected"
    )
    summary: str = Field(
        description="Brief summary of safety compliance findings"
    )
3) Configure the Agent (Gemini + Pydantic AI)
Use a deterministic configuration for repeatable outcomes
Set output_type to the schema for structured responses
Provide clear policy instructions and required equipment list
Core snippet:

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModelSettings

settings = GoogleModelSettings(
    google_thinking_config={"thinking_budget": 0},
    seed=42,
    temperature=0.0
)

safety_agent = Agent(
    model="gemini-2.5-flash-lite",
    output_type=SafetyModerationResult,
    instructions="""
    You are a workplace safety compliance system. Analyze the provided video to detect 
    violations of safety equipment policy.
    REQUIRED SAFETY EQUIPMENT:
    - Hard hats (helmets) must be worn by all personnel
    - Masks must be worn by all personnel
    Your tasks:
    1. Identify all people visible in the video
    2. Check if each person is wearing required safety equipment
    3. For every violation, fill out a SafetyViolation entry with type and timestamps
    4. Determine overall compliance ("compliant" or "violations_detected")
    5. Provide a brief summary of findings
    Be precise with timestamps and focus only on clearly visible violations.
    """,
    model_settings=settings,
    retries=3,
)
4) Prepare Helpers for Media Loading and Alerts
Load MP4 content and wrap it as BinaryContent for analysis
Simulate alert notifications to a safety team
Core snippet:

from pydantic_ai import BinaryContent

def load_video_for_analysis(video_path):
    with open(video_path, 'rb') as f:
        video_bytes = f.read()
    return BinaryContent(data=video_bytes, media_type='video/mp4')

def alert_safety_official(violation: str):
    print(f"🚨 SAFETY ALERT SENT: {violation}")
    print(f"   → Notification sent to safety@company.com")
    print(f"   → Incident logged in safety management system")
    print(f"   → Supervisor notified for immediate action\n")
5) Run the Analysis
Iterate over local MP4 files
Submit the binary content with a short instruction message
Print the structured result
Core snippet:

from pprint import pprint

for media_file in ["construction1.mp4", "construction2.mp4"]:
    media_content = load_video_for_analysis(media_file)
    result = safety_agent.run_sync(
        ["Analyze this video for workplace safety equipment compliance.", media_content]
    )
    safety_result = result.output
    pprint(safety_result.model_dump())
6) Process Issues and Send Alerts
If any issues are present, print details and send notifications
Otherwise, confirm compliance
Core snippet:

if safety_result.violations:
    for v in safety_result.violations:
        alert_message = (
            f"{v.violation_type.replace('_', ' ').title()} "
            f"from {v.timestamp_start}s to {v.timestamp_end}s."
        )
        alert_safety_official(alert_message)
else:
    print("No safety violations detected.")
Takeaways
Multimodal analysis can spot missing protective gear in real workplace footage
Alerts provide immediate, actionable feedback to safety teams
The approach scales from notebooks to production backends with minimal changes







In next few minutes, we're going to learn how to build an automated workplace safety compliance system using Pydantic AI and the Gemini model from Google. This system will watch videos of construction workers and automatically detect if they're missing required safety equipment like hard heads or masks. Let's see how it's done. We begin by importing all the libraries we need. We're bringing in the dotenv library to load our API credentials from an environment file, which is always a good practice for keeping secrets secure. We also import Pydantic for data validation and Pydantic AI for building our agent. The binary content class is particularly important here because it's how we'll pass video data to our AI model. We also use nest_asyncio to make the code work smoothly inside Jupiter notebooks, since Jupiter has its own event loop that can conflict with the way we are using Pydantic AI. After importing, we load our environment variables using load_dotenv, and check that the Gemini API key is present. Without this key, we won't be able to call the model. Now that we have our environment set up, let's define the structure of our safety compliance data. We're using Pydantic models here, which is really powerful because it gives us type safe validated data structures. First, we define a safety violation model. This represents a single violation, like someone not wearing a hard hat. Each violation has three fields, the violation type, which we restrict using literal to only allow missing hard hat or missing mask, and two times stem fields for when the violation starts and ends. The field function, lets us add descriptions that actually get passed to the AI model to help it understand what we want. Next, we create a safety moderation result model that wraps everything together. This includes an overall compliance status, either compliant or violations detected, a list of all the violations found and a text summary. The beauty of using Pydantic AI is that it will automatically structure the model's response to match the exact schema, giving us consistent parsable results every time. Now let's create our actual AI agent. We start by configuring the model settings. We're setting the thinking budget to zero to avoid delays, using a seed of 42 for reproducibility and temperature to zero for more deterministic results. Then we initialize the agent itself. We specify Gemini 2.5 flashlight as our model, which is fast and cost effective for video analysis. We set our output type to safety moderation result. Pydantic AI knows to structure all responses according to that scheme we just defined. Then let's look at the prompt. This is where we tell the AI exactly what to do. We define the required safety equipment. Hard hats and masks must be worn by all personnel. Then we give it a clear step by step process. Identify all people in the video, check their safety equipment, record violations with precise timestamps, determine overall compliance, and provide a summary. We emphasize being precise with time stamps and only flagging clearly visible violations. We also set it to try three times if there's a temporary API failure. With our agent configured, let's define some helper functions. First, we need a function to load video files. We open the video file in binary mode, read all the bytes, and wrap them in a binary content object with the media type set to Video mp4. This format is what Pydantic AI expects when passing multimedia content to the model. We also create a Moc function called alert safety official. In a real system, this would send actual notifications to supervisors or log incidents in a database. Here, it just prints alerts to show how the workflow would operate. Now, for the exciting part, let's actually analyze some videos. We're going to process two different construction videos to see our system in action. For each video, we first display it so we can see what we're analyzing. Then we load the video content using our helper function. We call the agents run sync method, passing in a text prompt, asking it to analyze for safety compliance, along with the video content itself. The use of this run sync method is the reason why we needed nest_asyncio at the beginning. Another approach would be to use the Async pattern of using Pydantic AI, but that goes beyond the scope here. The model then processes the entire video frame by frame, looking for people and checking their safety equipment. When we run this on our first video, we see that everyone is compliant. The model returns no violations and confirms that all personnel were wearing the required hard hats and masks throughout the video. But when we analyze the second video, the system detects violations. The worker in this video is not wearing either a hard hat or a mask during demolition work. The model correctly identifies both violations and times starts them from the beginning to the end of the video clip. Finally, we give a mock example of how we would process these violations to take action. If any violations were detected, we loop through each one, format the details nicely, and call our alert function. In production, this is where you'd send e mails, create tickets in your safety management system, or even trigger real time alerts to supervisors on the worksite. This concludes our demo for today. Thanks for watching.