This demo shows how to create a short marketing asset for Brain Fuel, a fictional hydration drink, using Veo 3 in two workflows:

Prompt-to-clip: create a full motion asset from descriptive text only.
Image-to-clip: start from a product image to keep branding exact, then animate.
Real-world use case: rapid concept exploration for marketing, followed by brand-accurate product shots. Expect to learn trade-offs between speed and control, plus a practical pattern for polling and downloading outputs.

NOTE: Video generation is one of the most expensive operations you can use your API key for. If you run this demo code, it is best not too run too many times and to track your budget to ensure you have enough to complete any other work you need to complete.

Summary of the process
Configure environment and client.
Scene 1 (prompt-to-clip): describe the setting, product, and mood; generate and save.
Scene 2 (image-to-clip): create a product image, set it as the first frame, animate and save.
Compare outputs for speed vs control.
Setup
To use the Udacity workspace:
Click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l4/demos/5-video-gen/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the environment named the same as this activity’s directory.
Create environment file and add an API key.
cp env.example .env
Then set GEMINI_API_KEY in .env.
Initialize the client and imports.
import time
import dotenv
import os
from google import genai

dotenv.load_dotenv()
assert os.getenv("GEMINI_API_KEY"), "Please set the GEMINI_API_KEY environment variable"
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
Scene 1: Prompt-to-Clip (Text-to-… Generation)
Purpose: fastest way to get a marketing concept moving on screen.
Trade-off: the product container and label are model-generated, so exact branding may vary.
Steps
Write a descriptive prompt covering setting, product, lighting, and mood.
Call Veo 3 to create the motion asset.
Poll until done, then download and save as MP4.
scene1_prompt = """
A student is working on a laptop at a wooden desk in a cozy, dimly lit room.
Picks up a can of Brain Fuel, takes a sip, then acknowledges the brand.
Warm, moody lighting, shallow depth of field, cinematic, realistic.
"""

operation = client.models.generate_videos(
    model="veo-3.0-generate-001",
    prompt=scene1_prompt,
)

while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

scene1_video = operation.response.generated_videos[0]
client.files.download(file=scene1_video.video)
scene1_video.video.save("text-to-video.mp4")
Tips:

Include product name, label text, environment, lighting, and camera feel.
Keep prompts concise but specific.
Scene 2: Image-to-Clip (Brand-Controlled Generation)
Purpose: preserve exact product appearance while adding motion.
Trade-off: requires an image; slower than pure text prompts but better for brand accuracy.
Steps
Generate (or provide) a product image. In a real workflow, use an approved product photo.
Load the image as the starting frame.
Write a prompt describing motion, environment, and audio.
Call Veo 3 with the starting frame; poll, download, and save.
Generate a product image for the demo:

from PIL import Image
from io import BytesIO

# Optional: create client if not reused
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["""
An extreme close-up of a sleek aluminum Brain Fuel bottle with condensation.
Label text: "Brain Fuel - Hydrate Your Mind". Warm desk lamp lighting.
"""],
)

for part in response.candidates[0].content.parts:
    if getattr(part, "inline_data", None):
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("brain_fuel_product.png")
Animate the product image:

from google.genai import types

with open("brain_fuel_product.png", "rb") as f:
    image_bytes = f.read()

starting_frame = types.Image(
    image_bytes=image_bytes,
    mime_type="image/png",
)

scene2_prompt = """
Camera pulls back as hands open the can and take a sip.
Face not shown; warm amber lamp, bokeh background, evening study mood.
Include subtle handling sounds and a short brand line.
"""

operation = client.models.generate_videos(
    model="veo-3.0-generate-001",
    prompt=scene2_prompt,
    image=starting_frame,
)

while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

scene2_video = operation.response.generated_videos[0]
client.files.download(file=scene2_video.video)
scene2_video.video.save("image-to-video.mp4")
Prompt tips:

Describe motion (“camera pulls back”), visible elements (hands, desk, lamp), and mood.
Keep text short; focus on essentials that influence the scene.
Comparison
Prompt-to-clip
Fastest, great for concepting.
Less control over exact product visuals.
Image-to-clip
Strong control over branding and packaging.
Best for final product segments that must match approvals.
Takeaways
Two practical workflows: fast concepting from text and brand-accurate animation from an image.
Polling and download patterns are the same across both workflows.
Strong prompts describe setting, product details, lighting, and motion.
Image-to-clip preserves product look; prompt-to-clip maximizes speed.
Suitable path for marketing: concept first, then polish with brand-controlled animation.






In this demo, I'm going to show you how to generate marketing videos with Veo 3. We're going to create two video clips for Brain Fuel, a made up hydration drink, and you'll see how text-to-video compares to image-to-video generation. These are two fundamentally different workflows, each with its own strengths. Let's get into it. We start with the imports, time for polling our requests, dotenv to load environment variables and credentials, the GenAI library for accessing Veo 3, and PIL for handling images. We load the environment variables and make sure the API key is set with an assertion. We then initialize the client with our API key. This client gives us access to all of Gemini's capabilities, including Veo 3, and also Gemini 2.5 flash for image generation, AKA Nano Banana. Let's start with text-to-video. This is the simplest approach. You describe what you want and Veo creates it from scratch. We write a detailed prompt describing our scene. A student at their desk in warm evening lighting, reaching for Brain Fuel, taking a sip and delivering the tag line. We include specifics about the product design, lighting setup, and overall aesthetic. The more detailed the prompt, the better the results. Google publishes a prompt guide for Veo 3 that is worth looking into, which describes a few techniques to get the best out of Veo 3. Here, I'm using one of the options suggested there, which is to describe the scene, the lighting, and the audio separately. It is not the only option, but for this use case, it turned out to work best. Once we have the prompt, we call generate videos on the models object, passing in the Veo 3 model name and our prompt. This starts the generation and returns an operation object. Video generation takes a few minutes. While we wait, we poll the operation with a while loop, that checks if it's done, waits 10 seconds, then fetches the operation again. This continues until the video is ready. Once done, we grab the first video from the operation response. We download it using the files download method and save it locally as an MP4 file. Let's see what we got. Brain Fuel, my favorite water for studying. The video looks very nice, very realistic, and it follows the prompt very well. The only thing I don't like is the conclusion. The student smiles in a very realistic way, but then the video stops because of the eight second limitation. It doesn't look very realistic. Note that because of the randomness involved, rerunning the same prompt will return a different result. In many cases, you have to run your prompt a number of times and then select the best generation. For the second approach, the image-to-video, we want more control over the product appearance. This is more representative of real applications because say in a real campaign, you'd definitely have professional product photos, or renderings before you start working on the video. You will want the video to reflect the exact design of your product. For this demo, will generate a pretend one using Gemini image generation. We write a prompt describing our product shot, a close up of the Brain Fuel bottle with condensation, visible label, colorful patterns, and warm lighting. We call general content with the flash image model, AKA Nano Banana. Note that this is different from video generation. It's specifically for creating still images. We pass in our prompt and get back a response. The response contains candidates with parts. We look through these parts. If it's text, we print it, if it's image data, we open it with PIL and save it as a PNG. This is the generated image. This gives us our product image. Now, we animate our product image. We're using that image as the first frame of the generated video, which ensures our product looks exactly as designed. We load the product image as bytes, then create an image object from the types module with those bytes and the MIME type. This is what Veo 3 uses as the starting frame. We write a new prompt describing what happens after that first frame, camera pulling back, hands opening the can, the desk set up, warm lighting. We even specify audio cues like the metallic sound and the voice-over. We call generate videos again, but this time, we pass both the prompt and the image parameter. This tells Veo start with our image and animate from there. We pull the operation just like before checking every 10 seconds until it's done. Once ready, we download and save the video. Let's look at it. Brain Fuel, hydrate your mind. Everything worked, and now we have a video that includes naturally our exact product. The difference between these methods, text-to-video and image-to-video thumbs down to control versus speed. Text-to-video is useful for unconstrained use cases because it leaves more freedom to the model to generate. You describe what you want and get results. But you have less control over specific details like product appearance. You can try to describe exactly what you want, but you're still going to leave a lot of creative power to the model. Image-to-video instead gives you precise control over your products look. These matters for maintaining bland consistency in real campaigns. However, since you are forcing the model to start from a specific frame, the results of the generation can be of lower quality and it might get you longer to get a satisfying results. You might try different times. In practice, use text-to-video for rapid prototyping and exploring concepts. Use image-to-video when you need exact product representation in your final videos. Before we finish, let me note that Veo 3 generates up to eight seconds per clip. That's not much for a real campaign. You can stitch multiple segments together, but maintaining continuity is tricky. Character consistency works reasonably well with the appropriate prompts, but controlling room appearance, lighting, and camera angles across segments is very challenging. The practical solution is to design scripts with completely different scene settings for each segment, which avoids the continuity problem altogether. There are also other models in the market that offer durations up to one minute. Those might be better choices if you have a need for a longer video. That wraps up our demo, thanks for watching and see you next time.