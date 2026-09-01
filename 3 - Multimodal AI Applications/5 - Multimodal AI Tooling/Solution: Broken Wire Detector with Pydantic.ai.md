This walkthrough demonstrates a practical automation: classify a wire image as intact or broken with Pydantic AI + Google Gemini, then trigger the appropriate action. The exercise builds confidence in using structured outputs from LLMs, handling images as inputs, and wiring business logic based on model results.

Main premise: structure the model’s output with Pydantic so downstream decisions (email QA or ship the product) are reliable and easy to maintain.

Step-by-Step Instructions
Configuration
To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l1/exercises/2-pydantic-ai/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
Copy environment file and insert a Gemini API key:
cp env.example .env
Edit .env and set GEMINI_API_KEY=[your key]
Load environment:
from dotenv import load_dotenv
load_dotenv()
Enable Jupyter asyncio support (skip for scripts)
import nest_asyncio
nest_asyncio.apply()
Add utility to display images (optional but helpful)
Use PIL and matplotlib:
display_image_with_caption(image, caption_json) to visualize the result.
Define the structured output contract
Create ImageAnalysis with:
status: Literal["intact", "not_intact"]
description: str
The docstring sets intent: “Detect whether the wire is intact or not, and describe the picture.”
Create a Pydantic AI Agent with Gemini
Model: google-gla:gemini-2.5-flash
Provide a concise system prompt focused on image analysis.
Set output_type=ImageAnalysis for enforced schema.
Prepare and send the image
Load the image: Image.open("wire.jpg")
Resize with thumbnail((600, 600)) to optimize tokens.
Encode as BinaryContent with media_type='image/jpeg'.
Run inference with structured output
Call agent.run_sync([binary_content]).
Extract result.output to get an ImageAnalysis instance.
Inspect and display results (optional)
Pretty-print: analysis.model_dump_json(indent=4)
Optionally overlay the JSON on the image for quick review.
Trigger the action
If analysis.status == "not_intact", call send_alert_to_qa_team(analysis.description).
Otherwise, call mark_for_shipping().
Adapt for async applications (optional)
Replace run_sync(...) with await agent.run([...]) inside async code.
Remove nest_asyncio.apply() in pure script environments.
Remember: enforce a strict output schema with Pydantic to make LLM results reliable and easy to use.

Keep model calls efficient by resizing images and using BinaryContent with the correct media type.






This exercise, you experimented with Pydantic AI and learned how to use it to interact with API based models such as Google Gemini. Let's look at the solution. First, we need to load our credentials. Make sure this returns true and your credentials are actually loaded. Then, remember to apply the nest-asyncio trick so you can use Pydantic AI within Jupyter. To conclude these preparation steps, simply execute this cell with the helper function to display our image and its caption. Now, let's get to the main focus of this exercise. Using Pydantic AI with Gemini to get structured output. The first step you had to complete was setting up the output schema using Pydantic. Here's how it's done. We create an image analysis class, or whatever you want to call it that inherits from the base model class from Pydantic. We add a doc string describing the task related to this output schema. We then add two attributes, a status attribute that can only take one of two values intact or not intact, and a description, which is free from text, where the model can describe what it sees. With that in place, let's look at the second thing you had to do. Create an agent instance using the Google Gemini 2.5 flashlight model, passing in our output schema and a suitable system prompt. Now that we have the agent, let's look at how we use it. We go inside this function where I already prepared the binary content instance, which contains our image encoded in a format that the model can understand. All you had to do was call the agent using Rn sync, passing in the binary content instance and making sure to wrap it in a list. Let's apply what we have prepared so far. First, you had to read the wired.jpg image, which is done using the open method of the image class from pillow. Then you had to call the function we just completed and collect the result. When we execute this cell, we get this output. We can see that the model indeed detected that the wire is broken and provided a description of it. Great. Now, for the last step of the exercise, I prepared mock functions for you, send alert to QA team and mark for shipping. You had to write simple code to execute one or the other conditionally based on the status of the wire detected by the model. Since the wire is broken, we call the function that mark's sending an e mail to the QA team. This simulates a typical scenario where your AI is part of a larger system that needs to take decisions programmatically based on the output of the analysis. This concludes the solution to this exercise. See you next time.