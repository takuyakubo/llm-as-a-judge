from pydantic import BaseModel

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

