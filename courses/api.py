from typing import List

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from .models import Course, CourseMember
from .permissions import is_admin, is_instructor, is_student
from .schemas import (
    AnalyticsOut,
    CourseIn,
    CourseMemberOut,
    CourseOut,
    CoursePatchIn,
    DetailCourseOut,
    TaskStatusOut,
)
from .services import (
    aggregate_course_activity,
    course_detail_cache_key,
    course_list_cache_key,
    invalidate_course_cache,
    log_activity,
    log_learning_analytics,
    rate_limit,
    serialize_course,
    serialize_course_detail,
)
from .tasks import (
    export_course_report,
    generate_certificate,
    send_enrollment_email,
    update_course_statistics,
)
from django.core.cache import cache


router = Router()


@router.get("/", response=List[CourseOut], tags=["Courses"])
@rate_limit('course-list')
def list_courses(request):
    cache_key = course_list_cache_key()
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    courses = Course.objects.select_related('teacher').order_by('-created_at')
    payload = [serialize_course(course) for course in courses]
    cache.set(cache_key, payload, timeout=settings.CACHE_TTL_COURSE_LIST)
    return payload


@router.get("/{course_id}", response=DetailCourseOut, tags=["Courses"])
@rate_limit('course-detail')
def get_course(request, course_id: int):
    cache_key = course_detail_cache_key(course_id)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    course = get_object_or_404(
        Course.objects.select_related('teacher').prefetch_related('coursecontent_set'),
        id=course_id,
    )
    payload = serialize_course_detail(course)
    cache.set(cache_key, payload, timeout=settings.CACHE_TTL_COURSE_DETAIL)
    return payload


@router.post("/", auth=JWTAuth(), response={201: CourseOut}, tags=["Courses"])
@is_instructor
def create_course(request, data: CourseIn):
    course = Course.objects.create(teacher=request.auth, **data.dict())
    invalidate_course_cache(course.id)
    log_activity('course_created', request.auth, course)
    return 201, course


@router.patch("/{course_id}", auth=JWTAuth(), response=CourseOut, tags=["Courses"])
@is_instructor
def update_course(request, course_id: int, data: CoursePatchIn):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher_id != request.auth.id and request.auth.role != 'admin':
        raise HttpError(403, 'Forbidden: Anda bukan pemilik course ini.')

    for attr, value in data.dict(exclude_none=True).items():
        setattr(course, attr, value)
    course.save()
    invalidate_course_cache(course.id)
    log_activity('course_updated', request.auth, course)
    return course


@router.delete("/{course_id}", auth=JWTAuth(), response={204: None}, tags=["Courses"])
@is_admin
def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    log_activity('course_deleted', request.auth, course)
    course.delete()
    invalidate_course_cache(course_id)
    return 204, None


@router.post("/{course_id}/enroll", auth=JWTAuth(), response={200: CourseMemberOut}, tags=["Enrollments"])
@is_student
def enroll_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    member, _ = CourseMember.objects.get_or_create(
        course_id=course,
        user_id=request.auth,
        defaults={'roles': 'std'},
    )
    log_activity('course_enrolled', request.auth, course)
    log_learning_analytics('course_enrolled', request.auth, course)
    send_enrollment_email.delay(request.auth.id, course.id)
    update_course_statistics.delay()
    invalidate_course_cache(course.id)
    member = CourseMember.objects.select_related('course_id__teacher', 'user_id').get(id=member.id)
    return member


@router.post("/{course_id}/complete", auth=JWTAuth(), response={200: CourseMemberOut}, tags=["Enrollments"])
@is_student
def complete_course(request, course_id: int):
    member = get_object_or_404(
        CourseMember.objects.select_related('course_id__teacher', 'user_id'),
        course_id_id=course_id,
        user_id=request.auth,
    )
    if member.completed_at is None:
        member.completed_at = timezone.now()
        member.save(update_fields=['completed_at'])
        log_activity('course_completed', request.auth, member.course_id)
        log_learning_analytics('course_completed', request.auth, member.course_id)
        generate_certificate.delay(member.id)
        update_course_statistics.delay()
        invalidate_course_cache(course_id)
    return member


@router.get("/{course_id}/analytics", auth=JWTAuth(), response=AnalyticsOut, tags=["Analytics"])
@is_instructor
def course_analytics(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher_id != request.auth.id and request.auth.role != 'admin':
        raise HttpError(403, 'Forbidden: Anda bukan pemilik course ini.')
    return aggregate_course_activity(course_id)


@router.post("/{course_id}/export-report", auth=JWTAuth(), response=TaskStatusOut, tags=["Analytics"])
@is_instructor
def export_report(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher_id != request.auth.id and request.auth.role != 'admin':
        raise HttpError(403, 'Forbidden: Anda bukan pemilik course ini.')
    task = export_course_report.delay(course_id)
    log_activity('course_report_requested', request.auth, course, {'task_id': task.id})
    return {'task_id': task.id, 'message': 'Export report diproses secara asynchronous.'}
