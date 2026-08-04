Building Your First Chatbot: Understanding Conversation, Context, and Control
Run the cells in the demo below to explore creating a chatbot that includes:

conversation state
system prompts,
and message structures

From Simple Responses to Intelligent Conversations
When you first interact with ChatGPT, Claude, or Gemini it feels natural - like talking to a knowledgeable friend. The bot remembers what you said earlier, maintains context across multiple exchanges, and responds in a consistent personality. But here's something that might surprise you: the AI has absolutely no memory of previous messages.

Every single interaction is a fresh start. The model doesn't "remember" anything. So how does it maintain context? How does it know what "it" refers to when you say "Can you explain it differently?" The answer lies in how we structure our API calls.

The Stateless Nature of LLMs: A Memory Paradox
Large language models are completely stateless. Each time you send a message to an LLM (API call), it's like meeting someone with amnesia, they have no recollection of any previous conversation.

Think about how a simple web server works. When you visit a website, the server sends you a page, then immediately forgets about you. If you click a link, the server has no idea you were just there. To maintain a "session," the website uses cookies or tokens to reconstruct what you were doing.

LLMs work similarly. The model itself doesn't maintain any state between API calls. When you send a request, you're starting from scratch every single time.

The Illusion of Memory
So how does an LLM "remember" your earlier questions? The secret is elegantly simple: we send the entire conversation history with every new message.

This is what it looks like:

Turn 1:

messages = [
    {"role": "user", "content": "What's the weather like today?"}
]
# Send to API → Get response: "I don't have access to real-time weather..."
Turn 2:

messages = [
    {"role": "user", "content": "What's the weather like today?"},
    {"role": "assistant", "content": "I don't have access to real-time weather..."},
    {"role": "user", "content": "Should I bring an umbrella?"}
]
# Send to API → Model can reference previous context!
Notice what happened? On the second turn, we included the first question AND the assistant's response. This gives the model the context it needs to understand that "umbrella" relates to the weather discussion.

Message Roles: The Conversation Structure
Every message in an LLM conversation has a specific role. Understanding these roles is important for building effective chatbots.

The Three Core Roles
1. System:

The user never sees these messages, but they profoundly shape how the bot behaves.

{
    "role": "system",
    "content": "You are a helpful tech support assistant. Be patient and clear."
}
Think of the system message as the bot's internal instructions - its personality, its constraints, its purpose. Change this message, and you completely change how the bot responds to the same user input.

2. User:

User messages represent what the person using your chatbot says. These are straightforward - they're the questions, requests, or statements from your users.

{
    "role": "user",
    "content": "My laptop won't turn on"
}
3. Assistant: The Bot's Responses

Assistant messages are the model's previous responses. When building conversation history, you include what the assistant said in earlier turns.

{
    "role": "assistant",
    "content": "Let's troubleshoot this step by step. First, is the power cable plugged in?"
}
The role structure helps the model understand conversational dynamics. The model learns during training that:

System messages provide overarching context
User messages are questions or requests
Assistant messages are its own previous responses
This structure enables the model to maintain appropriate conversational boundaries and respond consistently with its assigned role.




