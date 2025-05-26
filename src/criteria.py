from pydantic import BaseModel
import xml.etree.ElementTree as ET

class Level(BaseModel):
    score: int
    rule: str

class Criterion(BaseModel):
    name: str
    description: str
    levels: list[Level]

class Criteria:
    def __init__(self) -> None:
        self.criteria = []

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

