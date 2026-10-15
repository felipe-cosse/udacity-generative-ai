Exercise Name
In this hands-on exercise, you will build an audio moderation workflow that detects and flags personal information disclosed in recorded calls. Using Gemini with PydanticAI for structured outputs, this exercise connects policy rules to real analysis results. The included sample file and a mock company policy (no customer information shared over unsecured calls) anchor the task in common contact-center and compliance use cases.

Prerequisites
Classroom workspace (recommended) or local Python 3.12+
Packages: pydantic, pydantic-ai, python-dotenv, librosa, soundfile, nest_asyncio
Gemini API key in a .env file at the project root with GEMINI_API_KEY=...
In classroom workspace, the key may already be provisioned
Sample audio file available at ../audio_moderation.mp3
Objectives
By the end of this exercise, you will be able to:

Define a Pydantic output schema (ModerationResult) for structured moderation results
Configure a PydanticAI Agent with a system prompt to transcribe and detect personal information
Prepare audio for multimodal input, run the analysis, and interpret transcript, violations, risk level, and recommendations
Steps
Open the notebook and verify the environment
To use the Udacity workspace:
In the navigation pane on the left (below the table of contents), click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l3/exercises/4-moderation/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
API key setup
copy example.env to .env
set GEMINI_API_KEY
Configure credentials
Classroom: skip if assertions pass.
Local: create a .env file in the project root with line: GEMINI_API_KEY=YOUR_KEY
Re-run the setup cell to confirm the environment variable is detected.
Review policy and violation types
Examine ViolationType and PolicyViolation classes:
Supported types: phone_number, email_address, social_security_number, physical_address, credit_card_number, date_of_birth.
Note the context field in PolicyViolation, used to capture surrounding transcript text.
Implement ModerationResult (complete the TODO)
Replace the placeholder with a Pydantic model containing:
transcript: str
violations_found: List[PolicyViolation]
risk_level: str (use LOW, MEDIUM, HIGH)
recommendations: List[str]
Save and re-run to ensure no import/type errors.
Initialize the PydanticAI Agent (complete the TODO)
Create moderation_agent with:
model="gemini-2.5-flash-lite"
result_type=ModerationResult
system_prompt covering:
Transcribe the audio.
Analyze transcript for policy violations.
Flag phone numbers, email addresses, SSN, physical addresses, credit card numbers, and dates of birth.
Assess overall risk level and provide actionable recommendations.
Suggested risk guidance in the prompt:
HIGH: SSN or credit card present, or multiple different personal identifiers.
MEDIUM: single sensitive item (e.g., phone number, email, address, DOB) with business context.
LOW: no violations or false positives with low confidence.
Prepare the sample audio (complete the TODO)
Ensure ../audio_moderation.mp3 exists. Adjust the path if needed.
Call format_audio_for_gemini(sample_file) and capture audio_array, sample_rate, audio_content.
If librosa fails to load MP3, install ffmpeg or use a WAV file; otherwise switch the sample to a WAV file and update sample_file accordingly.
Create the multimodal message content (complete the TODO)
Build a list with:
A short instruction string, e.g., "Transcribe and analyze this audio for personal information per policy."
The audio_content object returned above.
Run the agent and review results
Execute result = moderation_agent.run_sync(message_content).
Inspect console output:
Transcript: check for accuracy and completeness.
Risk Level: verify it matches the prompt guidance.
Violations Found: count and types (phone number, email, etc.).
Recommendations: confirm practical steps appear (e.g., redact, remind policy, secure channel).
Refine policy logic (optional enhancement)
Update the system prompt to add stricter rules (e.g., HIGH for any SSN or credit card; MEDIUM for contact info plus context about sharing).
Re-run and compare outputs to validate improved consistency.
Try additional audio (optional)
Replace sample_file with another recording that includes or excludes personal data.
Confirm false positives are limited and genuine disclosures are detected.