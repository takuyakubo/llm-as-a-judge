import unittest
from datetime import datetime
import json
from src.criteria import Criteria, Criterion, Level
from src.evaluator import Evaluator, EvaluationResult, CriterionScore


class TestEvaluator(unittest.TestCase):
    def setUp(self):
        """Set up test criteria"""
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
        self.evaluator = Evaluator(self.criteria)
    
    def test_generate_prompt(self):
        """Test prompt generation"""
        document = "これはテスト文書です。"
        criterion = self.criteria.criteria[0]
        prompt = self.evaluator.generate_prompt(document, criterion)
        
        # Check if prompt contains necessary elements
        self.assertIn("clarity", prompt)
        self.assertIn("文章の明確さ", prompt)
        self.assertIn("これはテスト文書です。", prompt)
        self.assertIn("スコア 5: 非常に明確", prompt)
    
    def test_parse_llm_response(self):
        """Test LLM response parsing"""
        response = """1. スコア: 4
2. 理由: 文章は明確で理解しやすい
3. 確信度: 0.85"""
        
        score = self.evaluator.parse_llm_response(response, "clarity")
        
        self.assertEqual(score.criterion_name, "clarity")
        self.assertEqual(score.score, 4)
        self.assertEqual(score.reasoning, "文章は明確で理解しやすい")
        self.assertEqual(score.confidence, 0.85)
    
    def test_parse_llm_response_with_variations(self):
        """Test parsing with different response formats"""
        # Test with full-width colon
        response = """スコア：3
理由：まあまあの出来
確信度：0.6"""
        
        score = self.evaluator.parse_llm_response(response, "test")
        self.assertEqual(score.score, 3)
        self.assertEqual(score.confidence, 0.6)
    
    def test_mock_evaluate(self):
        """Test mock evaluation"""
        document = "これはテスト文書です。"
        result = self.evaluator.evaluate_document(document)
        
        self.assertIsInstance(result, EvaluationResult)
        self.assertEqual(len(result.scores), 2)  # We have 2 criteria
        self.assertEqual(result.model_used, "mock")
        self.assertIsInstance(result.timestamp, datetime)
        
        # Check individual scores
        for score in result.scores:
            self.assertIn(score.criterion_name, ["clarity", "coherence"])
            self.assertEqual(score.score, 3)
            self.assertEqual(score.confidence, 0.7)
    
    def test_evaluate_with_custom_llm(self):
        """Test evaluation with custom LLM function"""
        def mock_llm(prompt):
            if "clarity" in prompt:
                return "スコア: 5\n理由: 非常に明確な文章\n確信度: 0.95"
            else:
                return "スコア: 4\n理由: 論理的に一貫している\n確信度: 0.8"
        
        document = "これは優れた文書です。"
        result = self.evaluator.evaluate_document(document, llm_function=mock_llm)
        
        self.assertEqual(len(result.scores), 2)
        self.assertEqual(result.model_used, "custom_llm")
        
        # Check scores
        clarity_score = next(s for s in result.scores if s.criterion_name == "clarity")
        self.assertEqual(clarity_score.score, 5)
        self.assertEqual(clarity_score.confidence, 0.95)
        
        coherence_score = next(s for s in result.scores if s.criterion_name == "coherence")
        self.assertEqual(coherence_score.score, 4)
        self.assertEqual(coherence_score.confidence, 0.8)
        
        # Check overall score calculation
        expected_overall = (5 * 0.95 + 4 * 0.8) / (0.95 + 0.8)
        self.assertAlmostEqual(result.overall_score, expected_overall, places=2)
    
    def test_evaluation_result_to_dict(self):
        """Test EvaluationResult serialization"""
        result = EvaluationResult(
            document_id="doc123",
            timestamp=datetime.now(),
            scores=[
                CriterionScore(
                    criterion_name="clarity",
                    score=4,
                    reasoning="Clear writing",
                    confidence=0.9
                )
            ],
            overall_score=4.0,
            model_used="gpt-4"
        )
        
        result_dict = result.to_dict()
        self.assertEqual(result_dict["document_id"], "doc123")
        self.assertEqual(result_dict["overall_score"], 4.0)
        self.assertEqual(result_dict["model_used"], "gpt-4")
        self.assertEqual(len(result_dict["scores"]), 1)
        self.assertEqual(result_dict["scores"][0]["criterion_name"], "clarity")


class TestIntegrationWithRubric(unittest.TestCase):
    def setUp(self):
        """Load the actual rubric from JSON"""
        with open('tests/rubric.json', 'r', encoding='utf-8') as f:
            rubric_data = f.read()
        self.criteria = Criteria.from_json(rubric_data)
        self.evaluator = Evaluator(self.criteria)
    
    def test_evaluate_with_rubric(self):
        """Test evaluation using the actual rubric"""
        document = """
        本記事では、AIの社会実装における課題について論じる。
        
        第一に、技術的な課題がある。現在のAIシステムは...
        第二に、倫理的な課題も重要である。プライバシーの問題...
        
        結論として、これらの課題を解決するには...
        """
        
        result = self.evaluator.evaluate_document(document)
        
        # Check that we have scores for all 5 criteria in the rubric
        self.assertEqual(len(result.scores), 5)
        
        # Check criterion names match rubric
        criterion_names = {score.criterion_name for score in result.scores}
        expected_names = {"claim_clarity", "coherence", "evidence_quality", 
                         "depth_of_reasoning", "readability"}
        self.assertEqual(criterion_names, expected_names)


if __name__ == '__main__':
    unittest.main()