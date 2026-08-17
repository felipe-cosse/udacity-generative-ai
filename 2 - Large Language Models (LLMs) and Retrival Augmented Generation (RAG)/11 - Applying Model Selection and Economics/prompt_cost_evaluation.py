# Prompt Engineering and Cost Evaluation Exercise - Starter Template
# TODO: Complete this script to optimize prompts for effectiveness and cost efficiency

# TODO: Import necessary libraries
# Hint: You'll need openai, pandas, time, json, typing, matplotlib, seaborn, datetime, numpy
import openai
from openai import OpenAI
# TODO: Add remaining imports here
import os
import pandas as pd
import time
import json
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

from dotenv import load_dotenv

load_dotenv()


# TODO: Define prompt configurations for different cost-effectiveness strategies
# Create a dictionary with three configurations:
# 1. "minimal" - lowest cost but potentially less effective
# 2. "standard" - balanced cost-performance ratio
# 3. "premium" - highest quality but most expensive
PROMPT_CONFIGS = {
    "minimal": {
        # TODO: Choose most cost-effective model (hint: gpt-4o-mini is cheapest)
        "model": "gpt-4o-mini",  # Most cost-effective model
        # TODO: Set temperature for balanced results
        "temperature": 0.7,      # Balanced temperature for consistent results
        # TODO: Set low max_tokens to control costs
        "max_tokens": 150,       # Limited tokens to control costs
        "description": "Minimal prompts with cost-effective model for budget optimization"
    },
    "standard": {
        # TODO: Choose balanced model (hint: gpt-4o offers good performance)
        "model": "gpt-4o",       # Standard model with good performance
        # TODO: Set temperature for consistent results
        "temperature": 0.7,      # Balanced temperature
        # TODO: Set moderate max_tokens
        "max_tokens": 300,       # Moderate token limit
        "description": "Standard prompts with balanced cost-performance ratio"
    },
    "premium": {
        # TODO: Choose high-performance model
        "model": "gpt-4.1",       # High-performance model
        # TODO: Set temperature for consistency (hint: lower for more consistent)
        "temperature": 0.5,      # Lower temperature for consistency
        # TODO: Set higher max_tokens for detailed responses
        "max_tokens": 500,       # Higher token limit for detailed responses
        "description": "Detailed prompts with premium model for maximum effectiveness"
    }
}

# TODO: Define pricing information for cost calculations
# Research current OpenAI pricing and fill in the rates per 1K tokens in USD
MODEL_PRICING = {
    "gpt-4o-mini": {
        # TODO: Add input token price (hint: check OpenAI pricing page)
        "input": 0.00015,   # $0.15 per 1M input tokens
        # TODO: Add output token price
        "output": 0.0006    # $0.60 per 1M output tokens
    },
    "gpt-4o": {
        # TODO: Add input token price
        "input": 0.0025,    # $2.50 per 1M input tokens
        # TODO: Add output token price
        "output": 0.01      # $10.00 per 1M output tokens
    },
    "gpt-4-turbo": {
        # TODO: Add input token price
        "input": 0.003,      # $3.00 per 1M input tokens
        # TODO: Add output token price
        "output": 0.012      # $12.00 per 1M output tokens
    }
}

# TODO: Define prompt strategies for different task categories
# Create test cases that demonstrate how prompt complexity affects quality and cost
PROMPT_STRATEGIES = [
    {
        "category": "task_completion",
        "minimal": {
            # TODO: Create a basic summarization prompt
            "prompt": "Summarize this text: [TEXT_PLACEHOLDER]",
            "description": "Basic instruction without context or examples"
        },
        "standard": {
            # TODO: Create a more detailed summarization prompt with guidance
            "prompt": "Please provide a concise summary of the following text, focusing on the main points and key takeaways: [TEXT_PLACEHOLDER]",
            "description": "Clear instruction with specific guidance"
        },
        "premium": {
            # TODO: Create a comprehensive prompt with role-playing and detailed requirements
            "prompt": "You are an expert content analyst. Please provide a comprehensive summary of the following text. Focus on: 1) Main arguments or points, 2) Supporting evidence, 3) Key conclusions. Format your response with clear headings and bullet points for easy reading: [TEXT_PLACEHOLDER]",
            "description": "Detailed instruction with role, structure, and formatting requirements"
        }
    },
    {
        "category": "creative_writing",
        "minimal": {
            # TODO: Create a simple creative writing prompt
            "prompt": "Write a story about a robot.",
            "description": "Simple creative prompt without constraints"
        },
        "standard": {
            # TODO: Create a structured creative prompt with specifications
            "prompt": "Write a short story (200-300 words) about a robot who discovers emotions for the first time. Include dialogue and describe the robot's internal experience.",
            "description": "Structured creative prompt with length and content specifications"
        },
        "premium": {
            # TODO: Create a comprehensive creative prompt with detailed requirements
            "prompt": "You are a skilled science fiction author. Write a compelling short story (200-300 words) about a robot who discovers emotions for the first time. Requirements: 1) Include meaningful dialogue between characters, 2) Show the robot's emotional journey through actions and internal thoughts, 3) Create a satisfying narrative arc with beginning, middle, and end, 4) Use vivid, descriptive language to engage the reader. Focus on the contrast between the robot's logical programming and newfound emotional experiences.",
            "description": "Comprehensive creative prompt with role-playing, detailed requirements, and quality guidelines"
        }
    },
    {
        "category": "problem_solving",
        "minimal": {
            # TODO: Create a direct business question
            "prompt": "How do I reduce customer churn?",
            "description": "Direct question without context"
        },
        "standard": {
            # TODO: Create a contextualized business question
            "prompt": "I'm running a SaaS business and experiencing 15% monthly customer churn. What are the most effective strategies to reduce customer churn and improve retention?",
            "description": "Contextualized question with specific details"
        },
        "premium": {
            # TODO: Create a comprehensive business consultation prompt
            "prompt": "You are a business consultant specializing in customer retention. I'm running a SaaS business with the following metrics: 15% monthly churn rate, $50 average monthly revenue per user, 6-month average customer lifetime. Please provide: 1) Root cause analysis of potential churn drivers, 2) Specific, actionable strategies to reduce churn, 3) Implementation timeline and resource requirements, 4) Expected ROI and success metrics. Prioritize strategies by impact and feasibility.",
            "description": "Expert consultation prompt with detailed context, specific deliverables, and structured output requirements"
        }
    }
]

# TODO: Create sample text for testing summarization prompts
# Write a substantial paragraph (200-300 words) about a relevant topic
SAMPLE_TEXT = """
TODO: Add a comprehensive text sample here that can be used for summarization testing.
This should be 200-300 words about a relevant topic like AI, technology, business, etc.
Make sure it has multiple key points that can be summarized effectively.
"""
# Sample text for testing summarization prompts
SAMPLE_TEXT = """
Artificial Intelligence (AI) has emerged as one of the most transformative technologies of the 21st century, fundamentally reshaping industries, economies, and societies worldwide. From healthcare and finance to transportation and entertainment, AI applications are revolutionizing how we work, communicate, and solve complex problems.

The current AI landscape is dominated by machine learning techniques, particularly deep learning neural networks that can process vast amounts of data to identify patterns and make predictions. Large Language Models (LLMs) like GPT-4 have demonstrated remarkable capabilities in natural language understanding and generation, enabling applications from automated customer service to creative writing assistance.

However, the rapid advancement of AI also presents significant challenges. Concerns about job displacement, algorithmic bias, privacy, and the concentration of AI capabilities in the hands of a few large corporations have sparked important debates about regulation and governance. Additionally, the environmental impact of training large AI models has raised questions about sustainability in AI development.

Looking forward, the integration of AI into everyday life will likely accelerate, with developments in areas such as autonomous vehicles, personalized medicine, and smart cities. Success in navigating this AI-driven future will require thoughtful consideration of both the tremendous opportunities and the substantial risks that these technologies present.
"""

def call_openai_api(prompt: str, config: Dict) -> Dict:
    """
    Make API call to OpenAI and capture comprehensive response metrics including cost analysis.
    
    TODO: Complete this function to:
    1. Initialize OpenAI client
    2. Make API call with given configuration
    3. Measure response time
    4. Calculate costs based on token usage
    5. Return structured results with cost metrics
    
    Args:
        prompt (str): The input prompt to send to the model
        config (Dict): Model configuration including model name, temperature, etc.
    
    Returns:
        Dict: Response data including content, performance metrics, cost analysis, and error handling
    """
    print(f"  🔄 Calling {config['model']} (temp: {config['temperature']}, max_tokens: {config['max_tokens']})...")
    
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
            logprobs=True
        )
        
        # TODO: Calculate latency in milliseconds
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # TODO: Calculate cost based on token usage and model pricing
        # Hint: cost = (tokens / 1000) * price_per_1k_tokens
        # Calculate cost based on token usage and model pricing
        model_name = config["model"]
        if model_name in MODEL_PRICING:
            input_cost = (response.usage.prompt_tokens / 1000) * MODEL_PRICING[model_name]["input"]
            output_cost = (response.usage.completion_tokens / 1000) * MODEL_PRICING[model_name]["output"]
            total_cost = input_cost + output_cost
        else:
            input_cost = output_cost = total_cost = 0.0
        
        # TODO: Structure the successful response
        # Include: response content, latency, token usage, cost analysis, success status
        # Structure the successful response with all relevant metrics
        result = {
            "response": response.choices[0].message.content,
            "latency_ms": round(latency, 2),
            "tokens_used": response.usage.total_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(total_cost, 6),
            "cost_per_token": round(total_cost / response.usage.total_tokens, 8) if response.usage.total_tokens > 0 else 0,
            "success": True,
            "error": None
        }
        
        print(f"  ✅ Success! Latency: {result['latency_ms']}ms, Tokens: {result['tokens_used']}, Cost: ${result['total_cost']:.6f}")
        return result
        
    except Exception as e:
        # TODO: Handle API errors gracefully
        # Handle API errors gracefully and return structured error response
        print(f"Error: {str(e)}")
        return {
            "response": None, "latency_ms": None, "tokens_used": None,
            "prompt_tokens": None, "completion_tokens": None,
            "input_cost": 0, "output_cost": 0, "total_cost": 0, "cost_per_token": 0,
            "success": False, "error": str(e)
        }

def score_response_quality(response: str, category: str) -> int:
    """
    Evaluate the quality of responses on a 1-5 scale based on task category.
    
    TODO: Complete this function to:
    1. Check response content for category-specific indicators
    2. Evaluate completeness and quality
    3. Return appropriate score based on criteria
    
    Args:
        response (str): The model's response to evaluate
        category (str): The task category (task_completion, creative_writing, problem_solving)
    
    Returns:
        int: Score from 1-5 where 5 is excellent quality, 1 is poor quality
    """
    if not response:
        return 0
        
    response_lower = response.lower()
    word_count = len(response.split())
    
    # TODO: Implement scoring for task_completion category
    # Task completion scoring: Focus on completeness and structure
    if category == "task_completion":
        # Check for summary indicators and structure
        summary_indicators = ["main", "key", "important", "summary", "conclusion", "points"]
        structure_indicators = ["first", "second", "finally", "additionally", "furthermore"]
        
        summary_score = sum(1 for indicator in summary_indicators if indicator in response_lower)
        structure_score = sum(1 for indicator in structure_indicators if indicator in response_lower)
        
        # Base score on content indicators and length appropriateness
        if summary_score >= 3 and word_count >= 50:
            return 5  # Excellent: comprehensive summary with good structure
        elif summary_score >= 2 and word_count >= 30:
            return 4  # Good: adequate summary with some structure
        elif summary_score >= 1 and word_count >= 20:
            return 3  # Fair: basic summary
        elif word_count >= 10:
            return 2  # Poor: minimal content
        else:
            return 1  # Very poor: insufficient content
            
    # TODO: Implement scoring for creative_writing category
    # Creative writing scoring: Focus on narrative elements and creativity
    elif category == "creative_writing":
        # Check for story elements
        narrative_elements = ["robot", "emotion", "feel", "discover", "experience", "thought"]
        dialogue_indicators = ['"', "'", "said", "asked", "replied", "exclaimed"]
        descriptive_words = ["suddenly", "slowly", "carefully", "bright", "dark", "strange", "wonderful"]
        
        narrative_score = sum(1 for element in narrative_elements if element in response_lower)
        dialogue_score = sum(1 for indicator in dialogue_indicators if indicator in response)
        descriptive_score = sum(1 for word in descriptive_words if word in response_lower)
        
        # Evaluate story completeness and creativity
        if narrative_score >= 4 and dialogue_score >= 2 and word_count >= 150:
            return 5  # Excellent: complete story with dialogue and good length
        elif narrative_score >= 3 and word_count >= 100:
            return 4  # Good: solid story with adequate development
        elif narrative_score >= 2 and word_count >= 50:
            return 3  # Fair: basic story elements present
        elif narrative_score >= 1:
            return 2  # Poor: minimal story development
        else:
            return 1  # Very poor: no clear story structure
            
    # TODO: Implement scoring for problem_solving category
    # Problem solving scoring: Focus on actionable advice and comprehensiveness
    elif category == "problem_solving":
        # Check for business strategy elements
        strategy_words = ["strategy", "approach", "solution", "recommend", "implement", "improve"]
        analysis_words = ["analyze", "identify", "cause", "reason", "factor", "metric"]
        action_words = ["action", "step", "plan", "timeline", "measure", "track"]
        
        strategy_score = sum(1 for word in strategy_words if word in response_lower)
        analysis_score = sum(1 for word in analysis_words if word in response_lower)
        action_score = sum(1 for word in action_words if word in response_lower)
        
        # Evaluate comprehensiveness and actionability
        total_score = strategy_score + analysis_score + action_score
        if total_score >= 6 and word_count >= 100:
            return 5  # Excellent: comprehensive analysis with actionable strategies
        elif total_score >= 4 and word_count >= 75:
            return 4  # Good: solid advice with some analysis
        elif total_score >= 2 and word_count >= 50:
            return 3  # Fair: basic recommendations
        elif total_score >= 1:
            return 2  # Poor: minimal useful content
        else:
            return 1  # Very poor: no actionable advice
    
    return 3  # Default middle score

def calculate_cost_effectiveness(quality_score: int, total_cost: float) -> float:
    """
    Calculate cost-effectiveness ratio for prompt strategies.
    
    TODO: Complete this function to:
    1. Handle zero cost cases
    2. Calculate quality points per dollar
    3. Return meaningful ratio for comparison
    
    Args:
        quality_score (int): Quality score from 1-5
        total_cost (float): Total cost in USD for the API call
    
    Returns:
        float: Cost-effectiveness ratio (higher is better)
    """
    # TODO: Handle zero cost case
    if total_cost == 0:
        return 0.0
    
    # TODO: Calculate and return cost-effectiveness ratio
    # Hint: quality_score / total_cost, multiply by 1000 for readability
    # Calculate quality points per dollar spent
    # Multiply by 1000 to get a more readable number
    return (quality_score / total_cost) * 1000

def test_prompt_strategy(category: str, strategy_type: str):
    """
    Test a specific prompt strategy and analyze its cost-effectiveness.
    
    TODO: Complete this function to:
    1. Find the specified strategy from PROMPT_STRATEGIES
    2. Get the appropriate configuration
    3. Make API call and evaluate results
    4. Display comprehensive metrics
    5. Return structured results
    
    Args:
        category (str): The task category to test
        strategy_type (str): The prompt strategy type (minimal, standard, premium)
    
    Returns:
        dict: Results including quality scores, costs, and effectiveness metrics
    """
    # TODO: Find the specified strategy
    strategy_data = None
    # Hint: Loop through PROMPT_STRATEGIES to find matching category
    for strategy in PROMPT_STRATEGIES:
        if strategy["category"] == category:
            strategy_data = strategy
            break

    if not strategy_data:
        print(f"❌ Category '{category}' not found")
        return None
    
    # TODO: Get prompt info and config
    prompt_info = strategy_data[strategy_type]
    config = PROMPT_CONFIGS[strategy_type]
    
    print(f"\n🧪 TESTING PROMPT STRATEGY: {category.upper()} - {strategy_type.upper()}")
    print(f"Description: {prompt_info['description']}")
    print(f"Model: {config['model']} | Temp: {config['temperature']} | Max Tokens: {config['max_tokens']}")
    print("=" * 80)
    
    # TODO: Prepare the prompt (replace placeholder if needed)
    prompt = prompt_info["prompt"]
    # Hint: Replace [TEXT_PLACEHOLDER] with SAMPLE_TEXT if present
    if "[TEXT_PLACEHOLDER]" in prompt:
        prompt = prompt.replace("[TEXT_PLACEHOLDER]", SAMPLE_TEXT)
    
    # TODO: Make API call with current configuration
    result = call_openai_api(prompt, config)
    
    if result['success']:
        print(result)
        # TODO: Score the response quality
        quality_score = score_response_quality(result['response'], category)
        
        # TODO: Calculate cost-effectiveness
        cost_effectiveness = calculate_cost_effectiveness(quality_score, result['total_cost'])
        
        # TODO: Display results with clear formatting
        print(f"\n📝 RESPONSE:")
        print("-" * 60)
        print(result['response'])
        print("-" * 60)
        
        print(f"\n📊 METRICS:")
        print(f"✅ Quality Score: {quality_score}/5")
        print(f"⏱️  Latency: {result['latency_ms']}ms")
        print(f"🔢 Tokens Used: {result['tokens_used']} (Input: {result['prompt_tokens']}, Output: {result['completion_tokens']})")
        print(f"💰 Cost Breakdown:")
        print(f"   Input Cost: ${result['input_cost']:.6f}")
        print(f"   Output Cost: ${result['output_cost']:.6f}")
        print(f"   Total Cost: ${result['total_cost']:.6f}")
        print(f"   Cost per Token: ${result['cost_per_token']:.8f}")
        print(f"📈 Cost-Effectiveness: {cost_effectiveness:.2f} quality points per $1000")
        
        # TODO: Return structured results
        return {
            'category': category,
            'strategy_type': strategy_type,
            'response': result['response'],
            'quality_score': quality_score,
            'latency_ms': result['latency_ms'],
            'tokens_used': result['tokens_used'],
            'prompt_tokens': result['prompt_tokens'],
            'completion_tokens': result['completion_tokens'],
            'total_cost': result['total_cost'],
            'cost_effectiveness': cost_effectiveness,
            'model': config['model']
        }
    else:
        print(f"❌ Failed: {result['error']}")
        return None

def compare_prompt_strategies(category: str):
    """
    Compare all prompt strategies for a given category and analyze trade-offs.
    
    TODO: Complete this function to:
    1. Test all three strategy types for the given category
    2. Collect and analyze results
    3. Create comparison table using pandas
    4. Provide recommendations based on different criteria
    
    Args:
        category (str): The task category to compare strategies for
    
    Returns:
        dict: Comparison results with recommendations
    """
    print(f"\n🔍 COMPARING PROMPT STRATEGIES FOR: {category.upper()}")
    print("=" * 80)
    
    results = {}
    strategy_types = ["minimal", "standard", "premium"]
    
    # TODO: Test each strategy type
    for strategy_type in strategy_types:
        # TODO: Call test_prompt_strategy and store results
        # Add small delay between calls to avoid rate limiting
        result = test_prompt_strategy(category, strategy_type)
        if result:
            results[strategy_type] = result
        
        # Add a small delay between API calls to avoid rate limiting
        time.sleep(1)
    
    # TODO: Analyze and display comparison
    if len(results) > 1:
        print(f"\n📊 STRATEGY COMPARISON SUMMARY:")
        print("=" * 80)
        
        # TODO: Create comparison table using pandas
        # Include: Strategy, Quality, Cost, Tokens, Cost-Effectiveness, Model
        # Create comparison table
        comparison_data = []
        for strategy_type, data in results.items():
            comparison_data.append({
                'Strategy': strategy_type.capitalize(),
                'Quality': f"{data['quality_score']}/5",
                'Cost': f"${data['total_cost']:.6f}",
                'Tokens': data['tokens_used'],
                'Cost-Effectiveness': f"{data['cost_effectiveness']:.2f}",
                'Model': data['model']
            })

        # Display comparison table
        df = pd.DataFrame(comparison_data)
        print(df.to_string(index=False))

        # TODO: Provide recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        # TODO: Find and display best cost-effectiveness
        # Find best cost-effectiveness
        best_ce = max(results.values(), key=lambda x: x['cost_effectiveness'])
        print(f"🏆 Best Cost-Effectiveness: {best_ce['strategy_type'].capitalize()} strategy")
        print(f"   Quality: {best_ce['quality_score']}/5, Cost: ${best_ce['total_cost']:.6f}")
        # TODO: Find and display highest quality
        # Find highest quality
        best_quality = max(results.values(), key=lambda x: x['quality_score'])
        print(f"⭐ Highest Quality: {best_quality['strategy_type'].capitalize()} strategy")
        print(f"   Quality: {best_quality['quality_score']}/5, Cost: ${best_quality['total_cost']:.6f}")
        # TODO: Find and display lowest cost
        # Find lowest cost
        lowest_cost = min(results.values(), key=lambda x: x['total_cost'])
        print(f"💰 Lowest Cost: {lowest_cost['strategy_type'].capitalize()} strategy")
        print(f"   Quality: {lowest_cost['quality_score']}/5, Cost: ${lowest_cost['total_cost']:.6f}")
        
        return results
    else:
        print("❌ Insufficient results for comparison")
        return results

# TODO: Example usage - uncomment and test when ready
# Test a single strategy
# minimal_summary = test_prompt_strategy("task_completion", "minimal")
task_completion_results = compare_prompt_strategies("task_completion")

# TODO: Additional test examples you can run:
# Compare all strategies for a category
# task_completion_results = compare_prompt_strategies("task_completion")
# creative_writing_results = compare_prompt_strategies("creative_writing")
# problem_solving_results = compare_prompt_strategies("problem_solving")

# Single strategy tests:
# standard_story = test_prompt_strategy("creative_writing", "standard")
# premium_business = test_prompt_strategy("problem_solving", "premium")

"""
EXERCISE COMPLETION CHECKLIST:
□ Import all necessary libraries
□ Complete PROMPT_CONFIGS with appropriate models and parameters
□ Fill in MODEL_PRICING with current OpenAI pricing
□ Create comprehensive PROMPT_STRATEGIES for all categories and types
□ Write substantial SAMPLE_TEXT for summarization testing
□ Implement call_openai_api() function with cost calculation
□ Complete score_response_quality() with category-specific logic
□ Implement calculate_cost_effectiveness() function
□ Complete test_prompt_strategy() function
□ Implement compare_prompt_strategies() function
□ Test your implementation with the example usage
□ Add your own API key and test the complete workflow

BONUS CHALLENGES:
□ Add visualization of cost vs quality trade-offs using matplotlib
□ Implement batch testing with multiple runs for statistical analysis
□ Add confidence intervals for quality scores
□ Create a budget optimization function that recommends strategies based on cost constraints
□ Add support for custom prompt templates
□ Implement A/B testing framework for prompt comparison
□ Add export functionality for results (CSV, JSON)
□ Create a cost forecasting tool based on usage patterns
"""
