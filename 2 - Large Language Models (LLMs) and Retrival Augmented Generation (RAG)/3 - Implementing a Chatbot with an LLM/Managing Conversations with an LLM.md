Building Stateful Conversations: The Pattern
Let's walk through the complete pattern for building a stateful chatbot. This is the foundation you'll use in almost every LLM application.

The Conversation History Pattern
# Initialize empty conversation history
conversation = []

def chat(user_message):
    """Send a message and maintain conversation state."""

    # Step 1: Add the user's message to history
    conversation.append({
        "role": "user",
        "content": user_message
    })

    # Step 2: Send ENTIRE history to the API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,  # Full conversation!
        temperature=0.7,
        max_tokens=150
    )

    # Step 3: Extract the assistant's response
    assistant_message = response.choices[0].message.content

    # Step 4: Add assistant's response to history
    conversation.append({
        "role": "assistant",
        "content": assistant_message
    })

    # Step 5: Return the response
    return assistant_message
This pattern might seem simple, but it's powerful. Every time you call chat(), you're building a longer and longer history. The model sees the complete context of your conversation.

Following the Conversational Thread
Let me show you how this enables natural, contextual responses:

# First exchange
user_msg_1 = "My application keeps crashing"
bot_response_1 = chat(user_msg_1)
# Bot: "I'm sorry to hear that. Can you tell me which version you're using?"

# Second exchange - notice how we don't repeat the crash information
user_msg_2 = "Version 2.5"
bot_response_2 = chat(user_msg_2)
# Bot: "Thank you. When does the crash happen in version 2.5?"

# Third exchange - "it" refers to the crash, contextually understood
user_msg_3 = "When I try to export a file"
bot_response_3 = chat(user_msg_3)
# Bot: "I see. The export feature in version 2.5 has a known issue..."
Each call includes the full conversation. The model can reference "version 2.5" and "export a file" together, even though they were mentioned in separate messages.

The Context Window Limit
There's a hard technical limit to conversations with an LLM: context windows.

GPT-3.5-turbo has a 4,096 token limit. GPT-4 extends to 8,192 or even 128,000 tokens depending on the version. But eventually, long conversations will exceed these limits.

What happens when you hit the limit? Your API call fails with an error.

Strategies for Managing Long Conversations
1. Conversation Truncation

Keep only the most recent N exchanges:

def chat_with_truncation(user_message, max_history=10):
    """Maintain only the last 10 exchanges."""

    # Add system prompt (always keep this)
    full_conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add user message
    conversation.append({"role": "user", "content": user_message})

    # Keep only recent history
    recent_history = conversation[-max_history:]
    full_conversation.extend(recent_history)

    # Make API call with truncated history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=full_conversation
    )

    # Add response to full conversation
    assistant_message = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_message})

    return assistant_message
Trade-off: You lose old context. The AI might forget important details from earlier in the conversation.

2. Conversation Summarization

Periodically summarize old exchanges:

def summarize_conversation(conversation_history):
    """Summarize older parts of conversation."""

    # If conversation is short, don't summarize
    if len(conversation_history) < 20:
        return conversation_history

    # Get the older messages (first 10 exchanges)
    old_messages = conversation_history[:10]
    recent_messages = conversation_history[10:]

    # Ask LLM to summarize old messages
    summary_request = [
        {"role": "system", "content": "Summarize this conversation concisely."},
        {"role": "user", "content": str(old_messages)}
    ]

    summary_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=summary_request,
        max_tokens=150
    )

    summary = summary_response.choices[0].message.content

    # Build new conversation with summary
    return [
        {"role": "system", "content": f"Previous conversation summary: {summary}"}
    ] + recent_messages
Trade-off: Costs an extra API call for summarization, but maintains key context.

3. Selective Context

Only include relevant parts of conversation:

def chat_with_selective_context(user_message):
    """Include only contextually relevant past messages."""

    # Add new user message
    conversation.append({"role": "user", "content": user_message})

    # Use semantic search to find relevant past exchanges
    relevant_history = semantic_search(user_message, conversation, top_k=5)

    # Build context with system prompt + relevant history + new message
    context = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + relevant_history + [
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=context
    )

    assistant_message = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_message})

    return assistant_message
Trade-off: More complex implementation, but maximizes relevant context.




