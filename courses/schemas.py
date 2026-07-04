from ninja import Schema, FilterSchema
from typing import Optional, List
from pydantic import Field

# Schema untuk menerima data dari user (Input)
class ReviewSchemaIn(Schema):
    rating: int
    comment: Optional[str] = None

# Schema untuk mengembalikan data ke user (Output)
class ReviewSchemaOut(Schema):
    id: int
    course_id: int
    student_id: int
    rating: int
    comment: Optional[str]

class MessageOut(Schema):
    message: str

class CategoryOut(Schema):
    id: int
    name: str

class InstructorOut(Schema):
    id: int
    username: str

class CourseSchemaOut(Schema):
    id: int
    title: str
    description: str
    category: Optional[CategoryOut] = None
    instructor: InstructorOut

# Schema khusus untuk menangani Filter dan Search
class CourseFilterSchema(FilterSchema):
    # 'q' akan mencari teks di field title ATAU description
    search: Optional[str] = Field(None, q=['title__icontains', 'description__icontains'])
    category_id: Optional[int] = None
    instructor_id: Optional[int] = None


# --- KODE YANG SUDAH ADA SEBELUMNYA BIARKAN SAJA ---

class ActiveCourseOut(Schema):
    course_id: int
    title: str
    progress_percentage: float

class RecommendationOut(Schema):
    course_id: int
    title: str
    category: str

class StudentDashboardOut(Schema):
    active_courses: List[ActiveCourseOut]
    completed_courses_count: int
    recommendations: List[RecommendationOut]