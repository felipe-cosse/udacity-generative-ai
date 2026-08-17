Analysis of cost results:

GPT-4o is faster AND cheaper for this mixed workload
o1-mini's reasoning overhead adds cost and time even on generation tasks
Cost per second is a useful metric for comparing efficiency
Scaling implications:

At 1,000 queries/day:

o1-mini: $23.40/day = $8,541/year
GPT-4o: $19.80/day = $7,227/year
Savings: $1,314/year by choosing the right model
At 1,000,000 queries/day:

o1-mini: $23,400/day = $8.5M/year
GPT-4o: $19,800/day = $7.2M/year
Savings: $1.3M/year
When o1-mini wins on cost:

If you filtered to only the 3 reasoning tasks:

o1-mini would likely be cheaper per correct answer
Higher accuracy reduces need for retries
Lower cost per quality unit
The right model for the right job:

This exercise demonstrates that model selection matters immensely at scale.






For our first test, we're going to be evaluating two types of models, reasoning and generating models. For the reasoning, we're going to be choosing 04-mini with a temperature of one and maximum tokens of 500. For the generation model, we're going to be using gpt-4o temperature of one, maximum of tokens of 500, and a top_p of 0.95. We are going to set three different reasoning prompts with the expected answer and a little bit of description to understand what each of these props will do. Then we set up three generation prompts that will allow us to evaluate the responses for each of these tasks. We complete our call for OpenAI LLM, that this will help us make all these tests a little bit simpler by setting up the model, the messages, the temperature, and the maximum completion tokens. As well, we are also evaluating how long it takes for each of these responses to complete. Then we set up very simple tests in order to be able to evaluate the responses. Both for accuracy in the very specific words that we are looking for, as well as for the creativity. We're looking for very specific words. These are simple tests to help us evaluate the models efficiently by now. Then we go through a full loop for our reasoning task in which we're going to be evaluating each one of the tasks and be able to present the results in a very well formatted form. We do the same thing for our generation task, where we are able to present all the information in an easy way to read it. At the end, we are able to set all of these by setting up which task we are going to be generating. 0, 1 or 2. As remember, we have set of three problems that we are able to test. I'm going to go ahead and I'm going to run our code here. You will see that it's going to start testing our optimized reasoning model 04-mini. Then it's going to run the same task for our generation model. Finally, it's going to run the reasoning task for both models as well. Notice that it is important for us not only to take a look at the quality of the response, five out of five, but also at the latency and the number of tokens that it generates. You will be able to do this for each one of the tasks and prompts that we have set up.