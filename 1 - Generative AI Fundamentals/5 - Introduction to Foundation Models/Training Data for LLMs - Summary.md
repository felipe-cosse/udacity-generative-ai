# Executive Summary: Training Data for Large Language Models (LLMs)

## Overview
This document summarizes the scale, scope, and composition of datasets used to train modern Large Language Models (LLMs), drawing from industry benchmarks such as Meta's LLaMA.

---

## 1. Core Scale Metrics
* **Dataset Sizes:** Modern LLMs are trained on datasets ranging from **tens to hundreds of terabytes (TB)** of plain text.
* **Scale Comparison:** 1 TB of plain text is roughly equivalent to **1 million books**. 
* **Benchmark Example:** The original LLaMA model was trained on **4.5+ TB of text** (approximately 4.5 million books).

---

## 2. Training Data Diversity (Scope)
To build robust generalization capabilities, LLMs are trained on highly diverse data sources:

| Data Source | Primary Contribution / Benefit |
| :--- | :--- |
| **Websites (Blogs, Forums, Articles)** | Formal/informal language, current trends, cultural context. |
| **Scientific & Academic Papers** | Technical terminology, complex logical concepts, expert domain knowledge. |
| **Encyclopedias (e.g., Wikipedia)** | High-quality, curated, factual general knowledge. |
| **Books & Literature** | Rich vocabulary, complex narrative structures, and long-form reasoning. |
| **Conversational Data** | Colloquial structures, dialogue flow, and human interaction patterns. |
| **Social Media Posts** | Rapidly evolving slang, abbreviations, and informal communication. |
| **Legal Documents** | Highly structured, formal phrasing, and precise syntax. |
| **Multilingual Texts** | Cross-linguistic understanding (though English remains highly dominant). |

---

## 3. Key Insights & Takeaways
* **The "Textbook" Effect:** Recent research indicates that models trained on high-quality, structured "textbook-style" data learn more efficiently and require less overall volume to achieve high performance.
* **Linguistic Disparity:** The vast majority of LLM training data is currently in English. Thousands of regional and native languages remain severely underrepresented.