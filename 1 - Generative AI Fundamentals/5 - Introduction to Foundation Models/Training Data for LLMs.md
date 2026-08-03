# Full Course Text: Training Data for LLMs

## Course Module: Introduction to Foundation Models

Large Language Models (LLMs) can be terabytes in size, which is huge. This raises a natural question: how much data does it actually take to train one of these models? This lesson explores the massive scale, scope, and specific types of text data, from websites to books, that power modern LLMs.

---

## The Scale of LLM Training Data

Modern LLMs are often trained on datasets comprising tens to hundreds of terabytes of text data. To put this into perspective, one terabyte (1 TB) of plain text is roughly equivalent to about a million books worth of content. This means that an LLM could be trained on the equivalent of tens to hundreds of millions of books. 

In this industry, things move so fast that the scale of training data is constantly increasing. For a specific historical milestone:
* **LLaMA (2023):** The original LLaMA model was trained on more than **4.5 terabytes of text data**, equivalent to roughly 4.5 million books.

During this period, major AI labs still routinely published their training mixtures. Today, the scale and scope have grown exponentially.

---

## The Scope: Types of Training Data

Training data is not only massive in volume but also vast in scope, covering almost every subject matter accessible in written form. Below is an overview of the primary data categories utilized:

### 1. Websites
* **Description:** Content crawled from billions of web pages (e.g., via the Common Crawl repository, which contains over 25 billion pages).
* **Impact:** Provides informal and formal language, blogs, articles, forums, and real-time cultural trends.

### 2. Scientific and Academic Papers
* **Description:** Peer-reviewed journals, preprints, and academic publications.
* **Impact:** Teaches the model highly technical vocabulary, rigorous logic, and complex domain concepts.

### 3. Encyclopedias
* **Description:** Curated knowledge databases like Wikipedia.
* **Impact:** Serves as a foundational baseline for factual, cross-disciplinary general knowledge.

### 4. Books and Literature
* **Description:** Classic literature, modern fiction/non-fiction, and textbooks.
* **Impact:** Exposes the model to sophisticated prose, diverse vocabulary, and advanced narrative structures. 
* *Note:* Studies demonstrate that training on high-quality "textbook-format" data substantially accelerates model convergence and data efficiency.

### 5. Conversational Data
* **Description:** Dialogue transcripts, plays, screenplays, and chatbot records.
* **Impact:** Helps the model master the nuances of natural dialogue, colloquialisms, and conversational flow.

### 6. Social Media Posts
* **Description:** Short-form public text from various social platforms.
* **Impact:** Allows the model to parse modern internet slang, abbreviations, and informal shorthand.

### 7. Legal Documents
* **Description:** Legislation, court filings, and corporate contracts.
* **Impact:** Trains the network to parse dense, highly formal legalese and complex logical constraints.

### 8. Multilingual Texts
* **Description:** Parallel and monolingual corpora in multiple global languages.
* **Impact:** Powers translation and cross-lingual comprehension capabilities. 

---

## The Representation Gap
Despite efforts to curate global datasets, the vast majority of current training data is in English. Thousands of regional and minority languages are heavily underrepresented, presenting an ongoing challenge for equitable global AI performance.




We've seen that LLMs are a type of foundation model that can range in size from hundreds of megabytes to multiple terabytes. That's huge. A natural question to ask is how much data does it take to train these things? Modern LLMs are often trained on datasets comprising tens to hundreds of terabytes of text data. To put this into perspective, one terabyte of plain text is roughly equivalent to about a million books worth of content. This means that an LLM could be trained on the equivalent of tens to hundreds of millions of books. In fact, in this industry, things move so fast, by the time you are watching this video, the scale of training data will likely have already increased. As seen here, the original LLaMA model was trained on more than 4.5 terabytes of text data, which is equivalent to about 4.5 million books. You'll notice that training data isn't just large in volume, but it's also vast in scope, covering practically every subject matter accessible in written form. In this image, you can see the range of sources used for the LLaMA model, including Wikipedia, in the CommonCrawl, which is a repository of web crawl data composed of over 25 billion web pages. This was 2023 when the large companies training these models still publish this information. Fast forward several years, and you can just imagine how much the size and scope of data have grown when training these models. Here's an overview of some of the types of data used for training these models. We have websites, content from a multitude of websites, including articles, blogs, and forums. This is readily available in abundance and contributes to the understanding of formal and informal language, as well as current trends. We also have scientific and academic papers, and these help the model learn technical language and complex concepts, particularly useful for queries that require detailed expert knowledge. Encyclopedia such as Wikipedia. Comprehensive and factual entries from encyclopedias give the model a basis for general knowledge across an array of topics. Books and literature: This includes classic literature for modern books and textbooks across various genres and subjects, providing a rich vocabulary in complex sentence structure. Interestingly, one study showed that models trained on data presented in textbook form were able to be trained more easily and with less data. Conversational data: Transcripts of conversations, dialogues from plays, and screenplays, and texts from chat bots train the model in the nuances of dialogue and colloquial speech. Social media posts: This helps a model grasp the latest linguistic trends, abbreviations, and the informal, often concise way people communicate online. Legal documents: Contracts, legal filings, and legislation texts train the model to understand formal language and complex sentence structures. Finally, multilingual texts. To create models that understand multiple languages, texts in various languages are included. It must be noted that still most of the data used to train these models are in English. Plus, there are still thousands of languages that are woefully underrepresented in these datasets.