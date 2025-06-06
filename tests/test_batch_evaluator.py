import unittest
import tempfile
import os
import csv
import json
from datetime import datetime
from pathlib import Path
from src.criteria import Criteria, Criterion, Level
from src.evaluator import Evaluator, EvaluationResult, CriterionScore


class TestBatchEvaluator(unittest.TestCase):
    def setUp(self):
        """Set up test criteria and evaluator"""
        self.criteria = Criteria()
        self.criteria.append(Criterion(
            name="clarity",
            description="文章の明確さ",
            levels=[
                Level(score=5, rule="非常に明確"),
                Level(score=4, rule="明確"),
                Level(score=3, rule="普通"),
                Level(score=2, rule="やや不明確"),
                Level(score=1, rule="不明確")
            ]
        ))
        self.criteria.append(Criterion(
            name="coherence",
            description="論理的一貫性",
            levels=[
                Level(score=5, rule="完全に一貫"),
                Level(score=4, rule="ほぼ一貫"),
                Level(score=3, rule="部分的に一貫"),
                Level(score=2, rule="一貫性に欠ける"),
                Level(score=1, rule="全く一貫性なし")
            ]
        ))
        # Use mock evaluator for tests
        self.evaluator = Evaluator(self.criteria)
    
    def test_evaluate_batch_with_list(self):
        """Test batch evaluation with list of documents"""
        documents = [
            "これは最初のテスト文書です。",
            "これは二番目のテスト文書です。",
            "これは三番目のテスト文書です。"
        ]
        
        results = self.evaluator.evaluate_batch(documents, show_progress=False)
        
        self.assertEqual(len(results), 3)
        for i, result in enumerate(results):
            self.assertEqual(result.document_id, f"doc_{i}")
            self.assertIsInstance(result, EvaluationResult)
            self.assertEqual(len(result.scores), 2)  # 2 criteria
    
    def test_evaluate_batch_with_dict(self):
        """Test batch evaluation with dictionary of documents"""
        documents = {
            "report_1.txt": "業績報告書の内容です。",
            "report_2.txt": "技術仕様書の内容です。",
            "report_3.txt": "提案書の内容です。"
        }
        
        results = self.evaluator.evaluate_batch(documents, show_progress=False)
        
        self.assertEqual(len(results), 3)
        doc_ids = {r.document_id for r in results}
        self.assertEqual(doc_ids, {"report_1.txt", "report_2.txt", "report_3.txt"})
    
    def test_evaluate_batch_with_tuples(self):
        """Test batch evaluation with list of (id, content) tuples"""
        documents = [
            ("doc_A", "文書Aの内容"),
            ("doc_B", "文書Bの内容"),
            ("doc_C", "文書Cの内容")
        ]
        
        results = self.evaluator.evaluate_batch(documents, show_progress=False)
        
        self.assertEqual(len(results), 3)
        doc_ids = [r.document_id for r in results]
        self.assertEqual(doc_ids, ["doc_A", "doc_B", "doc_C"])
    
    def test_evaluate_batch_csv_output(self):
        """Test batch evaluation with CSV output"""
        documents = {
            "test1.txt": "テスト文書1",
            "test2.txt": "テスト文書2"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_path = f.name
        
        try:
            results = self.evaluator.evaluate_batch(
                documents, 
                show_progress=False,
                output_csv=csv_path,
                include_reasoning=True
            )
            
            # Check CSV file was created
            self.assertTrue(os.path.exists(csv_path))
            
            # Read and verify CSV content
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                # Should have 4 rows (2 documents × 2 criteria)
                self.assertEqual(len(rows), 4)
                
                # Check headers
                expected_headers = {'document_id', 'timestamp', 'model_used', 
                                  'criterion_name', 'score', 'confidence', 
                                  'reasoning', 'overall_score'}
                self.assertEqual(set(reader.fieldnames), expected_headers)
                
                # Verify document IDs
                doc_ids = {row['document_id'] for row in rows}
                self.assertEqual(doc_ids, {"test1.txt", "test2.txt"})
                
        finally:
            if os.path.exists(csv_path):
                os.unlink(csv_path)
    
    def test_evaluate_directory(self):
        """Test evaluating all documents in a directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            test_files = {
                "doc1.txt": "第一の文書の内容です。",
                "doc2.txt": "第二の文書の内容です。",
                "doc3.txt": "第三の文書の内容です。",
                "ignore.pdf": "This should be ignored"
            }
            
            for filename, content in test_files.items():
                with open(os.path.join(tmpdir, filename), 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Evaluate directory
            results = self.evaluator.evaluate_directory(
                tmpdir,
                pattern="*.txt",
                show_progress=False
            )
            
            # Should only process .txt files
            self.assertEqual(len(results), 3)
            
            # Check document IDs contain file paths
            doc_ids = {r.document_id for r in results}
            for doc_id in doc_ids:
                self.assertTrue(doc_id.endswith('.txt'))
                self.assertIn('doc', doc_id)
    
    def test_evaluate_directory_recursive(self):
        """Test recursive directory evaluation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create subdirectory
            subdir = os.path.join(tmpdir, "subdir")
            os.makedirs(subdir)
            
            # Create files in main and subdirectory
            files = {
                os.path.join(tmpdir, "main.txt"): "メインディレクトリの文書",
                os.path.join(subdir, "sub.txt"): "サブディレクトリの文書"
            }
            
            for filepath, content in files.items():
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Non-recursive should only find main.txt
            results = self.evaluator.evaluate_directory(
                tmpdir,
                pattern="*.txt",
                recursive=False,
                show_progress=False
            )
            self.assertEqual(len(results), 1)
            
            # Recursive should find both files
            results = self.evaluator.evaluate_directory(
                tmpdir,
                pattern="*.txt",
                recursive=True,
                show_progress=False
            )
            self.assertEqual(len(results), 2)
    
    def test_evaluate_batch_with_custom_llm(self):
        """Test batch evaluation with custom LLM function"""
        def mock_llm(prompt):
            # Return different scores based on document content
            if "優秀" in prompt:
                return "スコア: 5\n理由: 優秀な文書\n確信度: 0.95"
            elif "良好" in prompt:
                return "スコア: 4\n理由: 良好な文書\n確信度: 0.85"
            else:
                return "スコア: 3\n理由: 標準的な文書\n確信度: 0.75"
        
        evaluator_with_llm = Evaluator(self.criteria, llm_function=mock_llm)
        
        documents = {
            "excellent.txt": "これは優秀な文書です。",
            "good.txt": "これは良好な文書です。",
            "standard.txt": "これは標準的な文書です。"
        }
        
        results = evaluator_with_llm.evaluate_batch(documents, show_progress=False)
        
        # Check that different documents got different scores
        result_map = {r.document_id: r for r in results}
        
        excellent_result = result_map["excellent.txt"]
        good_result = result_map["good.txt"]
        standard_result = result_map["standard.txt"]
        
        # Verify scores match our mock LLM logic
        self.assertGreater(excellent_result.overall_score, good_result.overall_score)
        self.assertGreater(good_result.overall_score, standard_result.overall_score)
    
    def test_evaluate_batch_error_handling(self):
        """Test error handling for invalid inputs"""
        # Empty list
        with self.assertRaises(ValueError):
            self.evaluator.evaluate_batch([])
        
        # Invalid directory
        with self.assertRaises(ValueError):
            self.evaluator.evaluate_directory("/nonexistent/directory")
        
        # Directory with no matching files
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create only non-matching files
            with open(os.path.join(tmpdir, "test.pdf"), 'w') as f:
                f.write("PDF content")
            
            with self.assertRaises(ValueError):
                self.evaluator.evaluate_directory(tmpdir, pattern="*.txt")
    
    def test_max_concurrent_setting(self):
        """Test that max_concurrent parameter is respected"""
        # This is mainly to ensure the parameter is passed correctly
        # Actual concurrency testing would require mocking async operations
        documents = ["doc1", "doc2", "doc3", "doc4", "doc5"]
        
        results = self.evaluator.evaluate_batch(
            documents,
            show_progress=False,
            max_concurrent=2
        )
        
        self.assertEqual(len(results), 5)


if __name__ == '__main__':
    unittest.main()