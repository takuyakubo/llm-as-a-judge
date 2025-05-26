import unittest
import json
import xml.etree.ElementTree as ET
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
        with open("tests/rubric.json", "r") as f:
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

    def test_to_xml_empty_criteria(self):
        """空のCriteriaのXML出力テスト"""
        criteria = Criteria()
        xml_output = criteria.to_xml()
        
        root = ET.fromstring(xml_output)
        self.assertEqual(root.tag, "criteria")
        self.assertEqual(len(root), 0)

    def test_to_xml_single_criterion(self):
        """単一基準のXML出力テスト"""
        criteria = Criteria()
        criteria.append(self.test_criterion)
        xml_output = criteria.to_xml()
        
        root = ET.fromstring(xml_output)
        self.assertEqual(root.tag, "criteria")
        self.assertEqual(len(root), 1)
        
        criterion_element = root[0]
        self.assertEqual(criterion_element.tag, "criterion")
        self.assertEqual(criterion_element.get("name"), "test_criterion")
        
        description_element = criterion_element.find("description")
        self.assertEqual(description_element.text, "テスト用の基準")
        
        levels_element = criterion_element.find("levels")
        self.assertEqual(len(levels_element), 1)
        
        level_element = levels_element[0]
        self.assertEqual(level_element.tag, "level")
        self.assertEqual(level_element.get("score"), "5")
        self.assertEqual(level_element.text, "テストルール")

    def test_to_xml_multiple_criteria(self):
        """複数基準のXML出力テスト"""
        criteria = Criteria()
        
        # 2つ目のテスト基準を作成
        level2 = Level(score=3, rule="ルール2")
        level3 = Level(score=1, rule="ルール3")
        criterion2 = Criterion(
            name="test_criterion2",
            description="2つ目の基準",
            levels=[level2, level3]
        )
        
        criteria.append(self.test_criterion)
        criteria.append(criterion2)
        
        xml_output = criteria.to_xml()
        root = ET.fromstring(xml_output)
        
        self.assertEqual(len(root), 2)
        
        # 1つ目の基準を検証
        first_criterion = root[0]
        self.assertEqual(first_criterion.get("name"), "test_criterion")
        self.assertEqual(len(first_criterion.find("levels")), 1)
        
        # 2つ目の基準を検証
        second_criterion = root[1]
        self.assertEqual(second_criterion.get("name"), "test_criterion2")
        self.assertEqual(second_criterion.find("description").text, "2つ目の基準")
        self.assertEqual(len(second_criterion.find("levels")), 2)

    def test_to_xml_with_rubric_data(self):
        """rubric.jsonのデータを使用したXML出力テスト"""
        criteria = Criteria()
        
        # rubric.jsonのデータを使用してCriterionを作成
        for criterion_data in self.rubric_data["criteria"]:
            levels = [Level(**level) for level in criterion_data["levels"]]
            criterion = Criterion(
                name=criterion_data["name"],
                description="",
                levels=levels
            )
            criteria.append(criterion)
        
        xml_output = criteria.to_xml()
        root = ET.fromstring(xml_output)
        
        # XMLの基本構造を検証
        self.assertEqual(root.tag, "criteria")
        self.assertEqual(len(root), 5)  # 5つの基準
        
        # 最初の基準（claim_clarity）の詳細検証
        first_criterion = root[0]
        self.assertEqual(first_criterion.get("name"), "claim_clarity")
        levels_element = first_criterion.find("levels")
        self.assertEqual(len(levels_element), 5)  # 5つのレベル
        
        # 最初のレベルの詳細検証
        first_level = levels_element[0]
        self.assertEqual(first_level.get("score"), "5")
        self.assertEqual(first_level.text, "冒頭で問題提起と結論を1–2文で宣言, 結論が末尾で再確認できる")

if __name__ == "__main__":
    unittest.main() 