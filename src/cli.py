#!/usr/bin/env python3
"""Command Line Interface for LLM as a Judge framework."""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .criteria import Criteria
from .evaluator import Evaluator


def evaluate_document(args):
    """Evaluate a document using the specified rubric."""
    # Load criteria
    criteria = Criteria.from_json_file(args.rubric)
    
    # Create evaluator (using mock evaluation for now)
    evaluator = Evaluator(criteria)
    
    # Read document
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            document = f.read()
    else:
        # Read from stdin
        document = sys.stdin.read()
    
    if not document.strip():
        print("Error: Empty document provided", file=sys.stderr)
        return 1
    
    # Evaluate
    try:
        result = evaluator.evaluate_document(document)
        
        # Output results
        if args.output_format == 'json':
            # Convert to simple score dict for compatibility
            score_dict = {score.criterion_name: score.score for score in result.scores}
            print(json.dumps(score_dict, indent=2))
        else:  # pretty format
            print("Evaluation Results:")
            print("-" * 40)
            for score in result.scores:
                print(f"{score.criterion_name}: {score.score}/5")
            print("-" * 40)
            total = sum(score.score for score in result.scores)
            avg = total / len(result.scores)
            print(f"Total Score: {total}/{len(result.scores) * 5}")
            print(f"Average: {avg:.2f}/5")
            
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
        choices=['pretty', 'json'],
        default='pretty',
        help='Output format (default: pretty)'
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