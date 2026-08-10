Before any language model can understand text, before any algorithm can find patterns, before any meaningful analysis can happen, we face a fundamental challenge: raw text is messy, inconsistent, and filled with variations that obscure meaning.

Consider these three sentences:

"The café is open."
"THE CAFE IS OPEN."
"the café is open!!!"
To you, these communicate essentially the same information. But to a computer processing raw strings, they're dramatically different. Different capitalization, different accents, different spacing, different punctuation. Without preprocessing, a machine learning model must learn that these are related—wasting capacity on surface variations instead of semantic meaning.

This is where normalization and pretokenization come in. They transform chaotic human text into consistent, structured input that models can learn from efficiently. These steps are invisible to most users but absolutely critical to everything modern NLP accomplishes.

Normalization: Cleaning and Standardizing Text
Normalization makes text consistent by applying transformations that reduce variation without destroying information. Every normalization step is a trade-off between simplicity and context.

More normalization means:

Simpler, smaller models
Faster training
BUT: Loss of potentially meaningful information
Less normalization means:

Richer context preservation
More complex models required
Slower training
BUT: Ability to distinguish nuances

Normalization and Pretokenization
Normalization and pretokenization are the foundations of NLP. They don't appear in academic papers or flashy demos, but they determine whether your models work reliably.

Normalization cleans text for consistency by removing complexity.
Pretokenization breaks the text into smaller "words" and will be the base of what tokens will be.
Tokenization and Postprocessing
Tokenization breaks text into smaller parts called "tokens" to create meaningful building blocks.
Postprocessing applies additional transformations, such as adding tags at the beginning and end of sentences.
Tokens - The Atoms of Language
After normalization and pretokenization prepare your text, you face a critical decision: how should you break down the text into tokens? This affects every downstream task in natural language processing.

Think about reading this sentence. Your brain doesn't process it character by character, and it doesn't wait for complete sentences before starting to understand meaning. You work with words and meaningful word parts—prefixes, roots, suffixes. Your mental vocabulary strikes a balance between memorizing complete words and understanding word components.

Language models face the same challenge. Break text too small (individual characters) and you lose semantic meaning. Keep pieces too large (complete words) and you struggle with vocabulary size and rare words. The tokenization strategy defines the building blocks a model works with, shaping what it can learn and how efficiently it learns.

A token is the basic unit of text that an LLM processes. Think of tokens as the "atoms" of language from the model's perspective. Tokens aren't always whole words.

Let's look at how the same text gets tokenized differently:

Example 1: Common words

Text: "I love pizza"
Tokens: ["I", "love", "pizza"]
Token count: 3
Example 2: Uncommon words

Text: "I love pizza margherita"
Tokens: ["I", "love", "pizza", "margin", "herita"]
Token count: 5
Notice what happened? "margherita" got split into two tokens because it's less common. The tokenizer learned that "pizza" appears frequently enough to be its own token, but "margherita" is rarer, so it breaks it into pieces.

Example 3: Technical terms

Text: "Initialize the PostgreSQL database"
Tokens: ["Initialize", "the", "Post", "gre", "SQL", "database"]
Token count: 6
The technical term "PostgreSQL" splits into three tokens. This is why technical prompts often cost more - specialized vocabulary fragments into more tokens.

How Tokenization Actually Works
Modern LLMs use subword tokenization algorithms like Byte Pair Encoding (BPE) or WordPiece. The idea is elegant: find a balance between character-level (too granular) and word-level (vocabulary too large) tokenization.

Here's the intuition:

Character-level tokenization:

Text: "chatbot"
Tokens: ["c", "h", "a", "t", "b", "o", "t"]
Problem: 7 tokens for one word! Very inefficient.
Word-level tokenization:

Text: "chatbot"
Tokens: ["chatbot"]
Problem: Need a token for every possible word - vocabulary explodes!
Subword tokenization (BPE):

Text: "chatbot"
Tokens: ["chat", "bot"]
Sweet spot: Common subwords as single tokens, rare words split up.
The tokenizer learned during training that "chat" and "bot" appear frequently, so they each get their own token.

Tokenization Methods
Character tokenization
Character tokenization means that each character becomes a token.

Grid of colored blocks for each character in "do you prefer coffee or tea?" with no spaces.
Example of character tokenization

This results in a small vocabulary but can be harder for downstream tasks.

Word tokenization
Word tokenization means that each word becomes a token.

Grid of colored blocks for each word and punctuation in "do you prefer coffee or tea?" with no spaces.
Example of word tokenization

This retains more context than character tokenization, which makes downstream tasks easier. But it also results in a much larger vocabulary, increasing the likelihood of encountering out-of-vocabulary tokens.

Subword tokenization
Subword tokenization is a balance between small and large tokens where frequent words are not split and rare words are broken down.

Grid of colored blocks for multiple letters to make words in "do you prefer coffee or tea?". The blocks are "do", "you", "pre", "fer", "cof", "fee", "or", "t", "ea", "?"
Example of subword tokenizations

Subword tokenization is popular because it keeps vocabulary size manageable compared to word tokenization while retaining more context than character tokenization.

Common Subword Tokenization Algorithms
Byte-pair encoding (BPE)(opens in a new tab)
WordPiece(opens in a new tab)
SentencePiece




Tokenization transforms text to a useful representation that a computer can understand. During tokenization, we can also assist in extracting the context from the text. The steps to tokenization can be summarized into four steps. Normalization, pretokenization, tokenization, and post processing. The first step in tokenization is normalization, which essentially cleans the text for consistency. The steps for normalization vary depending on your task. In practice, more normalization will be done to reduce complexity, but will also mean you can lose context. During normalization, we might make all letters, lower case, remove punctuation, and replace acted characters. However, the most advanced NLP systems, like large language models, will opt to keep more complexity and less normalization. For example, punctuation is usually kept to retain more contexts. It's also important to not clean out important information if it's relevant to the task. In certain situations, accented characters can be important to the overall text in other times, they won't be. Characters that contain contextual information, such as keeping hash tags or emoticons might be worth keeping as well to retain its contexts. Our next step in creating tokens is pretokenization. This is where we break up the text into smaller pieces. You can think of the pre tokenizer as splitting your text into words. These will be the base of what your tokens will end up being. In some languages like English, we might split the text into words separated by spaces, which can then be later split further in later steps. However, splitting text into words isn't always a simple and obvious operation. Languages like Korean, Mandarin, and Cantonese don't group characters into semantic units the way languages like English do.