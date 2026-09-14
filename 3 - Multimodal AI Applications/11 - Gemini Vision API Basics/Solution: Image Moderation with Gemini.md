This walkthrough assembles an end-to-end image moderation workflow that checks workplace images against policy using Gemini with Pydantic AI. The goal is to produce structured, explainable results, support reliable automation, and simulate test data when real images are not available.

What this exercise teaches:

How to structure moderation outputs with Pydantic models and enums.
How to configure a Gemini-powered agent for image analysis.
How to generate synthetic images for testing and evaluate results consistently.

Step-by-Step Instructions
Prepare environment

To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l2/exercises/3-image-moderation/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Add .env with GEMINI_API_KEY=... in the parent directory.
Model the policy

Define PolicyViolationType enum with desired categories.
Create ModerationResult with is_compliant, violations, explanation, suggested_action.
Configure the Gemini agent

Set system_prompt with clear policy rules and reasonable guidance.
Use gemini-2.5-flash-lite, temperature=0.2, seed=42, and output_type=ModerationResult.
Add image moderation helper

Downscale to 600x600, encode to JPEG, and pass as BinaryContent.
Return parsed ModerationResult.
Define test scenarios

Create TestScenario entries with name, description, and expected_moderation_result.
Generate images and run moderation

Use gemini-2.5-flash-image-preview to synthesize images from scenario descriptions.
Retry generation if no image is returned.
Call moderate_image(...) and collect structured outputs.
Inspect and iterate

Review explanation, violations, and is_compliant.
Compare with expected_moderation_result.
Add more scenarios, edge cases, and policy categories as needed.
Move to real inputs

Replace synthetic generation with real workplace images.
Batch process images and store results for audits and analytics.
Evaluate reliability

Run multiple trials with varied seeds.
Track detection rates per violation category.
Avoid interpreting numeric “confidence” as certainty.
Helpful Code Highlights
Environment setup and credential check:

from dotenv import load_dotenv
import os

assert load_dotenv("../.env"), "Could not load credentials!"
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found")
Policy enum and structured output:

from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class PolicyViolationType(str, Enum):
    NONE = "none"
    UNPROFESSIONAL_ATTIRE = "unprofessional_attire"
    FOOD_IN_MEETING_ROOM = "food_in_meeting_room"
    PERSONAL_ITEMS_ON_DESK = "personal_items_on_desk"
    UNORGANIZED_WORKSPACE = "unorganized_workspace"
    CONFIDENTIAL_INFO_VISIBLE = "confidential_info_visible"

class ModerationResult(BaseModel):
    is_compliant: bool = Field(description="Whether the image complies with company policy")
    violations: List[PolicyViolationType] = Field(description="List of policy violations if any")
    explanation: str = Field(description="Brief explanation of the decision")
    suggested_action: str = Field(description="Recommended action if policy is violated")
Agent configuration with structured output:

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModelSettings

model_settings = GoogleModelSettings(temperature=0.2, seed=42)

moderation_agent = Agent(
    "gemini-2.5-flash-lite",
    output_type=ModerationResult,
    system_prompt=COMPANY_POLICY_PROMPT,
    model_settings=model_settings,
    retries=3,
)
Moderation helper:

from io import BytesIO
from pydantic_ai import BinaryContent
from PIL import Image

def moderate_image(img: Image.Image, agent: Agent) -> ModerationResult:
    img.thumbnail((600, 600))
    buf = BytesIO()
    img.save(buf, format="JPEG")
    res = agent.run_sync([BinaryContent(data=buf.getvalue(), media_type="image/jpeg")])
    return res.output
Scenario-driven generation and moderation:

from google import genai
from google.genai import types

def generate_and_moderate_image(test_scenario: TestScenario, moderation_agent: Agent):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=f"Create an image of {test_scenario.description}.",
        config=types.GenerateContentConfig(temperature=0.5, seed=42),
    )
    # Extract image, then call moderate_image(...)
Structured outputs with Pydantic make moderation decisions reliable, auditable, and easy to integrate.

Clear policy prompts and low temperature settings improve consistency, while explanations support responsible review and enforcement.






Let's look together at the solution to this exercise. After setting up our credentials, we need to activate the nesting of event loops using nest-asyncio. This is necessary to use pydantic AI in a Jupiter notebook if we don't explicitly use asynchronous programming. The first thing you had to do was complete the output schema for our moderation results. I already provided the policy violation, enum, but you had to complete the pydantic model. You had to add a field called Es compliant with the Boolean type, providing a description for the field by leveraging the field class of pydantic, like this. Providing a description helps the model understand what it's supposed to put into this particular field. Moving on, you had to add a violations field, which would contain the list of found violations, if any. This is accomplished by using a type list of policy violation type. We then provide a description like we did before. The other fields were already completed, so let's move on to the next part. Here, you were given the prompt describing our company policy about sharing workplace images on social media. You were also given some predefined settings for Google Gemini. We set the temperature to 0.2, which is a pretty low value, to ensure consistency in exchange for less creativity, which is obviously not needed here. We also fix a seed to further reduce the variability and ensure some level of repeatability. This is, however, not perfect for reasons we can't get into right now. Then the part you had to complete, you had to create the agent by providing the name of the model, the output type we've defined, the system prompt, as well as the model settings. It's also good practice to give a number of retries, so Pydantic A, I can retry requests that happen to fail for whatever reason. The next cell defines a helper function that just calls our agent on the image. We resize the image to make sure we don't handle images that are too large. We save it into a Bytes object using the Bytes IO trick. Then we call the run sync method of our agent passing in the image as a binary content class with media type equal to image/JPEG. For this demo, I decided to show you a trick that we can sometimes use to test our agents in a scenario such as this one. We might not have a lot of real-world images that would represent violations of our policies because those are hopefully rare, so we can generate some using models like Gemini itself, which can generate images starting from text prompts. In this cell, we define a few test scenarios. The idea is to use the description of each case to generate an image, and then we moderate that image with our agent and verify the answer against what we expect the result should be. In a real world case, you might want to use an image generation model that's less expensive and slower than Gemini, maybe something you can deploy on your own. But that's beside the scope of this exercise. With the test cases defined, let's run the analysis. In this function, we're using Google Gemini to generate an image by just asking it to create an image given the description in our test case. We then try for a few times. This is necessary because sometimes Gemini refuses to generate an image that contains potentially problematic content, such as employee information on a screen, even when they are fake. Inside the loop, we simply call the Gemini 2.5 flash image preview model to generate the image, then we extract it from the result. We then check if the generation is successful, otherwise, we try again. We then call this function on all our test cases. If you did everything right, you should see images that look similar to these with the results of our moderation agent. The first image has nothing problematic, and our agent does indeed find no violations. The second one presents a very messy workstation, and our agent catches that. The last one shows some fake, sensitive data, and once again, our agent flags that. Things are working as expected. This concludes the solution to this exercise. See you next time.