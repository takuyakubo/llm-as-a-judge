from pydantic import BaseModel
import xml.etree.ElementTree as ET
import json

class Level(BaseModel):
    score: int
    rule: str

class Criterion(BaseModel):
    name: str
    description: str
    levels: list[Level]

class Criteria:
    def __init__(self, criteria_list: list[Criterion] | None = None) -> None:
        self.criteria = criteria_list or []
        self.criteria_list = self.criteria  # Alias for compatibility

    def append(self, criterion: Criterion) -> None:
        self.criteria.append(criterion)

    def to_xml(self) -> str:
        root = ET.Element("criteria")
        
        for criterion in self.criteria:
            criterion_element = ET.SubElement(root, "criterion")
            criterion_element.set("name", criterion.name)
            
            description_element = ET.SubElement(criterion_element, "description")
            description_element.text = criterion.description
            
            levels_element = ET.SubElement(criterion_element, "levels")
            
            for level in criterion.levels:
                level_element = ET.SubElement(levels_element, "level")
                level_element.set("score", str(level.score))
                level_element.text = level.rule
        
        return ET.tostring(root, encoding='unicode')

    def to_json(self) -> str:
        data = {
            "criteria": [
                {
                    "name": criterion.name,
                    "description": criterion.description,
                    "levels": [
                        {
                            "score": level.score,
                            "rule": level.rule
                        }
                        for level in criterion.levels
                    ]
                }
                for criterion in self.criteria
            ]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'Criteria':
        data = json.loads(json_str)
        criteria = cls()
        
        for criterion_data in data.get("criteria", []):
            levels = [
                Level(score=level_data["score"], rule=level_data["rule"])
                for level_data in criterion_data.get("levels", [])
            ]
            criterion = Criterion(
                name=criterion_data["name"],
                description=criterion_data.get("description", ""),  # Default to empty string
                levels=levels
            )
            criteria.append(criterion)
        
        return criteria

    @classmethod
    def from_json_file(cls, filepath: str) -> 'Criteria':
        """Load criteria from a JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "criteria": [
                {
                    "name": criterion.name,
                    "description": criterion.description,
                    "levels": [
                        {
                            "score": level.score,
                            "rule": level.rule
                        }
                        for level in criterion.levels
                    ]
                }
                for criterion in self.criteria
            ]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Criteria':
        """Create from dictionary representation."""
        criteria = cls()
        
        for criterion_data in data.get("criteria", []):
            levels = [
                Level(score=level_data["score"], rule=level_data["rule"])
                for level_data in criterion_data.get("levels", [])
            ]
            criterion = Criterion(
                name=criterion_data["name"],
                description=criterion_data.get("description", ""),
                levels=levels
            )
            criteria.append(criterion)
        
        return criteria

