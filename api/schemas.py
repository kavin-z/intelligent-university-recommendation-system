from pydantic import BaseModel

class OLStudent(BaseModel):
  english: bool
  maths: bool
  science: bool
  passes: int

class ALStudent(BaseModel):
    stream: str           # Science / Commerce / Arts / Tech / Maths
    al_passes: int
    english: bool

class DiplomaStudent(BaseModel):
    diploma_field: str
    gpa: float | None
    institution_recognized: bool
    english: bool

class HNDStudent(BaseModel):
    hnd_field: str
    gpa: float | None
    english: bool

class BScStudent(BaseModel):
    degree_field: str
    gpa: float
    english: bool


class PostgradStudent(BaseModel):
    highest_degree: str
    postgrad_field: str
    research_experience: bool
    gpa: float
    english: bool
