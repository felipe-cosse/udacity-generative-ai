This walkthrough explains how the solution detects personal information in audio recordings with a structured, reproducible process. The exercise demonstrates how to convert audio to a transcript, analyze it for sensitive data, return structured findings, and produce risk ratings with recommendations. The main premise: turn unstructured audio into actionable, compliant insights.

What this solution teaches
How to structure policy violations with Pydantic models.
How to prepare audio for multimodal analysis.
How to configure a PydanticAI agent for transcription and detection.
How to return violations, risk level, and recommendations in a predictable schema.

The solution builds a lightweight audio moderation system for detecting personal information in speech. It uses:

librosa and soundfile to load and convert audio.
pydantic and pydantic_ai to define and enforce the output schema.
Gemini model gemini-2.5-flash-lite for transcription and analysis.
Step-by-step instructions
Install and configure
To use the Udacity workspace:
In the navigation pane on the left (below the table of contents), click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/exercises/4-moderation/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Create .env with GEMINI_API_KEY.
Load with load_dotenv and validate presence of the key.
Define policy schema
Create ViolationType enum with categories.
Implement PolicyViolation with violation_type, detected_text, context, and optional timestamp_start.
Implement ModerationResult with transcript, violations_found, risk_level, recommendations.
Prepare audio utilities
Load audio with librosa.load (mono, original sample rate).
Convert to WAV bytes using soundfile.
Wrap in BinaryContent(media_type='audio/wav').
Configure the agent
Use model gemini-2.5-flash-lite.
Set output_type=ModerationResult to enforce structure.
Provide a precise system prompt emphasizing context and avoiding false positives.
Build request content
Combine an instruction string and audio_content in message_content.
Execute and collect results
Call moderation_agent.run_sync(message_content).
Access result.output.transcript, result.output.violations_found, result.output.risk_level, result.output.recommendations.
Display and act
Present detected violations with type, text, and context.
Use risk_level to prioritize responses.
Apply recommendations to guide remediation (e.g., redact, retrain staff, use secure channels).
Code Snippets
Data models
Two schema layers are used: the violation structure and the overall result. ViolationType standardizes categories, and PolicyViolation captures each finding with optional timing and context.

from typing import List, Optional, Literal
from enum import Enum
from pydantic import BaseModel, Field

class ViolationType(str, Enum):
    PHONE_NUMBER = "phone_number"
    EMAIL_ADDRESS = "email_address"
    SSN = "social_security_number"
    ADDRESS = "physical_address"
    CREDIT_CARD = "credit_card_number"
    DATE_OF_BIRTH = "date_of_birth"

class PolicyViolation(BaseModel):
    violation_type: ViolationType
    detected_text: str
    timestamp_start: Optional[float] = None
    context: str = Field(description="Surrounding context where violation was detected")

class ModerationResult(BaseModel):
    transcript: str = Field(
        description="Full transcript of the audio. If multiple speakers are talking, include speaker labels."
    )
    violations_found: List[PolicyViolation]
    risk_level: Literal["LOW", "MEDIUM", "HIGH"] = Field(
        description="LOW, MEDIUM, or HIGH based on violations"
    )
    recommendations: List[str]
Audio preparation
Audio is loaded, converted to WAV bytes, and wrapped as BinaryContent for the agent.

import io, librosa, soundfile as sf
from pydantic_ai import BinaryContent

def audio_to_bytes(audio_array, sample_rate):
    buffer = io.BytesIO()
    sf.write(buffer, audio_array, sample_rate, format='WAV')
    buffer.seek(0)
    return buffer.getvalue()

def format_audio_for_gemini(file_path):
    audio_array, sample_rate = librosa.load(file_path, sr=None, mono=True)
    audio_bytes = audio_to_bytes(audio_array, sample_rate)
    return audio_array, sample_rate, BinaryContent(data=audio_bytes, media_type='audio/wav')
Agent configuration
The agent enforces the output schema and guides the model with a focused system prompt that covers transcription, detection, and risk assessment.

from pydantic_ai import Agent

moderation_agent = Agent(
    'gemini-2.5-flash-lite',
    output_type=ModerationResult,
    system_prompt="""
    You are an audio moderation system designed to detect personal information in recordings.
    Your task is to:
    1. Transcribe the provided audio accurately
    2. Analyze the transcript for personal information violations
    3. Flag any instances of: phone numbers, email addresses, SSN, physical addresses, credit card numbers, dates of birth
    4. Assess the overall risk level and provide recommendations
    Be thorough but avoid false positives. Consider context when determining if something is truly personal information.
    """
)
Running the detection
A short instructional message plus the audio content are sent together. The agent returns a ModerationResult.

audio_array, sample_rate, audio_content = format_audio_for_gemini("../audio_moderation.mp3")

message_content = [
    "Please transcribe this audio and analyze it for personal information disclosure according to the system prompt.",
    audio_content,
]

result = moderation_agent.run_sync(message_content)
The result includes:

transcript: full text with optional speaker labels.
violations_found: array of PolicyViolation objects.
risk_level: "LOW", "MEDIUM", or "HIGH".
recommendations: actions to mitigate exposure.
Remember:

Structured outputs with PydanticAI make moderation reliable: schema-first design reduces ambiguity.
Context-aware detection is essential to balance thorough scanning and avoidance of false positives.








This exercise, we're building a mock audio moderation system that can process audio recordings and flag any personal information disclosures. The system uses Gemini for transcription and analysis and pedantic to structure the output. Let's imagine we have a policy in our company that prevents customer service representatives to exchange customer private information over unsecured channels. The system we are building today enforces this policy. We start by importing the necessary libraries, in particular, sound file for audio input and output, dotenv for loading credentials, and the core classes from pedantic and pedantic AI. We load our environment variables from a.env file and check that the Gemini API Key is available. Next, we define the data schema and policy definitions. We use Python's om to list all possible violation types, such as phone numbers, email addresses, SSNs, physical addresses, credit card numbers, and dates of birth. The policy violation model captures details about each violation, including the type, detected text, timestamp, and context. You then had to create the moderation result pidantic model, which serves as the output schema for our moderation agent. This schema includes the transcript, a list of violations found, a risk level, and a list of recommendations. In particular, you had to use a list of policy violation instances for the violations found element. Risk level is instead a classification, so you had to use a literal with the required classes. Note also that I added a specific instruction for the transcript, telling the model to indicate the different speakers if a dialogue contains multiple people. Moving on, we set up some audio processing utilities. The audio to bytes function converts an audio array into bytes. Format audio for Gemini function loads an audio file, converts it to bytes, and wraps it in a binary content object with the audio wave media type ready for analysis. Next, you had to initialize the pedantic AI agent with Gemini, specifying the output schema and a detailed system prompt. The agent uses the Gemini 2.5 flashlight model. The system prompt instructs the model to transcribe the audio, analyze the transcript for personal information, flag any violations, assess the overall risk level, and provide recommendations. For the demonstration, we load a sample audio file. It contains a conversation between two customer agents. You then had to prepare the audio for the API by calling format audio for Gemini and collecting the audio array sample rate and audio content. Next, you created a message containing a prompt and the audio itself, which is sent to the moderation agent. The agent processes the message and returns a result. We print the obtained transcription, risk level, and the number of violations found. As you can see from the transcript, the audio file contains a conversation between two agents. They are talking about a customer, and they exchange some information that, according to our internal policy, should not be exchanged in an unsecured communication. Our system detects all violations, reports them, and provide suggestions for things to do next. This concludes our exercise for today. Congratulations for reaching this point, and see you next time.