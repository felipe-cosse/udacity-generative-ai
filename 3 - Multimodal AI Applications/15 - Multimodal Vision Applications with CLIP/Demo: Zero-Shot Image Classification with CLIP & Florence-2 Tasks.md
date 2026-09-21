Explore how to classify images without task-specific training using CLIP, then extend to rich multimodal tasks with Florence-2. The workflow mirrors real-world needs such as:

Weather condition recognition for photo organization and content filtering
Automatic alt-text generation and descriptive captions for accessibility
OCR for signs, receipts, and screens in diverse languages

Step-by-Step Instructions
1) Setup
To use the Udacity workspace:
At the top of the page, click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l2/demos/5-clip-and-florence/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the correct environment (the bottom option, named the same as this activity’s directory).
2) Load and Preview Images
Load sample images and preview a grid to confirm inputs.
images = [Image.open(x) for x in glob.glob("weather_images/*")]
display_grid(images, nrow=4)
3) Zero-Shot Image Classification with CLIP
Load the CLIP model and processor.
Define candidate labels (weather conditions).
Encode images and texts, compute logits and probabilities.
Visualize top-2 predictions per image.
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

classes = [
    "a picture in a cloudy weather",
    "a picture in a sunny weather",
    "a picture in a foggy weather",
    "a picture in a rainy weather",
    "a picture in a snowy weather"
]

inputs = clip_processor(text=classes, images=images, return_tensors="pt", padding=True)

with torch.no_grad():
    outputs = clip_model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)

display_clip_results(images, probs, classes)
What happens:

Images and text prompts are embedded into a shared space.
Similarity scores (logits) are produced for each image-class pair.
Softmax converts logits to probabilities for easy interpretation.
4) Florence-2: Image-Text Tasks
Initialize the Florence-2 pipeline for image-to-text tasks.
Supported tasks include:
, <OCR_WITH_REGION>
, ,
, <OPEN_VOCABULARY_DETECTION>
<DENSE_REGION_CAPTION>
<CAPTION_TO_PHRASE_GROUNDING>
<REFERRING_EXPRESSION_SEGMENTATION>, <REGION_TO_SEGMENTATION>
<REGION_TO_CATEGORY>, <REGION_TO_DESCRIPTION>, <REGION_TO_OCR>, <REGION_PROPOSAL>
florence = pipeline(
    "image-text-to-text",
    device=0,                 # set -1 for CPU if no GPU
    dtype=torch.bfloat16,     # use torch.float32 on CPU if needed
    model="ducviet00/Florence-2-base-hf"
)
5) Image Captioning
Generate captions at different detail levels for any image.
import textwrap
img = images[2]

task = "<CAPTION>"
ans = florence(img, task)
print(ans[0]['generated_text'])

task = "<MORE_DETAILED_CAPTION>"
ans = florence(img, task)
print(textwrap.fill(ans[0]['generated_text'], width=100))
6) OCR (Text Extraction)
Configure font to render non-English text.
Run OCR and display the recognized text.
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']

ocr_sample = Image.open("ocr_sample.jpg")
task = "<OCR>"
ans = florence(ocr_sample, task)

fig, ax = plt.subplots()
ax.imshow(ocr_sample); ax.axis("off")
_ = ax.set_title(ans[0]['generated_text'])
Takeaways
Zero-shot classification enables flexible image labeling without task-specific fine-tuning.
CLIP aligns text prompts and images in a shared space; logits + softmax provide readable probabilities.
Florence-2 covers a broad set of vision-language tasks with one interface.
Captioning and OCR workflows can be built in a few lines and adapted to many domains.





Today, we're going to show how we can leverage pre-trained foundation models in our applications that we can deploy on our own infrastructure. Let's get into it. Let's start with defining a few helper functions for visualization. Now, let's say we have an extensive collection of outdoor scenes. We want to add tags to that collection. For example, here I'm displaying some images that could belong to that collection. An obvious tag we'd want to add is the weather displayed in that shot. This is a very specific task, one for which we likely won't find specialized models. Before foundation models, we would have had to collect labels on our collection. Then train a custom model for each tag we wanted to add. This would have discouraged all but the most persistent teams. With CLIP, we can do that without any training. Let's see how. First, we need to load the processor and the CLIP model itself. We do that using from pre-trained method from the Hugging Face Transformer Library. Then, we simply define our classes. In our case, just a simple list of possible weather categories. Note that you get the best performance with CLIP by writing your classes as possible captions for an image instead of just the class. A picture in rainy weather is more likely to work than just rainy or rain. This is due to how CLIP was trained. Now, the magic happens. We run images and classes through the CLIP processor, which tokenizes them and processes them appropriately. Then, we simply run those through the model to get our outputs. The outputs contain the logits for each image, which are classification scores corresponding to our classes. We then apply the softmax function to obtain the class probability for each image. For each image, we get a vector with a size equal to the number of classes, where each position represents the probability that the image belongs to that class. Let's display the results by showing the first two highest probability classes for each image. We can see that in the first image, the model is pretty uncertain between rainy and cloudy, which makes sense given the image. In the second, there are clearly clouds, but no rain, so the model is predicting confidently the cloudy class. The third image is clearly a city street during a rainy evening. Hence, the class is indeed rainy. As you can see, we got our specialized classifier without any training. Note that realistically, you'll still need to label some data because you'll need at least a minimum validation dataset to measure performance before implementing in production. However, the size of this validation dataset would be orders of magnitude smaller than what you'd need to train your own classifier. That was an example of what Clip can do. Now, let's move to a different, even more flexible, model called Florence-2. In this case, we're going to use a different method for using Hugging Face models called pipeline. A pipeline encapsulates all the steps we were doing manually before, pre-processing, calling the model, post-processing, and can be used directly in just one call. Not all tasks are supported, however. Check the documentation for all available parameters. We just need to create a pipeline for the task we want called image text-to-text to signify that we start from an image, plus some text, describing what to do with that image, and we get text as output. The Florence-2 pipeline can do a lot of things, represented by what Florence-2 calls tasks. It can do OCR, OCR within a specific region, captioning, and many other things. Refer to the docs for details. For today, let's look at a few of them. Let's imagine, we're a news outlet. We need to make our website compliant with the Americans with Disabilities Act by providing alt text for all our images. Manual captioning would take months, but with this, we can potentially generate them automatically. Let's look at a sample image. We can define that the task we want Florence to do is caption. Then just run the pipeline on our image specifying that task. We immediately get a brief caption. We can also make the caption more detailed by changing the task to more detailed caption and re-running. We now get a much more comprehensive caption. For the same compliance effort, we also need to parse and transcribe all the text contained in the images, especially when they are an integral part of the story. We can leverage the exact same workflow and just change the task to OCR. Here's an example, where we're transcribing multilingual text contained in an image. As you can see, the model is recognizing the text in both languages and providing an accurate transcription. Good job sticking with me until now. This concludes our demo. See you next time.