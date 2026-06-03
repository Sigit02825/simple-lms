from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from .models import Course, CourseContent
from .schemas import CourseIn, CourseOut, DetailCourseOut, CourseContentIn, CourseContentOut
from ninja.pagination import paginate

router = Router()

@router.get("/", response=List[CourseOut], tags=["Courses"])
@paginate
def list_courses(request):
    return Course.objects.select_related('teacher').all()

@router.get("/{course_id}", response=DetailCourseOut, tags=["Courses"])
def get_course(request, course_id: int):
    return get_object_or_404(Course.objects.prefetch_related('coursecontent_set'), id=course_id)

@router.post("/", response={201: CourseOut}, tags=["Courses"])
def create_course(request, data: CourseIn):
    # For now, we'll assign the first user as teacher if not authenticated
    # In a real app, this would be request.auth
    from django.contrib.auth import get_user_model
    User = get_user_model()
    teacher = User.objects.first() 
    
    course = Course.objects.create(
        teacher=teacher,
        **data.dict()
    )
    return 201, course

@router.patch("/{course_id}", response=CourseOut, tags=["Courses"])
def update_course(request, course_id: int, data: CourseIn):
    course = get_object_or_404(Course, id=course_id)
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(course, attr, value)
    course.save()
    return course

@router.delete("/{course_id}", response={204: None}, tags=["Courses"])
def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return 204, None
