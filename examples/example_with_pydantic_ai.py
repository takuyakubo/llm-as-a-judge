#!/usr/bin/env python3
"""
Example of using the LLM-as-a-Judge framework with Pydantic AI framework integration

Pydantic AI is a Python agent framework that provides type-safe, production-ready
access to multiple LLM providers (OpenAI, Anthropic, Google Gemini, etc.).
"""
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.criteria import Criteria
from src.evaluator import Evaluator
from src.llm_providers import create_llm_provider, LLMConfig


def main():
    # Load environment variables
    load_dotenv()
    
    # Load evaluation criteria from rubric
    with open('tests/rubric.json', 'r', encoding='utf-8') as f:
        rubric_data = json.load(f)
    
    criteria = Criteria.from_dict(rubric_data)
    
    # Example document to evaluate
    sample_document = """
    人工知能の発展は、私たちの社会に革命的な変化をもたらしています。
    特に、大規模言語モデル（LLM）の登場により、テキスト生成や理解の分野で
    驚異的な進歩が見られます。
    
    これらの技術は、教育、医療、ビジネスなど様々な分野で応用されており、
    作業の効率化や新たな価値の創造に貢献しています。一方で、倫理的な課題や
    雇用への影響など、慎重に検討すべき問題も存在します。
    
    今後は、技術の発展と社会的な配慮のバランスを取りながら、
    より良い未来を構築していくことが重要です。
    """
    
    print("=== LLM-as-a-Judge Evaluation Example ===\n")
    
    # Example 1: Using Pydantic AI framework with default configuration
    print("1. Using Pydantic AI framework with default model (gpt-4o-mini):")
    print("-" * 50)
    
    evaluator = Evaluator(criteria)  # Will use default Pydantic AI framework
    
    try:
        result = evaluator.evaluate_document(sample_document, document_id="example_001")
        
        print(f"Model used: {result.model_used}")
        print(f"Overall score: {result.overall_score:.2f}")
        print("\nDetailed scores:")
        for score in result.scores:
            print(f"\n{score.criterion_name}:")
            print(f"  Score: {score.score}/5")
            print(f"  Confidence: {score.confidence:.2f}")
            print(f"  Reasoning: {score.reasoning}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set OPENAI_API_KEY in your environment or .env file")
    
    # Example 2: Using Pydantic AI framework with Claude
    print("\n\n2. Using Pydantic AI framework with Claude:")
    print("-" * 50)
    
    claude_config = LLMConfig(
        model_name="claude-3-5-haiku-latest",
        temperature=0.3,
        max_tokens=2000
    )
    
    # Create provider using Pydantic AI framework
    claude_provider = create_llm_provider("pydantic_ai", claude_config)
    evaluator_claude = Evaluator(criteria, llm_provider=claude_provider)
    
    try:
        result = evaluator_claude.evaluate_document(sample_document, document_id="example_002")
        
        print(f"Model used: {result.model_used}")
        print(f"Overall score: {result.overall_score:.2f}")
        print("\nDetailed scores:")
        for score in result.scores:
            print(f"\n{score.criterion_name}:")
            print(f"  Score: {score.score}/5")
            print(f"  Confidence: {score.confidence:.2f}")
            print(f"  Reasoning: {score.reasoning}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set ANTHROPIC_API_KEY in your environment or .env file")
    
    # Example 3: Using direct OpenAI API (bypassing Pydantic AI framework)
    print("\n\n3. Using direct OpenAI API (not using Pydantic AI framework):")
    print("-" * 50)
    
    openai_config = LLMConfig(
        model_name="gpt-3.5-turbo",
        temperature=0.2,
        max_tokens=1500
    )
    
    openai_provider = create_llm_provider("openai", openai_config)
    evaluator_openai = Evaluator(criteria, llm_provider=openai_provider)
    
    try:
        result = evaluator_openai.evaluate_document(sample_document, document_id="example_003")
        
        print(f"Model used: {result.model_used}")
        print(f"Overall score: {result.overall_score:.2f}")
        print("\nTop scoring criteria:")
        sorted_scores = sorted(result.scores, key=lambda x: x.score, reverse=True)
        for score in sorted_scores[:3]:
            print(f"- {score.criterion_name}: {score.score}/5")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set OPENAI_API_KEY in your environment or .env file")
    
    # Example 4: Export results to JSON
    print("\n\n4. Exporting results to JSON:")
    print("-" * 50)
    
    if 'result' in locals():
        output_file = 'evaluation_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        print(f"Results exported to {output_file}")


if __name__ == "__main__":
    main()