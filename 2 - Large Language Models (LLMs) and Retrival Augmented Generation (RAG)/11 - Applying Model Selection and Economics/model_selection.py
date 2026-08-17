# Model Selection Exercise - Starter Template
# TODO: Complete this script to compare different LLM configurations for specific tasks

# TODO: Import necessary libraries
# Hint: You'll need openai, pandas, time, json, typing, datetime, numpy
import openai
from openai import OpenAI
# TODO: Add remaining imports here
import os
import pandas as pd
import time
import json
from typing import Dict, List, Tuple
from datetime import datetime
import numpy as np

from dotenv import load_dotenv

load_dotenv()

# TODO: Define model configurations for different use cases
# Create a dictionary with two configurations:
# 1. "reasoning_optimized" - for logical, step-by-step reasoning
# 2. "generation_optimized" - for creative, varied responses
MODEL_CONFIGS = {
    "reasoning_optimized": {
        # TODO: Choose appropriate model for reasoning (hint: o-series models excel at reasoning)
        "model": "o4-mini",  # O-series models excel at reasoning tasks
        # TODO: Set temperature for consistent outputs (hint: lower values = more consistent)
        "temperature": 1.0,    # Only 1 accepted for this model
        # TODO: Set max_tokens for response length
        "max_tokens": 500,   # Sufficient tokens for detailed reasoning
        "description": "Uses o-series model for best logical, step-by-step reasoning"
    },
    "generation_optimized": {
        # TODO: Choose appropriate model for generation (hint: gpt-4o is excellent for creativity)
        "model": "gpt-4o",   # GPT-4o provides excellent creative capabilities
        # TODO: Set temperature for creative variation (hint: higher values = more creative)
        "temperature": 1.0,  # Higher temperature encourages creative variation
        # TODO: Set max_tokens for response length
        "max_tokens": 500,   # Allow for longer creative responses
        # TODO: Add top_p parameter for nucleus sampling
        "top_p": 0.95,      # Nucleus sampling for diverse but coherent outputs
        "description": "High temperature for creative, varied responses"
    }
}

# TODO: Define reasoning test prompts
# Create a list of dictionaries, each containing:
# - "id": unique identifier
# - "prompt": the test question
# - "expected_answer": what the correct response should be
# - "description": what this test evaluates
REASONING_PROMPTS = [
    {
        "id": "math_word_problem",
        # TODO: Create a math word problem (hint: simple arithmetic with context)
        "prompt": "Given the following passage, answer the factual question: Passage: 'Sarah inherits 5 apples. She gives two to Tom and buys three more at the store. How many apples does Sarah have now?'",
        # TODO: Provide the expected numerical answer
        "expected_answer": "6 apples",  # 5 - 2 + 3 = 6
        "description": "Simple arithmetic word problem"
    },
    {
        "id": "logical_deduction",
        # TODO: Create a logical reasoning problem (hint: if-then statements)
        "prompt": "Analyze this logical sequence: If all cats are animals, and Fluffy is a cat, what can we conclude about Fluffy? Provide your reasoning step by step.",
        # TODO: Provide the logical conclusion
        "expected_answer": "Fluffy is an animal",  # Basic syllogistic reasoning
        "description": "Basic syllogistic reasoning"
    },
    {
        "id": "business_calculation",
        # TODO: Create a multi-step percentage calculation problem
        "prompt": "A company's revenue increased by 20% in Q1, then decreased by 15% in Q2. If Q1 revenue was $100,000, what was the Q2 revenue? Show your calculation.",
        # TODO: Provide the calculated result
        "expected_answer": "$102,000",  # 100,000 * 1.20 * 0.85 = 102,000
        "description": "Multi-step business calculation"
    }
]

# TODO: Define generation test prompts
# Create a list of dictionaries for creative tasks:
GENERATION_PROMPTS = [
    {
        "id": "creative_storytelling",
        # TODO: Create a creative writing prompt
        "prompt": "Write a two-paragraph creative story about a cat that travels to outer space.",
        "description": "Open-ended creative writing task requiring imagination and narrative skills"
    },
    {
        "id": "marketing_copy",
        # TODO: Create a marketing content generation prompt
        "prompt": "Create an engaging product description for a revolutionary smart water bottle that tracks hydration and reminds users to drink water.",
        "description": "Persuasive marketing content requiring creativity and sales language"
    },
    {
        "id": "creative_dialogue",
        # TODO: Create a dialogue writing prompt
        "prompt": "Write a humorous dialogue between a coffee cup and a tea bag arguing about which beverage is superior.",
        "description": "Character-based creative writing requiring humor and personality"
    }
]

def call_openai_api(prompt: str, config: Dict) -> Dict:
    """
    Make API call to OpenAI and capture comprehensive response metrics.
    
    TODO: Complete this function to:
    1. Initialize OpenAI client
    2. Make API call with given configuration
    3. Measure response time
    4. Return structured results with metrics
    
    Args:
        prompt (str): The input prompt to send to the model
        config (Dict): Model configuration including model name, temperature, etc.
    
    Returns:
        Dict: Response data including content, performance metrics, and error handling
    """
    print(f"  🔄 Calling {config['model']} (temp: {config['temperature']})...")
    
    # TODO: Record start time for latency measurement
    start_time = time.time()  # Start timing the API call
    
    try:
        # TODO: Initialize OpenAI client with your API key
        # SECURITY NOTE: Use environment variables for API keys in production
        client = OpenAI(
            base_url="https://openai.vocareum.com/v1",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # TODO: Make the API call
        # Hint: Use client.chat.completions.create() with:
        # - model from config
        # - messages with user role and prompt content
        # - temperature from config
        # - max_completion_tokens from config
        # Make the API call with specified configuration
        response = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=config["temperature"],
            max_completion_tokens=config["max_tokens"],
            # Note: top_p is commented out as it may not be supported by all models
            #top_p=config["top_p"]
        )
        
        # TODO: Calculate latency in milliseconds
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # TODO: Structure the successful response
        # Include: response content, latency, token usage, success status
        # Structure the successful response with all relevant metrics
        result = {
            "response": response.choices[0].message.content,
            "latency_ms": round(latency, 2),
            "tokens_used": response.usage.total_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "success": True,
            "error": None
        }
        print(response)  # Debug output to see full API response
        
        print(f"  ✅ Success! Latency: {result['latency_ms']}ms, Tokens: {result['tokens_used']}")
        return result
        
    except Exception as e:
        # TODO: Handle API errors gracefully
        # Handle API errors gracefully and return structured error response
        print(f"Error: {str(e)}")
        return {
            "response": None, "latency_ms": None, "tokens_used": None,
            "prompt_tokens": None, "completion_tokens": None,
            "success": False, "error": str(e)
        }

def score_reasoning_accuracy(response: str, expected: str, task_id: str) -> int:
    """
    Evaluate the accuracy of reasoning responses on a 1-5 scale.
    
    This function implements task-specific scoring logic to assess how well
    the model performed logical reasoning, mathematical calculations, or deductions.
    
    Args:
        response (str): The model's response to evaluate
        expected (str): The expected correct answer
        task_id (str): Identifier for the specific reasoning task
    
    Returns:
        int: Score from 1-5 where 5 is perfect accuracy, 1 is poor/incorrect
    """
    if not response:
        return 0  # No response provided
        
    response_lower = response.lower()
    
    # Math word problem scoring: Check for correct numerical answer and context
    if task_id == "math_word_problem":
        if "6" in response and any(word in response_lower for word in ["apple", "total", "has"]):
            return 5  # Perfect: correct answer with proper context
        elif "6" in response:
            return 4  # Good: correct answer but missing context
        elif any(num in response for num in ["5", "7", "8"]):
            return 2  # Poor: close but incorrect calculation
        else:
            return 1  # Very poor: completely wrong
            
    # Logical deduction scoring: Check for correct conclusion and reasoning
    elif task_id == "logical_deduction":
        if "animal" in response_lower and "fluffy" in response_lower:
            # Perfect if includes reasoning words, good if just has correct conclusion
            return 5 if "therefore" in response_lower or "conclude" in response_lower else 4
        elif "animal" in response_lower:
            return 3  # Partial understanding
        else:
            return 1  # Missed the logical connection
            
    # Business calculation scoring: Multi-step percentage calculation
    elif task_id == "business_calculation":
        # Check for correct final answer: 100,000 * 1.20 * 0.85 = 102,000
        if any(answer in response.replace(",", "").replace("$", "") for answer in ["102000", "102,000"]):
            return 5  # Perfect calculation
        elif "120000" in response.replace(",", "") or "85000" in response.replace(",", ""):
            return 2  # Partial calculation (got one step right)
        else:
            return 1  # Incorrect calculation
    
    return 3  # Default middle score for unrecognized tasks

def score_creativity(response: str, task_id: str) -> int:
    """
    Evaluate the creativity and quality of generated content on a 1-5 scale.
    
    This function assesses creative responses based on vocabulary richness,
    task-specific elements, and overall quality of the generated content.
    
    Args:
        response (str): The model's creative response to evaluate
        task_id (str): Identifier for the specific generation task
    
    Returns:
        int: Score from 1-5 where 5 is highly creative, 1 is poor quality
    """
    if not response:
        return 0  # No response provided
        
    # Calculate vocabulary richness as a creativity indicator
    word_count = len(response.split())
    unique_words = len(set(response.lower().split()))
    vocabulary_richness = unique_words / word_count if word_count > 0 else 0
    
    base_score = 3  # Start with middle score
    
    # Creative storytelling scoring: Look for space and cat elements
    if task_id == "creative_storytelling":
        space_elements = ["space", "rocket", "planet", "star", "galaxy", "astronaut", "orbit", "cosmic"]
        cat_elements = ["cat", "whiskers", "meow", "paw", "tail", "feline"]
        elements_found = sum(1 for element in space_elements + cat_elements if element in response.lower())
        base_score = min(5, 2 + elements_found // 2)  # Score based on thematic elements
        
    # Marketing copy scoring: Look for persuasive language and product features
    elif task_id == "marketing_copy":
        marketing_words = ["revolutionary", "smart", "innovative", "perfect", "amazing", "ultimate", "advanced", "cutting-edge"]
        features = ["track", "remind", "hydration", "water", "bottle", "app", "notification"]
        marketing_found = sum(1 for word in marketing_words + features if word in response.lower())
        base_score = min(5, 2 + marketing_found // 3)  # Score based on marketing language
        
    # Creative dialogue scoring: Look for dialogue indicators and beverage references
    elif task_id == "creative_dialogue":
        dialogue_indicators = ["said", "replied", "argued", "exclaimed", "retorted", "declared"]
        beverage_words = ["coffee", "tea", "caffeine", "flavor", "aroma", "brew"]
        dialogue_found = sum(1 for word in dialogue_indicators + beverage_words if word in response.lower())
        base_score = min(5, 2 + dialogue_found // 3)  # Score based on dialogue quality
    
    # Adjust score based on vocabulary richness
    if vocabulary_richness > 0.8:
        base_score = min(5, base_score + 1)  # Bonus for rich vocabulary
    elif vocabulary_richness < 0.5:
        base_score = max(1, base_score - 1)  # Penalty for repetitive language
        
    return base_score

def test_reasoning_task(task_index=0):
    """
    Test a single reasoning task with both model configurations.
    
    This function demonstrates how to compare different models on reasoning tasks,
    measuring both accuracy and performance metrics.
    
    Args:
        task_index (int): Index of the reasoning task to test (0-2)
    
    Returns:
        dict: Results from both model configurations including scores and metrics
    """
    task = REASONING_PROMPTS[task_index]
    print(f"\n🧠 TESTING REASONING TASK: {task['id']}")
    print(f"Description: {task['description']}")
    print(f"Expected Answer: {task['expected_answer']}")
    print("=" * 60)
    
    results = {}
    
    # Test each model configuration on the same reasoning task
    for config_name, config in MODEL_CONFIGS.items():
        print(f"\n🤖 Testing {config_name}:")
        print(f"   Model: {config['model']} | Temp: {config['temperature']}")
        
        # Make API call with current configuration
        result = call_openai_api(task['prompt'], config)
        
        if result['success']:
            # Score the reasoning accuracy of the response
            accuracy_score = score_reasoning_accuracy(result['response'], task['expected_answer'], task['id'])
            
            # Display results with clear formatting
            print(f"\n📝 RESPONSE:")
            print("-" * 40)
            print(result['response'])
            print("-" * 40)
            print(f"✅ Accuracy Score: {accuracy_score}/5")
            print(f"⏱️  Latency: {result['latency_ms']}ms")
            print(f"🔢 Tokens: {result['tokens_used']}")
            
            # Store results for comparison
            results[config_name] = {
                'response': result['response'],
                'accuracy_score': accuracy_score,
                'latency_ms': result['latency_ms'],
                'tokens_used': result['tokens_used']
            }
        else:
            print(f"Failed: {result['error']}")

    return results


def test_generation_task(task_index=0):
    """
    Test a single generation task with both model configurations.
    
    This function demonstrates how to compare different models on creative tasks,
    measuring both creativity quality and performance metrics.
    
    Args:
        task_index (int): Index of the generation task to test (0-2)
    
    Returns:
        dict: Results from both model configurations including scores and metrics
    """
    task = GENERATION_PROMPTS[task_index]
    print(f"\n🎨 TESTING GENERATION TASK: {task['id']}")
    print(f"Description: {task['description']}")
    print("=" * 60)
    
    results = {}
    
    # Test each model configuration on the same generation task
    for config_name, config in MODEL_CONFIGS.items():
        print(f"\n🤖 Testing {config_name}:")
        print(f"   Model: {config['model']} | Temp: {config['temperature']}")
        
        # Make API call with current configuration
        result = call_openai_api(task['prompt'], config)
        
        if result['success']:
            # Score the creativity quality of the response
            creativity_score = score_creativity(result['response'], task['id'])
            
            # Display results with clear formatting
            print(f"\n📝 RESPONSE:")
            print("-" * 40)
            print(result['response'])
            print("-" * 40)
            print(f"🎨 Creativity Score: {creativity_score}/5")
            print(f"⏱️  Latency: {result['latency_ms']}ms") 
            print(f"🔢 Tokens: {result['tokens_used']}")
            
            # Store results for comparison
            results[config_name] = {
                'response': result['response'],
                'creativity_score': creativity_score,
                'latency_ms': result['latency_ms'],
                'tokens_used': result['tokens_used']
            }
        else:
            print(f"Failed: {result['error']}")
    
    return results

# TODO: Example usage - uncomment and test when ready
# Test the first generation task to demonstrate the comparison
# generation_results_1 = test_generation_task(0)
# Example usage: Run the first generation task to demonstrate the comparison
# This will test both model configurations on the creative storytelling task
generation_results_1 = test_generation_task(0)
reasoning_results_1 = test_reasoning_task(0)

# TODO: Additional test examples you can run:
# reasoning_results_1 = test_reasoning_task(0)  # Math problem
# reasoning_results_2 = test_reasoning_task(1)  # Logic deduction  
# reasoning_results_3 = test_reasoning_task(2)  # Business calculation
# generation_results_2 = test_generation_task(1)  # Marketing copy
# generation_results_3 = test_generation_task(2)  # Dialogue

"""
EXERCISE COMPLETION CHECKLIST:
□ Import all necessary libraries
□ Complete MODEL_CONFIGS with appropriate models and parameters
□ Fill in all REASONING_PROMPTS with test questions and expected answers
□ Fill in all GENERATION_PROMPTS with creative writing tasks
□ Implement call_openai_api() function with proper API calls and error handling
□ Test your implementation with the example usage
□ Add your own API key and test the complete workflow

BONUS CHALLENGES:
□ Add visualization of results using matplotlib/seaborn
□ Implement statistical significance testing
□ Add cost calculation for API usage
□ Create a summary report function
□ Add more diverse test prompts
□ Implement confidence intervals for scores
"""
