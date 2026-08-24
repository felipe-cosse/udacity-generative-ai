Project Environment
Here’s a breakdown of the technical environment you’ll be using in this project.

Programming Language
Python: All of the code you'll write for this project will be in Python.
Core Libraries and SDKs
You'll be using several key software development kits (SDKs) to interact with the different services and components of your RAG system:

OpenAI Python SDK: This is the official library for interacting with the OpenAI API. You'll use it to access the embedding models (for converting text to vectors) and the chat completion models that will generate the final answers.
Chroma SDK: This library allows you to work with ChromaDB, the open-source vector database you'll use to store and query your document embeddings. You'll use it to build your document index and perform semantic searches.
RAGAS SDK: This is the toolkit you'll use to evaluate the performance of your RAG system. It provides the functions needed to calculate metrics like faithfulness, answer relevancy, and context precision.


Local Machine Instructions


If you want to work on this project on your own computer, here are the instructions to get everything set up.

Prerequisites


Before you start, make sure you have the following:

Python 3.10 or a more recent version installed.
An active OpenAI API key. Instructions for accessing an OpenAI Key with a budget are on the following pages.
Clone the GitHub repository for the project from : ( Link )


Installation Steps :


Install the Required Libraries: All the Python libraries you need are listed in the requirements.txt file. You can install them all with a single command using pip.



pip install -r requirements.txt



Workspace Instructions
On the following pages, you'll find a Udacity workspace where you can build and run your project.




