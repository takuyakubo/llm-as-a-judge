#!/usr/bin/env python3
"""Command Line Interface for LLM as a Judge framework."""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from .criteria import Criteria
from .evaluator import Evaluator
from .llm_providers import create_llm_provider, LLMConfig


def evaluate_document(args):
    """Evaluate a document using the specified rubric."""
    # Load environment variables
    load_dotenv()
    
    # Load criteria
    criteria = Criteria.from_json_file(args.rubric)
    
    # Create evaluator
    if args.mock:
        # Mock mode - no provider needed
        evaluator = Evaluator(criteria)
    else:
        # Set up LLM provider
        model_name = args.model
        if not model_name:
            # Default models per provider
            default_models = {
                'pydantic_ai': os.getenv('DEFAULT_MODEL', 'gpt-4o-mini'),
                'openai': 'gpt-4o-mini',
                'anthropic': 'claude-3-5-haiku-latest'
            }
            model_name = default_models.get(args.provider, 'gpt-4o-mini')
        
        llm_config = LLMConfig(
            model_name=model_name,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
        
        try:
            llm_provider = create_llm_provider(args.provider, llm_config)
            evaluator = Evaluator(criteria, llm_provider=llm_provider)
        except Exception as e:
            print(f"Error: Failed to initialize LLM provider: {e}", file=sys.stderr)
            print("Hint: Make sure API keys are set in environment variables:", file=sys.stderr)
            print("  - OpenAI: OPENAI_API_KEY", file=sys.stderr)
            print("  - Anthropic: ANTHROPIC_API_KEY", file=sys.stderr)
            sys.exit(1)
    
    # Read document
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            document = f.read()
        document_id = args.file
    else:
        # Read from stdin
        document = sys.stdin.read()
        document_id = "stdin"
    
    if not document.strip():
        print("Error: Empty document provided", file=sys.stderr)
        return 1
    
    # Evaluate
    try:
        result = evaluator.evaluate_document(document, document_id=document_id)
        
        # Output results
        if args.output_format == 'json':
            # Full result with all details
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        elif args.output_format == 'csv':
            # CSV format output
            include_reasoning = args.verbose
            print(result.to_csv(include_reasoning=include_reasoning), end='')
        else:  # pretty format
            print("Evaluation Results:")
            print("-" * 40)
            print(f"Model: {result.model_used}")
            print(f"Document: {result.document_id}")
            print("-" * 40)
            
            for score in result.scores:
                print(f"\n{score.criterion_name}: {score.score}/5")
                print(f"  Confidence: {score.confidence:.2f}")
                if args.verbose and score.reasoning:
                    print(f"  Reasoning: {score.reasoning}")
            
            print("\n" + "-" * 40)
            print(f"Overall Score: {result.overall_score:.2f}/5")
            
    except Exception as e:
        print(f"Error during evaluation: {e}", file=sys.stderr)
        return 1
    
    return 0


def export_criteria(args):
    """Export criteria to XML format."""
    # Load criteria
    criteria = Criteria.from_json_file(args.rubric)
    
    # Export to XML
    xml_output = criteria.to_xml()
    
    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(xml_output)
        print(f"Criteria exported to {args.output}")
    else:
        print(xml_output)
    
    return 0


def show_criteria(args):
    """Display criteria in human-readable format."""
    # Load criteria
    criteria = Criteria.from_json_file(args.rubric)
    
    # Display criteria
    for criterion in criteria.criteria_list:
        print(f"\n{criterion.name}")
        print("=" * len(criterion.name))
        print(f"Description: {criterion.description}")
        print("\nScoring Levels:")
        for level in criterion.levels:
            print(f"  {level.score}: {level.rule}")
    
    return 0


def evaluate_batch(args):
    """Evaluate multiple documents in batch."""
    # Load environment variables
    load_dotenv()
    
    # Load criteria
    criteria = Criteria.from_json_file(args.rubric)
    
    # Create evaluator
    if args.mock:
        # Mock mode - no provider needed
        evaluator = Evaluator(criteria)
    else:
        # Set up LLM provider
        model_name = args.model
        if not model_name:
            # Default models per provider
            default_models = {
                'pydantic_ai': os.getenv('DEFAULT_MODEL', 'gpt-4o-mini'),
                'openai': 'gpt-4o-mini',
                'anthropic': 'claude-3-5-haiku-latest'
            }
            model_name = default_models.get(args.provider, 'gpt-4o-mini')
        
        llm_config = LLMConfig(
            model_name=model_name,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
        
        try:
            llm_provider = create_llm_provider(args.provider, llm_config)
            evaluator = Evaluator(criteria, llm_provider=llm_provider)
        except Exception as e:
            print(f"Error: Failed to initialize LLM provider: {e}", file=sys.stderr)
            print("Hint: Make sure API keys are set in environment variables:", file=sys.stderr)
            print("  - OpenAI: OPENAI_API_KEY", file=sys.stderr)
            print("  - Anthropic: ANTHROPIC_API_KEY", file=sys.stderr)
            sys.exit(1)
    
    # Determine input source
    if args.directory:
        # Evaluate all files in directory
        try:
            results = evaluator.evaluate_directory(
                args.directory,
                pattern=args.pattern,
                recursive=args.recursive,
                show_progress=not args.no_progress,
                max_concurrent=args.max_concurrent,
                output_csv=args.output_csv,
                include_reasoning=args.verbose
            )
        except Exception as e:
            print(f"Error evaluating directory: {e}", file=sys.stderr)
            return 1
    else:
        # Evaluate list of files
        if not args.files:
            print("Error: No files or directory specified", file=sys.stderr)
            return 1
        
        # Read documents from files
        documents = {}
        for file_path in args.files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    documents[file_path] = f.read()
            except Exception as e:
                print(f"Warning: Failed to read {file_path}: {e}", file=sys.stderr)
        
        if not documents:
            print("Error: No documents could be read", file=sys.stderr)
            return 1
        
        try:
            results = evaluator.evaluate_batch(
                documents,
                show_progress=not args.no_progress,
                max_concurrent=args.max_concurrent,
                output_csv=args.output_csv,
                include_reasoning=args.verbose
            )
        except Exception as e:
            print(f"Error during batch evaluation: {e}", file=sys.stderr)
            return 1
    
    # Display summary unless CSV output was specified
    if not args.output_csv:
        print(f"\nBatch Evaluation Summary:")
        print("=" * 60)
        print(f"Total documents evaluated: {len(results)}")
        
        if results:
            avg_overall = sum(r.overall_score for r in results) / len(results)
            print(f"Average overall score: {avg_overall:.2f}/5")
            
            # Per-criterion averages
            criterion_scores = {}
            for result in results:
                for score in result.scores:
                    if score.criterion_name not in criterion_scores:
                        criterion_scores[score.criterion_name] = []
                    criterion_scores[score.criterion_name].append(score.score)
            
            print("\nAverage scores by criterion:")
            for criterion_name, scores in criterion_scores.items():
                avg_score = sum(scores) / len(scores)
                print(f"  {criterion_name}: {avg_score:.2f}/5")
            
            if args.verbose:
                print("\nDetailed results:")
                for result in results:
                    print(f"\n{result.document_id}:")
                    print(f"  Overall: {result.overall_score:.2f}/5")
                    for score in result.scores:
                        print(f"  {score.criterion_name}: {score.score}/5 (confidence: {score.confidence:.2f})")
    else:
        print(f"Results saved to: {args.output_csv}")
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="LLM as a Judge - Document evaluation framework",
        epilog="For more information, visit: https://github.com/takuyakubo/llm-as-a-judge"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    subparsers.required = True
    
    # Evaluate command
    eval_parser = subparsers.add_parser('evaluate', help='Evaluate a document')
    eval_parser.add_argument(
        'rubric',
        help='Path to rubric JSON file'
    )
    eval_parser.add_argument(
        '-f', '--file',
        help='Document file to evaluate (if not provided, reads from stdin)'
    )
    eval_parser.add_argument(
        '-o', '--output-format',
        choices=['pretty', 'json', 'csv'],
        default='pretty',
        help='Output format (default: pretty)'
    )
    eval_parser.add_argument(
        '-m', '--mock',
        action='store_true',
        help='Use mock evaluation (for testing)'
    )
    eval_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed reasoning for scores'
    )
    
    # LLM provider options
    eval_parser.add_argument(
        '--provider',
        choices=['pydantic_ai', 'openai', 'anthropic'],
        default='pydantic_ai',
        help='LLM access method: pydantic_ai (Pydantic AI framework), openai (direct API), anthropic (direct API) (default: pydantic_ai)'
    )
    eval_parser.add_argument(
        '--model',
        type=str,
        help='LLM model name (e.g., gpt-4o, claude-3-5-sonnet-latest, gemini-1.5-pro)'
    )
    eval_parser.add_argument(
        '--temperature',
        type=float,
        default=0.3,
        help='Generation temperature (default: 0.3)'
    )
    eval_parser.add_argument(
        '--max-tokens',
        type=int,
        help='Maximum tokens for generation'
    )
    
    eval_parser.set_defaults(func=evaluate_document)
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export criteria to XML')
    export_parser.add_argument(
        'rubric',
        help='Path to rubric JSON file'
    )
    export_parser.add_argument(
        '-o', '--output',
        help='Output file path (if not provided, prints to stdout)'
    )
    export_parser.set_defaults(func=export_criteria)
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Display criteria in readable format')
    show_parser.add_argument(
        'rubric',
        help='Path to rubric JSON file'
    )
    show_parser.set_defaults(func=show_criteria)
    
    # Batch evaluate command
    batch_parser = subparsers.add_parser('batch', help='Evaluate multiple documents in batch')
    batch_parser.add_argument(
        'rubric',
        help='Path to rubric JSON file'
    )
    
    # Input options (mutually exclusive)
    input_group = batch_parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-d', '--directory',
        help='Directory containing documents to evaluate'
    )
    input_group.add_argument(
        '-f', '--files',
        nargs='+',
        help='List of document files to evaluate'
    )
    
    # Directory options
    batch_parser.add_argument(
        '-p', '--pattern',
        default='*.txt',
        help='File pattern for directory search (default: *.txt)'
    )
    batch_parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Search directory recursively'
    )
    
    # Processing options
    batch_parser.add_argument(
        '--max-concurrent',
        type=int,
        default=5,
        help='Maximum concurrent evaluations (default: 5)'
    )
    batch_parser.add_argument(
        '--no-progress',
        action='store_true',
        help='Disable progress bar'
    )
    
    # Output options
    batch_parser.add_argument(
        '-o', '--output-csv',
        help='Save results to CSV file'
    )
    batch_parser.add_argument(
        '-m', '--mock',
        action='store_true',
        help='Use mock evaluation (for testing)'
    )
    batch_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed results and include reasoning in CSV'
    )
    
    # LLM provider options
    batch_parser.add_argument(
        '--provider',
        choices=['pydantic_ai', 'openai', 'anthropic'],
        default='pydantic_ai',
        help='LLM provider (default: pydantic_ai)'
    )
    batch_parser.add_argument(
        '--model',
        type=str,
        help='LLM model name'
    )
    batch_parser.add_argument(
        '--temperature',
        type=float,
        default=0.3,
        help='Generation temperature (default: 0.3)'
    )
    batch_parser.add_argument(
        '--max-tokens',
        type=int,
        help='Maximum tokens for generation'
    )
    
    batch_parser.set_defaults(func=evaluate_batch)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    try:
        sys.exit(args.func(args))
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()