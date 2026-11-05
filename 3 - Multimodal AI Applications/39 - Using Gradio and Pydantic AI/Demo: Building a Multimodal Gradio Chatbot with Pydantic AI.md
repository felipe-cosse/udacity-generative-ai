In this demo, we build a compact chatbot app that accepts text plus media (images, audio, and clips) and replies using Google Gemini through Pydantic AI. The app runs in a browser using Gradio, handles concurrent users through async code, supports error handling and rate limiting, and can be extended to structured output tasks such as sentiment analysis.

Real-world uses:

Customer help with product images and voice notes
Media triage for support teams
Fast prototypes for media-aware assistants

Summary
Configure environment and API key
Create a Pydantic AI Agent for Gemini
Build an async chat function that accepts text and media
Wrap for error handling and rate limiting
Create a Gradio ChatInterface with multimodal input and state
Launch the app
Optional: enable streaming
Optional: create a custom app with structured output
Setup
To use the Udacity workspace:
Click Cloud Resources. Then select Start Cloud Resource, and then Open Cloud Console.
In VSCode, select the File menu and then Open Folder. Choose the directory for this assignment: /voc/work/code/l5/demos/1-gradio-unified-api/.
Open the notebook (.ipynb). In the upper-right corner select Select Kernel, then Python Environments, and choose the environment named the same as this activity’s directory.
Copy and edit environment file
cp env.example .env
Add the Gemini API key to .env
GEMINI_API_KEY=[your key]
Create the Pydantic AI Agent
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings

agent = Agent(
    model=GoogleModel("gemini-2.5-flash-lite"),
    system_prompt="You are a helpful AI assistant. Be concise and friendly.",
    model_settings=GoogleModelSettings(max_response_tokens=1024),
    retries=3,
)
Build the Async Chat Logic
Accept text plus file paths from Gradio
Detect MIME type, validate against supported types
Pack files as BinaryContent
Call the agent asynchronously and return the output with updated history
from pydantic_ai.messages import BinaryContent
import filetype

SUPPORTED_MIME_TYPES = ["image/png", "image/jpeg", "image/webp",
                        "application/pdf", "text/plain",
                        "video/mp4", "video/webm", "audio/wav", "audio/mp3", "audio/ogg", ...]

class ChatSession:
    def __init__(self, agent: Agent):
        self.agent = agent

    async def chat(self, message, history, past_messages):
        prompt_parts = []
        if message.get("text"):
            prompt_parts.append(message["text"])
        if message.get("files"):
            for file_path in message["files"]:
                kind = filetype.guess(file_path)
                if not kind or not kind.mime or kind.mime not in SUPPORTED_MIME_TYPES:
                    raise IOError(f"Unsupported file type: {file_path} ({kind.mime if kind else 'unknown'})")
                with open(file_path, "rb") as f:
                    prompt_parts.append(BinaryContent(data=f.read(), media_type=kind.mime))
        if not prompt_parts:
            raise ValueError("Please provide a message or at least one file.")
        result = await self.agent.run(prompt_parts, message_history=past_messages)
        return result.output, result.all_messages()
Why async matters: while waiting for Gemini, other users can interact without blocking the server.

Wrap for Gradio, Errors, and Rate Limiting
import gradio as gr
from rate_limiting import rate_limit

class GradioWrapper:
    def __init__(self, chat_session: ChatSession):
        self.chat_session = chat_session

    @rate_limit(calls=120, period=60)
    async def chat_gradio(self, message, history, past_messages):
        try:
            return await self.chat_session.chat(message, history, past_messages)
        except Exception as e:
            raise gr.Error(f"Error: {str(e)}")
Build the Gradio Chat Interface (Multimodal)
import gradio as gr

gradio_chat_session = GradioWrapper(ChatSession(agent))
past_messages_state = gr.State([])

demo = gr.ChatInterface(
    fn=gradio_chat_session.chat_gradio,
    type="messages",
    multimodal=True,
    title="Multimodal AI Chatbot",
    description="Chat with Gemini! Upload images, audio, or media files along with questions.",
    textbox=gr.MultimodalTextbox(
        file_count="multiple",
        file_types=["image", "audio", "video", "text", ".pdf"],
        placeholder="Type a message or upload files...",
    ),
    chatbot=gr.Chatbot(
        height=300,
        show_copy_button=True,
        placeholder="👋 Hello! Upload media or just chat.",
        type="messages",
    ),
    additional_inputs=[past_messages_state],
    additional_outputs=[past_messages_state],
)
Launch:

if __name__ == "__main__":
    demo.launch(share=False)
Optional: Streaming Responses
Replace run with run_stream and yield chunks:

async with self.agent.run_stream(prompt_parts, message_history=past_messages) as result:
    async for text_chunk in result.stream_text():
        yield text_chunk, past_messages
    updated_messages = result.all_messages()
    yield text_chunk, updated_messages
Update the wrapper to forward chunks with a streaming rate limiter.

Custom App with Structured Output
Targeted workflows (e.g., sentiment analysis) benefit from a schema and a tailored UI.

Define the output model:

from typing_extensions import Literal
from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    content_summary: str = Field(..., description="Summary by content type")
    sentiment: Literal["positive", "neutral", "negative"]
Create an Agent with output_type:

agent = Agent(
    model=GoogleModel("gemini-2.5-flash-lite"),
    system_prompt="You are a helpful AI assistant. Be concise and friendly.",
    model_settings=GoogleModelSettings(max_response_tokens=1024),
    output_type=AnalysisResult,
)
Wrap inputs from a form and return a DataFrame plus media previews:

import pandas as pd
from rate_limiting import rate_limit

class GradioWrapperCustomApp:
    def __init__(self, chat_session: ChatSession):
        self.chat_session = chat_session

    @rate_limit(calls=120, period=60)
    async def chat_gradio(self, text, file):
        message = {"text": text}
        if file:
            message["files"] = [file]
        result, _ = await self.chat_session.chat(message, [], [])
        df = pd.DataFrame([result.model_dump()])
        return df, file, file, file
Build the UI with Blocks, connect a submit button, and launch.

Takeaways
Multimodal input is straightforward with BinaryContent and MIME validation
Async functions keep the interface responsive under concurrent use
Gradio ChatInterface reduces boilerplate; Blocks enables custom layouts
Pydantic AI integrates cleanly with Gemini and supports retries, token limits, and structured output
Streaming improves UX for long replies
Error handling and rate limiting improve stability and safety






In the next few minutes, we're going to learn how to build a multi modal chat bot using Gradio and Pydantic AI with Google Gemini. This chat bot will accept text, images, audio and video inputs. Let's get started. We begin by setting up our credentials. First, we copy the example environment file and add our Gemini API key to it. Then we load those credentials using Dotenv and verify the API Key is actually loaded with an assertion. Before we build the chat bot, let's stop and talk a minute about async programming because we're going to leverage it heavily, and you might not be that familiar with it. Look at the diagram on screen. The top panel shows traditional synchronous code in a single threaded process. When you make Request 1, the CPU processes it, but then has to wait for input output, like waiting for a response from an API. During this waiting time, the CPU is basically doing nothing. Request 2 can't even start until Request 1 is completely done. Request 3 has to wait for both. This is incredibly inefficient. The middle panel shows multi threaded code. Here we can process multiple requests at the same time by using multiple threads. Thread 1 handles, Request 1. Thread 2 handles Request 2, and so on. This works, but threads have overhead, and there's complexity in coordinating between them. Moreover, most versions of Python have something called the global interpreter lock, which limits true parallelism. Now, look at the bottom panel. This is asynchronous programming. We're back to a single thread, but here's the magic. When Request 1 is waiting for a response, the CPU doesn't just sit idle. It can switch to start processing Request 2. While both requests are waiting for responses from the API, it can start Request 3. As soon as the response for Request 1 arrives, the CPU can switch back and finish it. Then when Response 2 arrives, it handles that. It's perfect for web applications like our chat bot. Think about it. When User 1 sends a message, we need to wait for Gemini to respond that might take a second or two. Instead of blocking and doing nothing, Gradio can handle User 2's message. While waiting for both Gemini responses, it can handle User 3 all on a single CPU, no multi threading needed. This is why async programming is so powerful for IO bound tasks, like API calls. In Python, you mark async functions with the async DF keyword, and you use await when calling other async functions. The await keyword is like saying, "Hey, Python, this is going to take a while. Go do something else and come back when this is ready." Gradio automatically recognizes async functions and let Python handle all the switching for us. We just need to write our code using async and await, and the rest happens automatically. Now let's build the core of our chat bot, the chat session class. This class has an init method that creates a unique session ID for tracking conversations and stores a reference to our Pydantic AI agent. The main method is chat, which is async because it needs to wait for AI responses. It takes three arguments, the message from the user, Gradio's chat history for display purposes, and Pydantic AI's message history, which we actually use for maintaining context. Inside the chat method, we start by building our prompt. We check if the message has text and add it to our prompt parts. Then we check for attached files. For each file, we use the file type library to detect its mime type and verify it's supported by Gemini. If it's not recognized or not supported, we raise an error. If it is supported, we read the file as bytes and wrap it in a binary content object with the correct mime type. Pydantic AI handles uploading this to Gemini for us. Once we have all our prompt parts, we use await to run the agent. This is the key async corporation. It tells Python this might take a while, so go handle other tasks while waiting. When the response comes back, we return both the AI's output and the updated message history, so future messages have context. Now, before we build the Gradio interface, let me give you a quick primer on Gradio itself. Gradio is a Python library that lets you create web interfaces with just a few lines of code. No HTML, CSS, or Java script required. The core concept is simple. You have components, which are UI elements, and you link them to Python functions. When the user interacts with the components, Gradio takes the user interaction and feeds it to Python functions as inputs, then takes the output of those functions and displays it back to the user. Common components include text box for text input and output, file for file uploads, image for displaying images, audio for playing or recording audio, video for video players, data frame for tables of data, button for clickable buttons, and chat bot for displaying chat messages. There are three main ways to build interfaces in Gradio. The simplest is interface. You just pass it a function, specify inputs and outputs, and you're done. For full control over layout, you use blocks, which lets you arrange components however you want, using row to arrange things horizontally, column for vertical arrangement, and tab for creating tab sections. For chat application specifically, there's chat interface, which gives you a pre-built chat UI. Perfect for what we're doing today. Connecting components to functions is straightforward. For buttons, you use the click method to specify which function to run, what inputs to pass to that function, and where to display the results. Gradio handles all the wiring automatically. A key feature is state management. The state component lets you persist data across interactions. For our chat bot, we'll use it to keep the conversation history, so the model remembers what you talked about earlier. Finally, launching your app is simple. You just call launch on your demo object. Set share to false for local use or true to create a public link you can share. That's really all you need to know. Components are your UI elements, functions are your logic, and events like click connect them together.






Connect our chat functionality with Gradio, we define a little wrapper. This serves as a connector, and it also allows us to handle errors gracefully. The Gradio wrapper class wraps our chat session, and as a chat Gradio method that catches any exceptions and displays them as Gradio errors instead of crushing the app. This gives users a much better experience. We then create our Pydantic AI agent with the Gemini flash light model. We set a generic system prompt, though in production, you'd want something more specific to your use case. We limit the max_response_tokens to 1,024 to control costs. That's roughly 750 words of English. We also enable automatic retries for transient errors. Next, we create a state variable to hold Pydantic AI's message history across interactions. This is crucial for maintaining conversation context. Now we build the Gradio interface using chat interface, which gives us a professional looking chatbot in just a few lines. We pass our chat Gradio method as the function to drive the chatbot. Note that Gradio automatically recognizes A sync functions and handles them appropriately. We enable multimodal mode and configure the text bot to accept multiple files of various types, images, audio, video, text, and PDFs. The chatbot component displays the conversation history with a copy button and a friendly placeholder message. Finally, we connect our message history state as both an additional input and output, so it persists across turns. We launch the app with share set to false. If you set it to true, Gradio creates a public link you can share. Before we play with it a bit, let's do one more thing. Now, let's add rate limiting to prevent abuse and manage costs. We import a rate limit decorator and apply it to our chat Gradio method. This limited to 120 calls per minute or two per second on average. The decorator handles the tracking automatically. Let's test our interface a bit. Great, it works well. Now, let me mention streaming responses. Pydantic AI supports streaming, where you see the response as it's generated, instead of waiting for it all at once. You'd replace the run code with run_stream and use an A sync for loop to yield chunks as they arrive. You'd also need to use the streaming version of the rate limiter. However, this doesn't work in our test environment, though it would work with the standard Gemini endpoints. Finally, let's build a more customized app for a specific use case, sentiment analysis. Instead of a chatbot, we want users to upload media and get structured analysis results. We define a pydantic model called analysis result with two fields, a content summary and a sentiment classification. We create a new agent that outputs the structure type instead of plain text. We build a new wrapper that reformats inputs from our custom interface into the format chat session expects. It takes text and a file, bundles them into a message dictionary, calls chat with empty history, since this is a one shot interaction and converts the result to a Pandas data frame for display. It also returns the file plot three times so it can be displayed in whichever media component matches the file type. For the interface, we use Gradio blocks for full layout control. We create a row with text input and file upload, another row with analyze and clear buttons, a data frame for results, and a row with image, video and audio components for displaying the uploaded file. The analyzed button connects everything. It takes the text and file as inputs, runs our analysis function, and outputs the results table plus the file to all three media components. Only the matching one will display it. The clear button just resets everything to none. Let's test it out a bit. Let's start with just some text. Yeah, the sentiment analysis is working. Now let's try with something multimodal like a video. Working again. Let's play the video. Let's try some audio now. The model can deal with that as well. Now let's use multiple things at once, say text and video. Let's put some information in the text related to the video and see what happens. As you can see, the model used the context from the text to interpret the video, and now it knows that the person is my friend Melissa and not just any person. It works as expected. This concludes our demo for today. You've learned how to build both a conversational chatbot and a custom analysis app using gradual and Pydantic AI with multimodal support, A sync programming, rate limiting, and structured outputs. Thanks for watching.