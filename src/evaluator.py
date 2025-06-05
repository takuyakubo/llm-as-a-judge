from typing import Dict, List, Optional, Callable, Union
from datetime import datetime
import asyncio
import csv
import io
from pydantic import BaseModel
from .criteria import Criteria, Criterion
from .llm_providers import LLMProvider, create_llm_provider, LLMConfig


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
    
    def to_csv(self, include_reasoning: bool = True) -> str:
        """Convert evaluation result to CSV format.
        
        Args:
            include_reasoning: Whether to include reasoning column
            
        Returns:
            CSV string with evaluation results
        """
        output = io.StringIO()
        
        # Define headers
        headers = ['document_id', 'timestamp', 'model_used', 'criterion_name', 
                   'score', 'confidence']
        if include_reasoning:
            headers.append('reasoning')
        headers.append('overall_score')
        
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        
        # Write row for each criterion score
        for score in self.scores:
            row = {
                'document_id': self.document_id or '',
                'timestamp': self.timestamp.isoformat(),
                'model_used': self.model_used or '',
                'criterion_name': score.criterion_name,
                'score': score.score,
                'confidence': score.confidence,
                'overall_score': f"{self.overall_score:.2f}"
            }
            if include_reasoning:
                row['reasoning'] = score.reasoning
            writer.writerow(row)
        
        return output.getvalue()


class Evaluator:
    def __init__(
        self, 
        criteria: Criteria, 
        llm_function: Optional[Callable[[str], str]] = None,
        llm_provider: Optional[LLMProvider] = None,
        llm_config: Optional[Union[LLMConfig, Dict]] = None
    ):
        self.criteria = criteria
        self.llm_function = llm_function
        self.llm_provider = llm_provider
        
        # Only create default provider if explicitly requested
        # (keep None for mock mode compatibility)
    
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
    
    def evaluate_document(self, document: str, return_dict: bool = False, document_id: Optional[str] = None) -> Union[Dict[str, int], EvaluationResult]:
        """Evaluate a document using all criteria
        
        Args:
            document: The document to evaluate
            return_dict: If True, return simple dict with criterion_name: score mapping
                       If False, return full EvaluationResult object
            document_id: Optional identifier for the document
        
        Returns:
            Dictionary mapping criterion names to scores, or EvaluationResult object
        """
        # Try to use async method if available
        if self.llm_provider and asyncio.iscoroutinefunction(self.llm_provider.generate):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If we're already in an async context, use sync version
                    return self._evaluate_sync(document, return_dict, document_id)
                else:
                    # Otherwise, run the async version
                    return loop.run_until_complete(self.evaluate_document_async(document, return_dict, document_id))
            except RuntimeError:
                # Fallback to sync version if async fails
                return self._evaluate_sync(document, return_dict, document_id)
        else:
            return self._evaluate_sync(document, return_dict, document_id)
    
    def _evaluate_sync(self, document: str, return_dict: bool = False, document_id: Optional[str] = None) -> Union[Dict[str, int], EvaluationResult]:
        """Synchronous evaluation"""
        llm_function = self.llm_function
        
        if llm_function is None and self.llm_provider is None:
            # For testing purposes, return mock results
            result = self._mock_evaluate(document, document_id)
        else:
            scores = []
            model_used = None
            
            for criterion in self.criteria.criteria:
                prompt = self.generate_prompt(document, criterion)
                
                if llm_function:
                    response = llm_function(prompt)
                    model_used = "custom_llm"
                elif self.llm_provider:
                    response = self.llm_provider.generate_sync(prompt)
                    model_used = getattr(self.llm_provider.config, 'model_name', 'unknown')
                else:
                    raise ValueError("No LLM function or provider available")
                
                score = self.parse_llm_response(response, criterion.name)
                scores.append(score)
            
            # Calculate overall score (weighted average based on confidence)
            total_weighted_score = sum(s.score * s.confidence for s in scores)
            total_confidence = sum(s.confidence for s in scores)
            overall_score = total_weighted_score / total_confidence if total_confidence > 0 else 0
            
            result = EvaluationResult(
                document_id=document_id,
                timestamp=datetime.now(),
                scores=scores,
                overall_score=overall_score,
                model_used=model_used
            )
        
        if return_dict:
            # Return simple dict for backward compatibility
            return {score.criterion_name: score.score for score in result.scores}
        return result
    
    async def evaluate_document_async(self, document: str, return_dict: bool = False, document_id: Optional[str] = None) -> Union[Dict[str, int], EvaluationResult]:
        """Asynchronous evaluation for better performance"""
        if not self.llm_provider:
            # Fallback to sync if no provider
            return self._evaluate_sync(document, return_dict, document_id)
        
        scores = []
        model_used = getattr(self.llm_provider.config, 'model_name', 'unknown')
        
        # Create all prompts
        prompts = [(criterion, self.generate_prompt(document, criterion)) 
                   for criterion in self.criteria.criteria]
        
        # Evaluate all criteria concurrently
        tasks = [self.llm_provider.generate(prompt) for _, prompt in prompts]
        responses = await asyncio.gather(*tasks)
        
        # Parse all responses
        for (criterion, _), response in zip(prompts, responses):
            score = self.parse_llm_response(response, criterion.name)
            scores.append(score)
        
        # Calculate overall score
        total_weighted_score = sum(s.score * s.confidence for s in scores)
        total_confidence = sum(s.confidence for s in scores)
        overall_score = total_weighted_score / total_confidence if total_confidence > 0 else 0
        
        result = EvaluationResult(
            document_id=document_id,
            timestamp=datetime.now(),
            scores=scores,
            overall_score=overall_score,
            model_used=model_used
        )
        
        if return_dict:
            return {score.criterion_name: score.score for score in result.scores}
        return result
    
    def _mock_evaluate(self, document: str, document_id: Optional[str] = None) -> EvaluationResult:
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
            document_id=document_id,
            timestamp=datetime.now(),
            scores=scores,
            overall_score=3.0,
            model_used="mock"
        )