What Are Vocareum Gemini API Keys?
OpenAI API keys provide access to paid Gemini services. Vocareum is a provider that Udacity uses to grant learners access to these keys as part of enrolling in a Udacity program.

Unlike API keys that come directly from Gemini, Vocareum Gemini API keys must be routed through Vocareum servers, allowing Udacity to manage API usage budgets.

Finding Your Vocareum Gemini API Key
You will find this on the “Cloud Resources” button on the navigation pane. By clicking into the “Cloud Resources” button, you will be provided with a Gemini API key along with the budget assigned to that key.

Under the "Gemini Key" header, there is a value starting with "voc" as well as an info panel showing "You have $10 left of your $10 budget for this program"
Your Budget
As you use up the credits, you can come back to that screen to see how much budget you have left. Note that while the key may appear at the lesson level, this budget may be shared across the broader Udacity program (course or Nanodegree program).

The budgets are set to align with the demos, exercises, and projects in the program. To avoid prematurely running out of your budgeted credits, do not use models or endpoints beyond those indicated in the program content.

Using Vocareum Gemini API Keys
Code that uses Vocareum Gemini API keys must include the appropriate configuration so the requests are routed to the Vocareum server.

The Python code for this configuration depends on the specific package being used. The following examples use a placeholder example API key, which must be replaced with your actual key.

Gemini Python Package
from google import genai
from google.genai import types

client = genai.Client(
    api_key="voc-00000000000000000000000000000000abcd.12345678",
    http_options={"base_url": "https://gemini.vocareum.com"},
)
REST API Calls
If using curl or another client to access the Gemini API, build the URLs using https://gemini.vocareum.com in place of https://generativelanguage.googleapis.com




