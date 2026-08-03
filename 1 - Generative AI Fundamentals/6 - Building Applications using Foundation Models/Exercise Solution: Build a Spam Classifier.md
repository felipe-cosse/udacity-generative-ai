Solution Walkthrough
The first step is to build a classifier using a zero-shot prompt. This prompt defines the model's role and specifies the desired JSON output format, but it does not include any pre-classified examples. This approach tests the model's ability to perform the task based on instructions alone.

# Get a few messages and format them as a string
sms_messages_string = get_sms_messages_string(dataset, range(7, 15))
# ...

# <<< START SOLUTION SECTION

SYSTEM_PROMPT = """You are a helpful assistant that classifies text messages as SPAM or NOT SPAM.

    You will receive a list of text messages, each with a unique identifier.

    Respond only with JSON. Do not include any other text, preamble, or explanation.

    EXAMPLE INPUT:
    11 -> ...
    16 -> ...
    23 -> ...

    EXAMPLE OUTPUT:
    {
        "11": "NOT SPAM",
        "16": "SPAM",
        "23": "NOT SPAM"
    }
    """

# >>> END SOLUTION SECTION
# ...
After sending the prompt to the model, we use the provided get_accuracy function to evaluate its response. The zero-shot approach achieves 88% accuracy, with one message misclassified.

Mismatch for entry 7: predicted=SPAM, actual=NOT SPAM
Accuracy: 0.88
To try and improve the classifier, we use few-shot prompting. This technique involves providing the model with complete examples of inputs and their correct outputs. We construct a new system prompt that dynamically includes these labeled examples using the provided get_few_shot_examples_string helper function.

# ... (sms_messages_string is prepared as before)

# <<< START SOLUTION SECTION

SYSTEM_PROMPT = f"""You are a helpful assistant that classifies text messages as SPAM or NOT SPAM.

    You will receive a list of text messages, each with a unique identifier.

    Respond only with JSON. Do not include any other text, preamble, or explanation.

{get_few_shot_examples_string(dataset, range(54, 60))}
    """
USER_PROMPT = sms_messages_string

# >>> END SOLUTION SECTION
# ...
After checking the accuracy of this improved classifier, we see that the performance remains the same for this particular set of messages.

Mismatch for entry 7: predicted=SPAM, actual=NOT SPAM
Accuracy: 0.88
Key Takeaway
While few-shot prompting can often improve model performance by providing in-context examples, it is not a guaranteed fix for all classification errors, especially when dealing with ambiguous messages or suboptimal examples.





In this exercise, we build a spam classifier using a foundation model. The goal is to see how effectively we can identify spam messages using only clever prompting without any traditional model training. First things first. We need to set up our environment. This cell imports the necessary libraries and configures a API key so we can communicate with the foundation model. If you are using a Vocareum API key, please put it here. Our first step is to identify and gather some relevant data. Here, we're using the datasets library to load a pre label dataset called SMS Spam. This gives us a collection of text messages already marked as either spam or not spam. As you can see, the labels are numeric, zero for not spam, and one for Spam. The text messages themselves vary quite a bit. Now, those numeric labels aren't very intuitive. We'll create a couple of Python dictionaries to map the numbers to human readable labels like not spam and spam. This makes the output much easier to understand. Now when we print the same messages, the labels make more sense. Now, we'll move on to building our first classifier using an LLM. To send multiple messages to our model in a single request we'll need to format them nicely. This helper function takes a few messages from our dataset and combines them into a single numbered string. This is the core of our first attempt. We're creating a zero shot prompt. The system prompt tells the model its role. It's an assistant that classifies text messages and must respond in JSON format. The user prompt contains the actual numbered SMS messages we want it to classify. Notice we haven't given it any examples yet. We're just telling it what to do. That is what zero shot prompting is. With our prompts ready, we send them to the model using the Light LLM completion function. We then extract the text content from the models response. But how well did it do? This function compares the model's predictions to the actual labels in our dataset. For our first try, we got an accuracy of 88%. That's pretty good for not providing any examples. We can see it made one mistake, misclassifying message Number 7 as spam when it was not. Can we do better? Let's try few-shot prompting, where we give the model examples to learn from. This new helper function creates a formatted string containing both example SMS messages and their correct labels. Now, we construct a new system prompt. It's similar to the first one, but this time we've embedded the few-shot examples directly into the instructions. The model will see these examples before it sees a new messages it needs to classify in these are prompt. We send this improved prompt to the model and get our predictions back. Again, it has correctly formatted the output as a JSON object. Now, let's check the accuracy one last time. In this case, the accuracy is still 88%, and it made the same mistake on message Number 7. This is an important lesson. While few-shot prompting can often improve performance, it's not a guaranteed fix. Some messages might be inherently ambiguous, or perhaps our examples weren't the right ones to correct the specific error.