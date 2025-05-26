from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel
from .criteria import Criteria, Criterion


class CriterionScore(BaseModel):
    criterion_name: str
    score: int
    reasoning: str
    confidence: float


class EvaluationResult(BaseModel):
    document_id: Optional[str] = None
    timestamp: datetime
    scores: List[CriterionScore]
    overall_score: float
    model_used: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "document_id": self.document_id,
            "timestamp": self.timestamp.isoformat(),
            "scores": [
                {
                    "criterion_name": score.criterion_name,
                    "score": score.score,
                    "reasoning": score.reasoning,
                    "confidence": score.confidence
                }
                for score in self.scores
            ],
            "overall_score": self.overall_score,
            "model_used": self.model_used
        }


class Evaluator:
    def __init__(self, criteria: Criteria):
        self.criteria = criteria
    
    def generate_prompt(self, document: str, criterion: Criterion) -> str:
        """Generate evaluation prompt for a specific criterion"""
        prompt = f"""あなたは文書評価の専門家です。以下の基準に従って文書を評価してください。

評価基準: {criterion.name}
説明: {criterion.description}

スコアリングルール:
"""
        for level in sorted(criterion.levels, key=lambda x: x.score, reverse=True):
            prompt += f"- スコア {level.score}: {level.rule}\n"
        
        prompt += f"""
評価対象文書:
---
{document}
---

以下の形式で回答してください:
1. スコア: [1-5の整数]
2. 理由: [評価の根拠を具体的に説明]
3. 確信度: [0.0-1.0の小数。評価の確実性]

回答:"""
        return prompt
    
    def parse_llm_response(self, response: str, criterion_name: str) -> CriterionScore:
        """Parse LLM response to extract score, reasoning, and confidence"""
        # Simple parsing implementation - can be enhanced with better parsing logic
        lines = response.strip().split('\n')
        score = 3  # default
        reasoning = ""
        confidence = 0.5  # default
        
        for line in lines:
            if "スコア:" in line or "スコア：" in line:
                try:
                    # Handle both half-width and full-width colons
                    parts = line.replace('：', ':').split(':')
                    score = int(parts[-1].strip())
                except:
                    pass
            elif "理由:" in line or "理由：" in line:
                # Handle both half-width and full-width colons
                parts = line.replace('：', ':').split(':', 1)
                reasoning = parts[-1].strip() if len(parts) > 1 else ""
            elif "確信度:" in line or "確信度：" in line:
                try:
                    # Handle both half-width and full-width colons
                    parts = line.replace('：', ':').split(':')
                    confidence = float(parts[-1].strip())
                except:
                    pass
        
        return CriterionScore(
            criterion_name=criterion_name,
            score=score,
            reasoning=reasoning,
            confidence=confidence
        )
    
    def evaluate_document(self, document: str, llm_function=None) -> EvaluationResult:
        """Evaluate a document using all criteria"""
        if llm_function is None:
            # For testing purposes, return mock results
            return self._mock_evaluate(document)
        
        scores = []
        for criterion in self.criteria.criteria:
            prompt = self.generate_prompt(document, criterion)
            response = llm_function(prompt)
            score = self.parse_llm_response(response, criterion.name)
            scores.append(score)
        
        # Calculate overall score (weighted average based on confidence)
        total_weighted_score = sum(s.score * s.confidence for s in scores)
        total_confidence = sum(s.confidence for s in scores)
        overall_score = total_weighted_score / total_confidence if total_confidence > 0 else 0
        
        return EvaluationResult(
            timestamp=datetime.now(),
            scores=scores,
            overall_score=overall_score,
            model_used="custom_llm"
        )
    
    def _mock_evaluate(self, document: str) -> EvaluationResult:
        """Mock evaluation for testing"""
        scores = []
        for criterion in self.criteria.criteria:
            scores.append(CriterionScore(
                criterion_name=criterion.name,
                score=3,
                reasoning="Mock evaluation result",
                confidence=0.7
            ))
        
        return EvaluationResult(
            timestamp=datetime.now(),
            scores=scores,
            overall_score=3.0,
            model_used="mock"
        )