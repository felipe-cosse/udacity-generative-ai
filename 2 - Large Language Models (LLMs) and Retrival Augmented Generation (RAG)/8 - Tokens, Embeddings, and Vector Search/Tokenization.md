Where Tokenization Matters
Cost Control

Every API call charges per token. Understanding tokenization helps you optimize costs:

# Expensive prompt (verbose)
prompt = """
I would like to request that you please provide me with a comprehensive
and detailed explanation of the fundamental concepts underlying machine
learning algorithms, if you would be so kind.
"""
# Estimated: 35 tokens

# Cheaper prompt (concise)
prompt = "Explain machine learning algorithms."
# Estimated: 5 tokens
You just reduced costs by 85% while asking the same question!

Context Window Management

LLMs have token limits. Every token in your prompt, conversation history, and response counts against this limit.

# This might fail if conversation is too long
conversation_history = [
    # 50 previous exchanges = ~2000 tokens
]
system_prompt = "..." # 200 tokens
user_message = "..." # 100 tokens
# Total: 2300 tokens used before model even responds!
Subword tokenization is popular because it keeps vocabulary size manageable compared to word tokenization while retaining more context than character tokenization.

Common Subword Tokenization Algorithms
Byte-pair encoding (BPE)(opens in a new tab)
WordPiece(opens in a new tab)
SentencePiece(opens in a new tab)
Popular Subword Algorithms
Three main algorithms dominate modern NLP. They differ in how they build the vocabulary, but share the core principle of frequency-based splitting.

Byte Pair Encoding (BPE)
Used by: GPT-2, GPT-3, GPT-4, RoBERTa, BART

Start with characters, iteratively merge the most frequent adjacent pairs.

Algorithm:

# Simplified BPE algorithm

def learn_bpe(text, num_merges):
    # Start with character-level splits
    vocab = set(text)
    splits = [[char for char in word] for word in text.split()]

    for _ in range(num_merges):
        # Count all adjacent pairs
        pair_counts = count_pairs(splits)

        # Find most frequent pair
        best_pair = max(pair_counts, key=pair_counts.get)

        # Merge this pair everywhere
        splits = merge_pair(splits, best_pair)

        # Add merged token to vocabulary
        vocab.add(''.join(best_pair))

    return vocab, splits
Strengths: Simple, effective, completely data-driven Weaknesses: No linguistic knowledge, treats all merges equally

WordPiece
Used by: BERT, DistilBERT, Electra

Similar to BPE but chooses merges based on likelihood improvement rather than raw frequency.

Difference:

BPE: Merge the most frequent pair
WordPiece: Merge the pair that maximizes training data likelihood
This subtle difference means WordPiece considers how merges affect the model's ability to represent text, not just how often pairs occur.

Example:

Consider two pairs with equal frequency:
- ('th','e'): appears in "the", "there", "them", "then" (common, high utility)
- ('q','u'): appears in "question", "quick", "quiet", "quote" (common in specific words)

BPE: Might merge either based on exact counts
WordPiece: Prefers 'th'+'e'='the' because it appears in more varied contexts
Strengths: Slightly better compression and representation Weaknesses: More complex algorithm, slightly slower training

SentencePiece
Used by: T5, ALBERT, XLNet, many multilingual models

Treat the entire text as a raw byte stream, no pretokenization required.

SentencePiece doesn't assume whitespace separates words. This is crucial for languages like Chinese, Japanese, or Korean where words aren't space-separated.

Example:

English text: "Hello world"
Traditional approach: Split on spaces first → ['Hello', 'world'] → tokenize each
SentencePiece: Treat "Hello world" as one stream → ['▁Hello', '▁world']

The ▁ symbol represents the start of a word (where space was).

Chinese text: "你好世界" (Hello world)
Traditional approach: Struggles without clear word boundaries
SentencePiece: ['▁你好', '▁世界'] or ['▁你', '好', '▁世', '界']
                (Learns natural splits from data)
Strengths: Truly language-agnostic, handles any Unicode text Weaknesses: Slightly more complex preprocessing

Practical Implementation: Using Pretrained Tokenizers
In practice, you'll rarely train tokenizers from scratch. You'll use existing tokenizers matched to your model.

Matching Model and Tokenizer
This cannot be emphasized enough: If you use a model trained with one tokenizer on text processed by a different tokenizer, results will be nonsensical.

Libraries
HuggingFace Tokenizers: https://github.com/huggingface/tokenizers(opens in a new tab)
SentencePiece: https://github.com/google/sentencepiece(opens in a new tab)
BPE implementation: https://github.com/rsennrich/subword-nmt(opens in a new tab)
Tools:

Tokenizer visualization: https://platform.openai.com/tokenizer(opens in a new tab)
Compare tokenizers: https://huggingface.co/spaces/Xenova/the-tokenizer-playground(opens in a new tab)
Start with pretrained tokenizers matched to pretrained models. The sophistication built into modern tokenizers represents years of research and engineering - you should leverage it!




