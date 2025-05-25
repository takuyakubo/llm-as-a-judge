import unittest
import json
from src.criteria import Level, Criterion, Criteria

class TestCriteria(unittest.TestCase):
    def setUp(self):
        # テスト用のデータを準備
        self.test_level = Level(score=5, rule="テストルール")
        self.test_criterion = Criterion(
            name="test_criterion",
            description="テスト用の基準",
            levels=[self.test_level]
        )
        
        # rubric.jsonからテストデータを読み込む
        with open("notebooks/rubric.json", "r") as f:
            self.rubric_data = json.load(f)

    def test_level_creation(self):
        """Levelクラスのインスタンス化テスト"""
        level = Level(score=5, rule="テストルール")
        self.assertEqual(level.score, 5)
        self.assertEqual(level.rule, "テストルール")

    def test_criterion_creation(self):
        """Criterionクラスのインスタンス化テスト"""
        criterion = Criterion(
            name="test_criterion",
            description="テスト用の基準",
            levels=[self.test_level]
        )
        self.assertEqual(criterion.name, "test_criterion")
        self.assertEqual(criterion.description, "テスト用の基準")
        self.assertEqual(len(criterion.levels), 1)
        self.assertEqual(criterion.levels[0].score, 5)

    def test_criteria_append(self):
        """Criteriaクラスのappendメソッドテスト"""
        criteria = Criteria()
        criteria.append(self.test_criterion)
        self.assertEqual(len(criteria.criteria), 1)
        self.assertEqual(criteria.criteria[0].name, "test_criterion")

    def test_rubric_data_parsing(self):
        """rubric.jsonのデータを使用した統合テスト"""
        criteria = Criteria()
        
        # rubric.jsonのデータを使用してCriterionを作成
        for criterion_data in self.rubric_data["criteria"]:
            levels = [Level(**level) for level in criterion_data["levels"]]
            criterion = Criterion(
                name=criterion_data["name"],
                description="",  # rubric.jsonにはdescriptionがないため空文字列
                levels=levels
            )
            criteria.append(criterion)

        # 検証
        self.assertEqual(len(criteria.criteria), 5)  # rubric.jsonには5つの基準がある
        
        # 最初の基準（claim_clarity）の検証
        first_criterion = criteria.criteria[0]
        self.assertEqual(first_criterion.name, "claim_clarity")
        self.assertEqual(len(first_criterion.levels), 5)
        self.assertEqual(first_criterion.levels[0].score, 5)
        self.assertEqual(first_criterion.levels[0].rule, "冒頭で問題提起と結論を1–2文で宣言, 結論が末尾で再確認できる")

if __name__ == "__main__":
    unittest.main() 