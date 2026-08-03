From Actor to Expert: Implementing AI Personas in Python
Have you ever asked an AI for expert advice, only to receive a generic, textbook-style answer? It might be factually correct, but it lacks the insight, tone, and perspective of a true professional. What's the difference between an AI that can simply recite information about a topic versus one that can embody the expertise of a professional in that field?

The difference lies in how we instruct it. Role-based prompting is a powerful technique for dramatically improving the quality, relevance, and safety of an AI's output in professional contexts.

Let's look at a practical example.

Analyzing a Suspicious Email
Imagine we have a potentially malicious email and we want an AI to analyze it.

The Suspicious Email Text:

From: SecureBank Support <support-update@secure-bank-net.com>
Subject: Urgent: Your Account Requires Immediate Verification

Dear Valued Customer,
We have detected unusual activity on your account. For your security, you must verify your identity immediately by clicking here: http://secure-bank-net.com/verify-now
Failure to do so within 24 hours will result in account suspension.
Thank you,
SecureBank Team
Attempt 1: The Generic Assistant
First, let's ask a generic assistant for help without giving it a specific role.

# The generic system prompt
system_prompt_generic = "You are a helpful assistant."

# The user's request with the email data
user_prompt = f"""
Please analyze the following email and tell me if it's safe:
---
{suspicious_email_text}
---
"""

# Calling the model
response = get_completion(system_prompt_generic, user_prompt)
print(response)
Likely Output:
The model would likely (and correctly) identify this as a phishing attempt. The response would be helpful but generic, something like: "This email looks like a phishing scam. You shouldn't click the link. It creates a sense of urgency and has a suspicious sender address."

This is okay, but it lacks professional rigor.

Attempt 2: The Cybersecurity Analyst Persona
Now, let's give the AI a proper role with specific instructions on its expertise, tone, and task.

# The detailed, role-based system prompt
system_prompt_analyst = """
You are a senior Cybersecurity Analyst providing a formal threat assessment. Your tone is objective, cautious, and precise.

When analyzing a potential phishing email, do the following:
1.  State your overall assessment clearly (e.g., "High-Confidence Phishing Attempt").
2.  Do not speculate or use casual language.
3.  List the specific red flags you've identified as a bulleted list. For each flag, provide a brief explanation.
4.  Conclude with a clear, actionable recommendation for the end-user.
"""

# We use the same user_prompt as before
response = get_completion(system_prompt_analyst, user_prompt)
print(response)
Likely Output:
Notice the difference. The output is no longer just a helpful tip; it's a professional analysis.

Assessment: High-Confidence Phishing Attempt.

Red Flags Identified:

Sender Address Spoofing: The sender email support-update@secure-bank-net.com uses a subdomain (support-update) and a slightly altered domain to impersonate a legitimate entity. Financial institutions rarely use such domains for official communication.
Urgency and Threats: The subject line and body use language designed to create panic ("Urgent," "Immediate Verification," "Failure to do so...will result in account suspension") to rush the user into making a mistake.
Suspicious Hyperlink: The hyperlink text "clicking here" masks the true destination URL, a common tactic to hide a malicious link.
Recommendation:

Do not click any links or reply to this email. Delete it immediately. If you are concerned about your account, please navigate directly to your bank's official website by typing the address in your browser or use their official mobile app to check your account status.

By defining a professional persona and a clear set of instructions, we guided the AI to produce a response that is not only more helpful but also more structured, trustworthy, and safe.

You'll apply this same principle of iterative prompt refinement, practicing how to control an AI's persona down to the details of its personality, expertise, and tone.