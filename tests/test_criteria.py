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

    def test_to_json_empty_criteria(self):
        """空のCriteriaのJSON出力テスト"""
        criteria = Criteria()
        json_output = criteria.to_json()
        
        data = json.loads(json_output)
        self.assertEqual(data["criteria"], [])

    def test_to_json_single_criterion(self):
        """単一基準のJSON出力テスト"""
        criteria = Criteria()
        criteria.append(self.test_criterion)
        json_output = criteria.to_json()
        
        data = json.loads(json_output)
        self.assertEqual(len(data["criteria"]), 1)
        
        criterion_data = data["criteria"][0]
        self.assertEqual(criterion_data["name"], "test_criterion")
        self.assertEqual(criterion_data["description"], "テスト用の基準")
        self.assertEqual(len(criterion_data["levels"]), 1)
        
        level_data = criterion_data["levels"][0]
        self.assertEqual(level_data["score"], 5)
        self.assertEqual(level_data["rule"], "テストルール")

    def test_to_json_multiple_criteria(self):
        """複数基準のJSON出力テスト"""
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
        
        json_output = criteria.to_json()
        data = json.loads(json_output)
        
        self.assertEqual(len(data["criteria"]), 2)
        
        # 1つ目の基準を検証
        first_criterion = data["criteria"][0]
        self.assertEqual(first_criterion["name"], "test_criterion")
        self.assertEqual(len(first_criterion["levels"]), 1)
        
        # 2つ目の基準を検証
        second_criterion = data["criteria"][1]
        self.assertEqual(second_criterion["name"], "test_criterion2")
        self.assertEqual(second_criterion["description"], "2つ目の基準")
        self.assertEqual(len(second_criterion["levels"]), 2)
        self.assertEqual(second_criterion["levels"][0]["score"], 3)
        self.assertEqual(second_criterion["levels"][1]["score"], 1)

    def test_to_json_with_rubric_data(self):
        """rubric.jsonのデータを使用したJSON出力テスト"""
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
        
        json_output = criteria.to_json()
        data = json.loads(json_output)
        
        # JSONの基本構造を検証
        self.assertEqual(len(data["criteria"]), 5)  # 5つの基準
        
        # 最初の基準（claim_clarity）の詳細検証
        first_criterion = data["criteria"][0]
        self.assertEqual(first_criterion["name"], "claim_clarity")
        self.assertEqual(len(first_criterion["levels"]), 5)  # 5つのレベル
        
        # 最初のレベルの詳細検証
        first_level = first_criterion["levels"][0]
        self.assertEqual(first_level["score"], 5)
        self.assertEqual(first_level["rule"], "冒頭で問題提起と結論を1–2文で宣言, 結論が末尾で再確認できる")

    def test_from_json_empty_criteria(self):
        """空のJSONからのCriteria読み込みテスト"""
        json_str = '{"criteria": []}'
        criteria = Criteria.from_json(json_str)
        
        self.assertEqual(len(criteria.criteria), 0)

    def test_from_json_single_criterion(self):
        """単一基準のJSONからの読み込みテスト"""
        json_str = '''
        {
            "criteria": [
                {
                    "name": "test_criterion",
                    "description": "テスト用の基準",
                    "levels": [
                        {
                            "score": 5,
                            "rule": "テストルール"
                        }
                    ]
                }
            ]
        }
        '''
        
        criteria = Criteria.from_json(json_str)
        
        self.assertEqual(len(criteria.criteria), 1)
        
        criterion = criteria.criteria[0]
        self.assertEqual(criterion.name, "test_criterion")
        self.assertEqual(criterion.description, "テスト用の基準")
        self.assertEqual(len(criterion.levels), 1)
        
        level = criterion.levels[0]
        self.assertEqual(level.score, 5)
        self.assertEqual(level.rule, "テストルール")

    def test_from_json_multiple_criteria(self):
        """複数基準のJSONからの読み込みテスト"""
        json_str = '''
        {
            "criteria": [
                {
                    "name": "criterion1",
                    "description": "基準1",
                    "levels": [
                        {"score": 5, "rule": "ルール1"},
                        {"score": 3, "rule": "ルール2"}
                    ]
                },
                {
                    "name": "criterion2",
                    "description": "基準2",
                    "levels": [
                        {"score": 4, "rule": "ルール3"}
                    ]
                }
            ]
        }
        '''
        
        criteria = Criteria.from_json(json_str)
        
        self.assertEqual(len(criteria.criteria), 2)
        
        # 1つ目の基準を検証
        first_criterion = criteria.criteria[0]
        self.assertEqual(first_criterion.name, "criterion1")
        self.assertEqual(first_criterion.description, "基準1")
        self.assertEqual(len(first_criterion.levels), 2)
        self.assertEqual(first_criterion.levels[0].score, 5)
        self.assertEqual(first_criterion.levels[1].score, 3)
        
        # 2つ目の基準を検証
        second_criterion = criteria.criteria[1]
        self.assertEqual(second_criterion.name, "criterion2")
        self.assertEqual(second_criterion.description, "基準2")
        self.assertEqual(len(second_criterion.levels), 1)
        self.assertEqual(second_criterion.levels[0].score, 4)

    def test_json_roundtrip(self):
        """JSON出力→読み込みの往復テスト"""
        # 元データを作成
        original_criteria = Criteria()
        original_criteria.append(self.test_criterion)
        
        level2 = Level(score=3, rule="ルール2")
        criterion2 = Criterion(
            name="criterion2",
            description="2つ目の基準",
            levels=[level2]
        )
        original_criteria.append(criterion2)
        
        # JSON出力
        json_output = original_criteria.to_json()
        
        # JSON読み込み
        loaded_criteria = Criteria.from_json(json_output)
        
        # 往復後のデータが元データと一致することを検証
        self.assertEqual(len(loaded_criteria.criteria), len(original_criteria.criteria))
        
        for original, loaded in zip(original_criteria.criteria, loaded_criteria.criteria):
            self.assertEqual(original.name, loaded.name)
            self.assertEqual(original.description, loaded.description)
            self.assertEqual(len(original.levels), len(loaded.levels))
            
            for orig_level, loaded_level in zip(original.levels, loaded.levels):
                self.assertEqual(orig_level.score, loaded_level.score)
                self.assertEqual(orig_level.rule, loaded_level.rule)

if __name__ == "__main__":
    unittest.main() 