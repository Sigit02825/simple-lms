from ninja import Schema, Field
from datetime import datetime
from typing import Optional, List
from users.schemas import UserSchema

class UserOut(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str

class CourseIn(Schema):
    name: str
    description: str = '-'
    price: int = 10000

class CourseOut(Schema):
    id: int
    name: str
    description: str
    price: int
    image: Optional[str] = None
    teacher: UserOut
    created_at: datetime
    updated_at: datetime

class ContentTitleOut(Schema):
    id: int
    name: str

class DetailCourseOut(CourseOut):
    contents: List[ContentTitleOut] = Field(
        ..., alias="coursecontent_set"
    )

class CourseContentIn(Schema):
    name: str
    description: str = '-'
    video_url: Optional[str] = None
    course_id: int
    parent_id: Optional[int] = None

class CourseContentOut(Schema):
    id: int
    name: str
    description: str
    video_url: Optional[str] = None
    course_id: int
    parent_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
