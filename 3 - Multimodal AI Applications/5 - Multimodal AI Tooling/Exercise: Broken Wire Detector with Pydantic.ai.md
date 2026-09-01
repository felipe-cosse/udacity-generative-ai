Prerequisites:
Python 3.10+ and Jupyter environment (classroom workspace or local)
Packages: pydantic-ai, python-dotenv, nest_asyncio, pillow, matplotlib
Google Gemini API key (from Google AI Studio) set in .env as GEMINI_API_KEY
Sample image file: wire.jpg
Internet access for model calls
Objectives:
By the end of this exercise, learners will be able to:

Configure environment variables and load credentials with python-dotenv
Define a Pydantic model with Literal types for structured output
Create a pydantic_ai.Agent for Gemini with an effective system prompt
Provide an image via BinaryContent and run analysis with run_sync
Implement control flow to route outcomes to QA alerting or shipping
Steps:
Prepare the workspace

To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l1/exercises/2-pydantic-ai/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Ensure wire.jpg is present in the working directory.
Configure credentials

Copy the example environment file: cp env.example .env.
Open .env and set the Gemini key: GEMINI_API_KEY=[your key]. Leave other entries unchanged.
In code, load variables:
from dotenv import load_dotenv
load_dotenv()
Enable asyncio in Jupyter

Import and apply Nest Asyncio:
import nest_asyncio
nest_asyncio.apply()
Note: Not required for plain Python scripts that manage their own event loop.
Review utility function

Confirm the provided display_image_with_caption(image, caption) is present for visualization.
Define the structured output model

Create a Pydantic BaseModel named ImageAnalysis with:
Docstring: “Detect whether the wire is intact or not, and describe the picture.”
status: Literal["intact", "not_intact"]
description: str
This schema will enforce valid values and guarantee consistent downstream logic.
Create the agent with structured output

Import: from pydantic_ai import Agent
Set the model to google-gla:gemini-2.5-flash.
Pass output_type=ImageAnalysis.
Provide a concise system prompt, for example:
“Act as a quality inspector. Decide if the wire is intact or not. Return ‘status’ and a concise ‘description’. Only use the allowed schema.”
Example signature (conceptual): agent = Agent(model="google-gla:gemini-2.5-flash", output_type=ImageAnalysis, system_prompt="...").
Implement the analysis function

In analyze_image_with_structured_output(img), ensure:
The image is resized with .thumbnail((600, 600)) to save tokens.
The image is encoded to JPEG in memory and wrapped in BinaryContent(data=..., media_type="image/jpeg").
Call agent.run_sync([binary_content]) (note the list) and return result.output.
This will yield a validated ImageAnalysis instance.
Load the image

Use Pillow to open the test asset:
from PIL import Image
image = Image.open("wire.jpg")
Run the analysis

Call the helper:
analysis = analyze_image_with_structured_output(image)
Print and inspect structured results:
print(analysis.model_dump_json(indent=4))
Optionally visualize:
display_image_with_caption(image, analysis.model_dump_json(indent=4))
Route the outcome

Implement the decision:
If analysis.status == "not_intact": call send_alert_to_qa_team(analysis.description).
Else: call mark_for_shipping().
Confirm console output shows either an alert draft or successful routing to shipping.
Validate behavior with variations (optional)

Try different wire images (clean vs. visibly damaged) to see status changes.
Adjust the system prompt for stricter language or shorter descriptions and observe the schema staying stable.
Troubleshooting

Missing key: ensure .env contains GEMINI_API_KEY.
Permission or model errors: confirm API access to gemini-2.5-flash.
Jupyter hangs: ensure nest_asyncio.apply() was executed before agent calls.
Large images: keep thumbnails under 600×600 to control token usage.
