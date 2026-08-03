Prerequisites
To succeed in this course, you should have:

Required Knowledge
Python programming: Comfortable with functions, classes, loops, and error handling
Basic data structures: Understanding of lists, dictionaries, and JSON
API concepts: Familiarity with making HTTP requests and handling responses
Command line basics: Ability to navigate directories and run Python scripts### Recommended Background
Machine learning awareness: Basic understanding of training data and models (helpful but not required)
Working with text data: Experience reading files and processing strings
Git fundamentals: Cloning repositories and tracking changes (for project work)### Technical Requirements
Don't worry if you're not an expert in all areas—the course will guide you through each concept with clear explanations and hands-on practice.

Review Resources
If you'd like to review prerequisite resources, here are some Udacity Nanodegrees you can review to prepare you for this course.

AI Programming with Python(opens in a new tab)

Programming for Data Science with Python(opens in a new tab)

Environment
This course provides you with the tools and resources needed to build LLM applications professionally.

Udacity Classroom Workspace
Jupyter Notebooks: Browser-based Python environment for exercises and demos
Pre-installed libraries: OpenAI SDK, ChromaDB, Streamlit, RAGAS, and other required packages
Sample datasets: Customer service data for exercises, NASA mission documents for the project
No setup required: Start coding immediately without installation
OpenAI API Access (Provided)
Vocareum OpenAI API Key: Free API credits included with your enrollment
Budget monitoring: Track your API usage in the "Cloud Resources" section
Cost-optimized examples: All exercises are designed to stay within your allocated budget
Access to models: GPT-3.5-turbo, GPT-4, and text-embedding-3-small
Working Locally (Optional)
You can work on your own machine if you prefer. Just make sure you have all the required software and you are working in Python 3.8 or higher. Run this script to confirm your setup:

# Confirm Python 3.8 or higher
python --version
# Install required packages
pip install openai chromadb streamlit ragas pandas numpy tiktoken
You'll also need to add an OpenAI key. You can use the key provided in the classroom or your own:

If you use Vocareum keys (provided in course)
from openai import OpenAI
client = OpenAI(
    base_url="https://openai.vocareum.com/v1",
    api_key="your-vocareum-key-here"
)
If you use your own OpenAI key
client = OpenAI(api_key="your-openai-key")
Resource Downloads:
Exercise starter code: Available in course workspaces
Sample datasets: Downloadable from workspaces and GitHub links
Project data: NASA mission documents provided in project workspace
Course GitHub repository: (opens in a new tab)https://github.com/udacity/cd13318-exercises-project/(opens in a new tab)
Using Your Own API Keys
If you have existing OpenAI credits or a company account:

Standard OpenAI keys work with all course code (just update the base_url)
Be mindful of costs: some exercises may consume more tokens than with Vocareum routing
Budget guidance provided for each exercise##