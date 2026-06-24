from pathlib import Path

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count, Q

from .models import Course, CourseMember
from .services import (
    export_course_report_file,
    log_activity,
    log_learning_analytics,
)


@shared_task
def send_enrollment_email(user_id: int, course_id: int):
    member = CourseMember.objects.select_related('user_id', 'course_id').get(
        user_id=user_id,
        course_id=course_id,
    )
    send_mail(
        subject=f'Enrollment Berhasil: {member.course_id.name}',
        message=(
            f'Halo {member.user_id.username},\n\n'
            f'Anda berhasil enroll ke course {member.course_id.name}.'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[member.user_id.email or 'student@example.com'],
        fail_silently=True,
    )
    log_activity('enrollment_email_sent', member.user_id, member.course_id)
    return {'status': 'sent'}


@shared_task
def generate_certificate(course_member_id: int):
    member = CourseMember.objects.select_related('user_id', 'course_id').get(id=course_member_id)
    output_dir = Path(settings.MEDIA_ROOT) / 'certificates'
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f'certificate-{member.course_id.id}-{member.user_id.id}.txt'
    file_path.write_text(
        (
            'SERTIFIKAT PENYELESAIAN\n'
            f'Peserta: {member.user_id.username}\n'
            f'Course: {member.course_id.name}\n'
        ),
        encoding='utf-8',
    )
    member.certificate_path = str(file_path)
    member.save(update_fields=['certificate_path'])
    log_activity('certificate_generated', member.user_id, member.course_id, {'file_path': str(file_path)})
    log_learning_analytics('certificate_generated', member.user_id, member.course_id)
    return str(file_path)


@shared_task
def update_course_statistics():
    stats = CourseMember.objects.values('course_id').annotate(
        total_enrollments=Count('id'),
        total_completions=Count('id', filter=Q(completed_at__isnull=False)),
    )
    updates = 0
    for row in stats:
        Course.objects.filter(id=row['course_id']).update(
            enrollment_count=row['total_enrollments'],
            completion_count=row['total_completions'],
        )
        updates += 1
    return {'updated_courses': updates}


@shared_task
def export_course_report(course_id: int):
    course = Course.objects.get(id=course_id)
    members = CourseMember.objects.select_related('user_id').filter(course_id=course)
    file_path = export_course_report_file(course, members)
    log_activity('course_report_exported', None, course, {'file_path': file_path})
    log_learning_analytics('course_report_exported', None, course, {'file_path': file_path})
    return file_path
