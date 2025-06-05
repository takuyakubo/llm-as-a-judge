#!/usr/bin/env python3
"""Example of exporting evaluation results to CSV format."""

import sys
sys.path.insert(0, '..')

from src.criteria import Criteria
from src.evaluator import Evaluator, EvaluationResult, CriterionScore
from datetime import datetime

# Sample document to evaluate
SAMPLE_DOCUMENT = """
人工知能（AI）の急速な発展により、私たちの生活は大きく変化しています。
特に、大規模言語モデル（LLM）の登場は、自然言語処理の分野に革命をもたらしました。

しかし、AIの発展には倫理的な課題も伴います。
プライバシーの保護、バイアスの問題、説明可能性の欠如など、
解決すべき課題は山積みです。

これらの課題に対処するため、研究者や政策立案者は協力して
AIガバナンスの枠組みを構築する必要があります。
"""

def main():
    # Load criteria from rubric
    criteria = Criteria.from_json_file('../tests/rubric.json')
    
    # Create evaluator (using mock mode for demo)
    evaluator = Evaluator(criteria)
    
    # Evaluate the document
    result = evaluator.evaluate_document(
        SAMPLE_DOCUMENT, 
        document_id="ai_ethics_doc.txt"
    )
    
    print("=== Evaluation Results ===")
    print(f"Document: {result.document_id}")
    print(f"Model: {result.model_used}")
    print(f"Overall Score: {result.overall_score:.2f}/5")
    print()
    
    # Export to CSV with reasoning
    print("=== CSV Export (with reasoning) ===")
    csv_with_reasoning = result.to_csv(include_reasoning=True)
    print(csv_with_reasoning)
    
    # Export to CSV without reasoning (more compact)
    print("=== CSV Export (without reasoning) ===")
    csv_without_reasoning = result.to_csv(include_reasoning=False)
    print(csv_without_reasoning)
    
    # Save to file
    with open('evaluation_results.csv', 'w', encoding='utf-8') as f:
        f.write(csv_with_reasoning)
    print("Results saved to evaluation_results.csv")
    
    # Example: Using the CLI for CSV export
    print("\n=== CLI Usage Example ===")
    print("To export evaluation results as CSV using the CLI:")
    print("$ python -m src.cli evaluate tests/rubric.json -f document.txt -o csv")
    print("\nWith detailed reasoning:")
    print("$ python -m src.cli evaluate tests/rubric.json -f document.txt -o csv -v")
    
    # Example: Processing multiple documents and combining results
    print("\n=== Batch Processing Example ===")
    documents = [
        ("doc1.txt", "第一の文書の内容..."),
        ("doc2.txt", "第二の文書の内容..."),
        ("doc3.txt", "第三の文書の内容...")
    ]
    
    all_results = []
    for doc_id, content in documents:
        result = evaluator.evaluate_document(content, document_id=doc_id)
        all_results.append(result)
    
    # Combine all CSV results
    with open('batch_results.csv', 'w', encoding='utf-8') as f:
        for i, result in enumerate(all_results):
            if i == 0:
                # Include header for first result
                f.write(result.to_csv(include_reasoning=False))
            else:
                # Skip header for subsequent results
                csv_lines = result.to_csv(include_reasoning=False).splitlines()
                f.write('\n'.join(csv_lines[1:]) + '\n')
    
    print("Batch results saved to batch_results.csv")

if __name__ == '__main__':
    main()