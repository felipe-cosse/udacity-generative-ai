Key Takeaways from the Exercise
1. Tokens Are the Currency
Everything costs tokens: input, output, formatting
~1 token ≈ 4 characters (rough estimate)
Use tiktoken for accurate counting
2. Output Costs More
Output tokens are 2-3x more expensive
Limit output with max_tokens
Prompt for concise responses
3. Conversation History Compounds
Each message includes all previous context
Costs grow linearly with conversation length
Prune aggressively but preserve critical context
4. Model Choice Matters
GPT-4 is 40-60x more expensive than GPT-3.5-turbo
Use cheaper models for simple tasks
Hybrid routing saves 60-80% on costs
5. Optimization Is Mandatory
Unoptimized bots can cost 10x more
Monitor token usage in production
Iterate on optimization strategies
Resources
OpenAI Tokenizer Tool: https://platform.openai.com/tokenizer(opens in a new tab)
Tiktoken Library: https://github.com/openai/tiktoken(opens in a new tab)
Cost Optimization Guide: https://platform.openai.com/docs/guides/production-best-practices(opens in a new tab)



