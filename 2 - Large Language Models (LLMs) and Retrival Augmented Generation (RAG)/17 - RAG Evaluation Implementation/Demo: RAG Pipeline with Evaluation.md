In this demo, let's evaluate the TechSupport Plus RAG system step by step.

Step 1: Install RAGAS
Step 2: Prepare Test Data
Step 3: Calculate Metrics
Step 4: Interpret Results
Context Precision: 0.92 - Good! 92% of retrieved documents are relevant

Context Recall: 0.88 - Decent, but we're missing some relevant docs

Faithfulness: 0.95 - Excellent! Answer sticks to the documents

Answer Relevancy: 0.90 - Good, answers address the questions

Step 5: Identify Improvements
Based on these metrics:

Low context recall? Increase retrieval from top-3 to top-5
Low faithfulness? Strengthen grounding prompt
Low answer relevancy? Improve query understanding
Low context precision? Improve embedding quality or chunk size
RAGAS provides 4 key metrics: context precision, context recall, faithfulness, answer relevancy
Evaluation identifies specific weaknesses to fix (not just "it's bad")
Aim for 0.90+ on all metrics for production deployment
Test with real customer questions, not synthetic examples





It's time for us to take the next step in our RAGA system. For this, we're going to leverage Chroma DB for our vector database, OpenAI for our LLM, and RAGAS, for our evaluation framework. First, we're going to define the libraries that we're going to be importing. Then we're going to set up some important information such as the collection name, embedding model that we're going to be using, and the local folder Chroma DB is going to be saving the data to. We are going to initialize our Chroma DB with a word collection in, and then we're going to load the embedding model. We're going to design some sample documents and we're going to be doing the embeddings on and we're going to be doing the search. Ultimately we're going to leverage this to generate some answers to some questions using our OpenAI LLM. To load the models into Chroma DB, we're going to combine the data with metadata and unique IDs, and then we're going to load all this information into our Chroma DB collection. Then we're going to define how to retrieve documents function that is going to combine all the information that we have in our Chroma DB as well as the metadata and the distance so we have a sense of how far are the information that is being retrieved to the query that we are making. We set up some test queries such as what is machine learning, neural networks, and computer vision applications, and we are able to test that we get very similar responses for each one of the queries. Then we set up a generate answer function. This will combine our context and query that we're making to get a raw answer from our open AI LLM using GPT 3.5 Turbo. For this, we'll have a sample questions that we're going to be defining here, such as what is artificial intelligence, what does machine learning work, and what is the difference between supervised and unsupervised learning? We run this through a for loop so that we are able to capture each of each of the answers that we are getting from the Open AI LLM, and we are now be able to see what these answers look like. Now, more importantly than the answers, it's being able to evaluate these answers against our ground truth. We are able to evaluate if these are good answers or they need further work. We combine our ground truth with the responses that we got from our LLM into a dataset. Then using our RAGAS framework, we're able to evaluate all of these against our faithfulness, answer relevancy, context recall and context precision. We run our evaluation for all of these. Then in a few seconds, we're able to get a sense as to how good are the responses that we are getting. As you are able to see here, for faithfulness and anti relevancy, it does require improvement. However, context recall and context precision is really good, meaning that it is leveraging the information correctly.