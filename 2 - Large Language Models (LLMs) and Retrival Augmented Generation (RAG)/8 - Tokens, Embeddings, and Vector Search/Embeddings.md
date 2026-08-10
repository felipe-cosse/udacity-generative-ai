Introduction: The Limitation of Token IDs
Tokenization converts text into integer IDs—essential for computers to process language. But there's a fundamental problem: these numbers are arbitrary. They're just labels.

Consider this tokenization:

vocabulary = {
    'cat': 5,
    'dog': 12,
    'kitten': 247,
    'puppy': 301,
    'car': 8,
    'automobile': 156
}
From the computer's perspective, 'cat' (5) is closer to 'car' (8) than to 'dog' (12) just based on the numbers. The relationship between 'cat' and 'kitten' is completely invisible—they're just two different IDs with no connection. The synonym relationship between 'car' and 'automobile' is lost.

These token IDs are like ISBN numbers for books. The ISBN tells you which book you're holding, but it tells you nothing about the content, genre, author, or how it relates to other books. A cookbook and a philosophy textbook might have consecutive ISBNs, but that doesn't make them similar.

This is where embeddings change everything. Embeddings transform meaningless token IDs into rich vector representations that encode semantic relationships. They take us from arbitrary labels to geometric spaces where you can measure meaning with distance.

From IDs to Geometry
Imagine representing movies not with ID numbers but with coordinates in a space defined by meaningful dimensions:

Movie representations (2D for simplicity):

Dimension 1: Action level (0-10)
Dimension 2: Romance level (0-10)

Die Hard:        (9, 1)
Titanic:         (2, 9)
The Notebook:    (1, 10)
Mad Max:         (10, 0)
The Princess Bride: (6, 7)
Now you can do interesting things:

Similarity: Movies close together in this space are similar

Die Hard (9,1) and Mad Max (10,0) are close → both action-heavy
Titanic (2,9) and The Notebook (1,10) are close → both romance-heavy
What Is an Embedding?
An embedding transforms a token into a high-dimensional vector - a list of numbers that captures the token's meaning, relationships, and context.

The Geometry of Meaning
Embeddings place words in a high-dimensional space where semantic relationships become geometric relationships.

Similar words are close together:

embedding("cat")     = [0.234, -0.891, 0.445, ...]
embedding("kitten")  = [0.241, -0.883, 0.451, ...]  # Very similar!
embedding("dog")     = [0.198, -0.847, 0.412, ...]  # Somewhat similar
embedding("pizza")   = [-0.634, 0.234, -0.891, ...] # Very different!
You can actually measure the similarity. Because embeddings encode meaning as geometry, you can do math with concepts.

Creating Embeddings
Classic methods for vectorization (such as bag-of-words, one-hot encoding, and TF-IDF) can lack contextual relationships.

Embeddings can encode context by vectorizing text/tokens into representational vectors.

Properties of Embeddings
Two dimensional coordinate plot where a blue dashed-arrow for "tea" points from the origin towards the top-right, a green dashed-arrow for "coffee" points from the origin to approximately the same spot as the blue arrow, and an a purple dashed-arrow for "dog" points to the far right and not close to the the other two arrows.
Vectors close to each other are more similar.

At the top, an equation of words where the equal sign is replaced with an arrow: "cat" plus "bark" minus "dog" goes to "meow". Under the equation is a 3D coordinate system with four colored arrows representing the vectors for the different words. A blue dashed-arrow for "dog" and a pink dashed-arrow for "cat" point from the origin to the left, approximately to the same point. A green dashed-arrow "bark" and a purple dashed-arrow for "meow" point from the origin to the right, approximately to the same point.
Relationships between words/vectors are encoded in the vector space.






Transformer-based architectures are particularly well-suited for creating large language models because of their ability to handle long sequences of data and their facility for learning complex patterns in the data. Transformer-based architectures are a type of neural network architecture that has become the foundation for most state-of-the-art NLP models. Since their introduction in the paper, attention is all you need in 2017. Transformer architectures used to train large language models are a significant advancement in NLP. They differ from rule-based statistical and traditional machine learning approaches in their ability to capture context across long stretches of text. This is achieved through a mechanism known as attention, particularly self attention, which allows the model to weigh the importance of each word in a sentence in relation to every other word. Let's take the sentence, A young girl named Alice sits bored by a riverbank. Here's how the transformer processes and learns from it. First, the sentence is broken down into tokens. Each word and sometimes parts of words become separate tokens. For example, Alice would be a single token, while riverbank might be split into river and bank if riverbank is not in the model's vocabulary. Each token is then turned into a numerical vector that represents the token in a high dimensional space. Words in textual form are not directly usable in most machine learning algorithms which operate on numerical data. Embeddings convert words into a format that can be fed into neural networks and other algorithms for processing. Embeddings are numerical representations of words or tokens, typically in the form of vectors of real numbers. These vectors are fundamentally different from the words themselves, which are simply sequences of characters that have no meaning to humans. The embeddings, on the other hand, are designed to be processed by algorithms capturing and quantifying aspects of the words meanings, their use in different contexts, and their syntactic roles. For instance, the word Alice might be tokenized and then transformed into an embedding like this in a simplified five dimensional space for the illustration. We have our word Alice, and then we have our numerical embedding. Each number in this embedding vector is a feature learned during the training of the language model and it contributes to the model's understanding of the word Alice. The model learns these values such that when it processes different texts, the vectors can help it recognize that Alice is a name, possibly a main character, a human, and other associated attributes that it is seen in the training data. The core idea behind Transformers is the attention mechanism which allows the model to dynamically focus on different parts of the input sequence as it processes data. Self-attention is used to calculate attention scores for each token, determining how much focus it should put on other tokens in the sentence. For example, for the word follows, the model might learn that Alice and rabbit hole are important tokens to consider for understanding the context. The attention mechanism allows every token to be represented in the context of all others in the sentence, leading to a rich context aware representation of each word. Imagine each word in the sentence is a planet in our solar system. Initially, these planets are spaced based on basic relationships, like their type: noun, verb, adjective. When the context is added, it's like gravity warping space around them. The planets shift to new positions based on the other words in their vicinity. Alice might move closer to girl and surprised, rabbit hole might be pulled towards plummet and landing.






We've seen how tokenization takes text to convert it into an integer representation or an input ID that a computer can process. The value of the number doesn't really have a meaning to it and is really meant just for identification. This is where embeddings can go further in encoding more context. Embeddings are created by vectorizing the text or tokens to create representational vectors which are essentially a list of numbers. These values aren't random, but instead are created specifically and usually result in contextual information being encoded. There are many classic vectorization methods like Bag of Words, One Hot encoding, and TF-IDF to create vectors. However, they usually lack the deep contextual information we're looking for. But there are other methods like those that utilize deep learning to create vectors that can encode relationships from the text. The resulting vectors are commonly referred to as embeddings. We can think of the vector representation of the embeddings living in a vector space. Remarkably, the techniques to build these embeddings can create vectors that encode context in the vector space itself. For example, words close to one another are more similar to one another than those that are farther away. Note that I'm using two dimensions for this example, but embeddings can have an arbitrary number of dimensions. There are other relationships encoded into the embeddings. For example, you'd probably expect bark and dog to have some relationship. You'd also expect dog and cat to have a relationship to one another. What if we want to see what word for cat has the same relationship as dog and bark? We can take the cat vector and add the bark vector to it, and then remove the dogness by subtracting the dog vector. Maybe somewhat surprisingly, we'd get a resulting vector that points nearest to something like meow. These relationships are learned from the text when creating the embeddings, but you can still reuse a pre-trained embedding on a different text. But be aware it might not give the best results if your text greatly differs from the text the embeddings were learned from.