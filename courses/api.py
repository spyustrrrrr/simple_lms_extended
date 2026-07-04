from ninja import Router, Query, NinjaAPI
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from ninja.errors import HttpError
from typing import List

# Import dari modul dosen untuk JWT
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth

from .models import Course, Review, Wishlist, Category, Section, Lesson, Enrollment, Progress
from .schemas import ReviewSchemaIn, ReviewSchemaOut, MessageOut, CourseSchemaOut, CourseFilterSchema, StudentDashboardOut

User = get_user_model()

# Inisialisasi Router Utama untuk Courses
router = Router()

# Inisialisasi JWT Auth Handler sesuai modul dosen
apiAuth = HttpJwtAuth()

# ==========================================
# ENDPOINT FONDASI: REGISTRASI USER
# ==========================================
from ninja import Schema

class RegisterSchema(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    role: str = 'student' # Tambahan field role untuk akomodasi sistem kita

class UserOutSchema(Schema):
    id: int
    username: str
    email: str
    role: str

@router.post('/register/', response=UserOutSchema)
def register(request, data: RegisterSchema):
    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, "Username sudah digunakan")
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, "Email sudah digunakan")
        
    newUser = User.objects.create_user(
        username=data.username,
        password=data.password,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        role=data.role
    )
    return newUser


# ==========================================
# FITUR PAKET 1 DENGAN PROTEKSI JWT ASLI
# ==========================================

# 1. Endpoint Daftar Course (Search, Filter, Sorting)
@router.get("/", response=List[CourseSchemaOut])
def list_courses(request, filters: CourseFilterSchema = Query(...), sort_by: str = "-created_at"):
    courses = Course.objects.all()
    courses = filters.filter(courses)
    if sort_by in ['created_at', '-created_at', 'title', '-title']:
        courses = courses.order_by(sort_by)
    return courses

# 2. Endpoint Rating & Review (Protected)
@router.post("/{course_id}/reviews", auth=apiAuth)
def create_review(request, course_id: int, data: ReviewSchemaIn):
    student = request.user # Mengambil user asli dari token JWT
    if getattr(student, 'role', 'student') != 'student':
        raise HttpError(403, "Hanya student yang dapat memberikan review")

    course = get_object_or_404(Course, id=course_id)
    review, created = Review.objects.update_or_create(
        course=course,
        student=student,
        defaults={'rating': data.rating, 'comment': data.comment}
    )
    return {
        "id": review.id,
        "rating": review.rating,
        "comment": review.comment
    }

# 3. Endpoint Wishlist (Protected)
@router.post("/{course_id}/wishlist", auth=apiAuth)
def add_to_wishlist(request, course_id: int):
    student = request.user
    if getattr(student, 'role', 'student') != 'student':
        raise HttpError(403, "Hanya student yang memiliki wishlist")

    course = get_object_or_404(Course, id=course_id)
    Wishlist.objects.get_or_create(student=student, course=course)
    return {"message": "Course added to wishlist"}

# 4. Endpoint Cek Progress Belajar Student (Protected)
@router.get("/{course_id}/progress", auth=apiAuth)
def get_course_progress(request, course_id: int):
    student = request.user
    course = get_object_or_404(Course, id=course_id)
    
    total_lessons = Lesson.objects.filter(course=course).count()
    if total_lessons == 0:
        return {"course_id": course.id, "progress_percentage": 0.0, "completed_lessons": 0, "total_lessons": 0}
        
    completed_lessons = Progress.objects.filter(
        student=student, 
        lesson__course=course, 
        is_completed=True
    ).count()
    
    percentage = (completed_lessons / total_lessons) * 100
    return {
        "course_id": course.id,
        "progress_percentage": round(percentage, 2),
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons
    }

# 5. Endpoint Student Dashboard (Protected)
@router.get("/dashboard/student", response=StudentDashboardOut, auth=apiAuth)
def student_dashboard(request):
    # student = request.user
    student = User.objects.get(pk=request.user.id)
    if getattr(student, 'role', 'student') != 'student':
        raise HttpError(403, "Halaman ini hanya dapat diakses oleh student")
        
    enrollments = Enrollment.objects.filter(student=student)
    active_courses = []
    completed_count = 0
    
    for enrollment in enrollments:
        course = enrollment.course
        total_lessons = Lesson.objects.filter(course=course).count()
        completed_lessons = Progress.objects.filter(student=student, lesson__course=course, is_completed=True).count()
        
        percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0.0
        
        if percentage >= 100 and total_lessons > 0:
            completed_count += 1
        else:
            active_courses.append({
                "course_id": course.id,
                "title": course.title,
                "progress_percentage": round(percentage, 2)
            })

    enrolled_course_ids = enrollments.values_list('course_id', flat=True)
    recommended_courses = Course.objects.exclude(id__in=enrolled_course_ids)[:3]
    
    recommendations = []
    for c in recommended_courses:
        recommendations.append({
            "course_id": c.id,
            "title": c.title,
            "category": c.category.name if c.category else "Uncategorized"
        })

    return {
        "active_courses": active_courses,
        "completed_courses_count": completed_count,
        "recommendations": recommendations
    }