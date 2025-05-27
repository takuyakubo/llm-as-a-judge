"""Tests for CLI module."""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from src.cli import evaluate_document, export_criteria, show_criteria, main


class TestCLI(unittest.TestCase):
    """Test cases for CLI functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_rubric = {
            "criteria": [
                {
                    "name": "clarity",
                    "description": "How clear the text is",
                    "levels": [
                        {"score": 5, "rule": "Very clear"},
                        {"score": 4, "rule": "Clear"},
                        {"score": 3, "rule": "Somewhat clear"},
                        {"score": 2, "rule": "Unclear"},
                        {"score": 1, "rule": "Very unclear"}
                    ]
                },
                {
                    "name": "accuracy",
                    "description": "How accurate the content is",
                    "levels": [
                        {"score": 5, "rule": "Highly accurate"},
                        {"score": 4, "rule": "Accurate"},
                        {"score": 3, "rule": "Mostly accurate"},
                        {"score": 2, "rule": "Inaccurate"},
                        {"score": 1, "rule": "Very inaccurate"}
                    ]
                }
            ]
        }
        
        # Create temporary rubric file
        self.rubric_file = tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.json', 
            delete=False
        )
        json.dump(self.test_rubric, self.rubric_file)
        self.rubric_file.close()
        
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.rubric_file.name)
        
    def test_evaluate_document_from_file(self):
        """Test evaluating document from file."""
        # Create test document
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("This is a test document for evaluation.")
            doc_file = f.name
            
        try:
            # Create mock args
            args = MagicMock()
            args.rubric = self.rubric_file.name
            args.file = doc_file
            args.output_format = 'json'
            
            # Capture output
            with patch('sys.stdout', new=StringIO()) as fake_out:
                result = evaluate_document(args)
                output = fake_out.getvalue()
                
            # Check result
            self.assertEqual(result, 0)
            parsed_output = json.loads(output)
            self.assertIn('clarity', parsed_output)
            self.assertIn('accuracy', parsed_output)
            
        finally:
            os.unlink(doc_file)
            
    def test_evaluate_document_from_stdin(self):
        """Test evaluating document from stdin."""
        args = MagicMock()
        args.rubric = self.rubric_file.name
        args.file = None
        args.output_format = 'pretty'
        
        # Mock stdin
        test_input = "This is a test document from stdin."
        with patch('sys.stdin', StringIO(test_input)):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                result = evaluate_document(args)
                output = fake_out.getvalue()
                
        # Check result
        self.assertEqual(result, 0)
        self.assertIn("Evaluation Results:", output)
        self.assertIn("clarity:", output)
        self.assertIn("accuracy:", output)
        self.assertIn("Total Score:", output)
        self.assertIn("Average:", output)
        
    def test_evaluate_empty_document(self):
        """Test evaluating empty document."""
        args = MagicMock()
        args.rubric = self.rubric_file.name
        args.file = None
        args.output_format = 'json'
        
        # Mock empty stdin
        with patch('sys.stdin', StringIO("")):
            with patch('sys.stderr', new=StringIO()) as fake_err:
                result = evaluate_document(args)
                error_output = fake_err.getvalue()
                
        # Check error
        self.assertEqual(result, 1)
        self.assertIn("Error: Empty document provided", error_output)
        
    def test_export_criteria_to_stdout(self):
        """Test exporting criteria to stdout."""
        args = MagicMock()
        args.rubric = self.rubric_file.name
        args.output = None
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = export_criteria(args)
            output = fake_out.getvalue()
            
        # Check result
        self.assertEqual(result, 0)
        self.assertIn("<criteria>", output)
        self.assertIn("<criterion name=\"clarity\">", output)
        self.assertIn("<criterion name=\"accuracy\">", output)
        
    def test_export_criteria_to_file(self):
        """Test exporting criteria to file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            output_file = f.name
            
        try:
            args = MagicMock()
            args.rubric = self.rubric_file.name
            args.output = output_file
            
            with patch('sys.stdout', new=StringIO()) as fake_out:
                result = export_criteria(args)
                console_output = fake_out.getvalue()
                
            # Check result
            self.assertEqual(result, 0)
            self.assertIn(f"Criteria exported to {output_file}", console_output)
            
            # Check file content
            with open(output_file, 'r') as f:
                content = f.read()
            self.assertIn("<criteria>", content)
            
        finally:
            os.unlink(output_file)
            
    def test_show_criteria(self):
        """Test showing criteria in readable format."""
        args = MagicMock()
        args.rubric = self.rubric_file.name
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = show_criteria(args)
            output = fake_out.getvalue()
            
        # Check result
        self.assertEqual(result, 0)
        self.assertIn("clarity", output)
        self.assertIn("accuracy", output)
        self.assertIn("Description: How clear the text is", output)
        self.assertIn("Scoring Levels:", output)
        self.assertIn("5: Very clear", output)
        
    def test_main_evaluate_command(self):
        """Test main function with evaluate command."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test document")
            doc_file = f.name
            
        try:
            test_args = [
                'llm-judge',
                'evaluate',
                self.rubric_file.name,
                '-f', doc_file,
                '-o', 'json'
            ]
            
            with patch('sys.argv', test_args):
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    with patch('sys.exit') as mock_exit:
                        main()
                        
            # Check that exit was called with 0
            mock_exit.assert_called_once_with(0)
            
        finally:
            os.unlink(doc_file)
            
    def test_main_file_not_found(self):
        """Test main function with non-existent file."""
        test_args = [
            'llm-judge',
            'evaluate',
            'non_existent_rubric.json'
        ]
        
        with patch('sys.argv', test_args):
            with patch('sys.stderr', new=StringIO()) as fake_err:
                with patch('sys.exit') as mock_exit:
                    main()
                    
        # Check that exit was called with 1
        mock_exit.assert_called_once_with(1)
        
    def test_main_show_command(self):
        """Test main function with show command."""
        test_args = [
            'llm-judge',
            'show',
            self.rubric_file.name
        ]
        
        with patch('sys.argv', test_args):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                with patch('sys.exit') as mock_exit:
                    main()
                    output = fake_out.getvalue()
                    
        # Check output
        self.assertIn("clarity", output)
        self.assertIn("accuracy", output)
        mock_exit.assert_called_once_with(0)


if __name__ == '__main__':
    unittest.main()