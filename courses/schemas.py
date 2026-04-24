from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from users.schemas import UserSchema

class CategorySchema(BaseModel):
    id: int
    name: str

class LessonSchema(BaseModel):
    id: int
    title: str
    content: str
    order: int

class CourseSchema(BaseModel):
    id: int
    title: str
    description: str
    instructor: UserSchema
    category: Optional[CategorySchema] = None
    created_at: datetime

class CourseCreateSchema(BaseModel):
    title: str
    description: str
    category_id: Optional[int] = None

class CourseUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class EnrollmentSchema(BaseModel):
    id: int
    user: UserSchema
    course: CourseSchema
    enrolled_at: datetime

class ProgressSchema(BaseModel):
    id: int
    lesson: LessonSchema
    completed_at: datetime
