from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth
from .models import Course, Category, Enrollment, Lesson, Progress
from .schemas import (
    CourseSchema, CourseCreateSchema, CourseUpdateSchema, 
    EnrollmentSchema, ProgressSchema, LessonSchema
)
from .permissions import is_instructor, is_admin, is_student
from ninja.pagination import paginate

router = Router()

# PUBLIC ENDPOINTS
@router.get("/", response=List[CourseSchema], tags=["Courses"])
@paginate
def list_courses(request, category_id: int = None):
    qs = Course.objects.for_listing()
    if category_id:
        qs = qs.filter(category_id=category_id)
    return qs

@router.get("/{course_id}", response=CourseSchema, tags=["Courses"])
def get_course(request, course_id: int):
    return get_object_or_404(Course.objects.for_listing(), id=course_id)

# PROTECTED ENDPOINTS (Instructor)
@router.post("/", auth=JWTAuth(), response={201: CourseSchema}, tags=["Courses"])
@is_instructor
def create_course(request, data: CourseCreateSchema):
    course = Course.objects.create(
        instructor=request.auth,
        **data.dict(exclude_none=True)
    )
    return 201, course

@router.patch("/{course_id}", auth=JWTAuth(), response=CourseSchema, tags=["Courses"])
@is_instructor
def update_course(request, course_id: int, data: CourseUpdateSchema):
    course = get_object_or_404(Course, id=course_id)
    if course.instructor != request.auth and request.auth.role != 'admin':
        raise HttpError(403, "Forbidden: You are not the owner of this course")
    
    for attr, value in data.dict(exclude_none=True).items():
        setattr(course, attr, value)
    course.save()
    return course

@router.delete("/{course_id}", auth=JWTAuth(), response={204: None}, tags=["Courses"])
@is_admin
def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return 204, None

# ENROLLMENTS
@router.post("/enrollments", auth=JWTAuth(), response={201: EnrollmentSchema}, tags=["Enrollments"])
@is_student
def enroll_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.auth, course=course)
    return 201, enrollment

@router.get("/enrollments/my-courses", auth=JWTAuth(), response=List[EnrollmentSchema], tags=["Enrollments"])
@is_student
def my_courses(request):
    return Enrollment.objects.for_student_dashboard().filter(user=request.auth)

@router.post("/enrollments/{enrollment_id}/progress", auth=JWTAuth(), response={201: ProgressSchema}, tags=["Enrollments"])
@is_student
def mark_lesson_complete(request, enrollment_id: int, lesson_id: int):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.auth)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=enrollment.course)
    progress, created = Progress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
    return 201, progress
