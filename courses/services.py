import csv
from functools import wraps
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from ninja.errors import HttpError
from pymongo import MongoClient


_mongo_client = None


def get_mongo_client() -> MongoClient:
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(settings.MONGODB_URI)
    return _mongo_client


def get_mongo_database():
    return get_mongo_client()[settings.MONGODB_DB_NAME]


def activity_logs_collection():
    return get_mongo_database()['activity_logs']


def learning_analytics_collection():
    return get_mongo_database()['learning_analytics']


def log_activity(action: str, user=None, course=None, metadata: dict[str, Any] | None = None):
    activity_logs_collection().insert_one({
        'action': action,
        'user_id': getattr(user, 'id', None),
        'username': getattr(user, 'username', None),
        'course_id': getattr(course, 'id', None),
        'course_name': getattr(course, 'name', None),
        'metadata': metadata or {},
        'created_at': timezone.now(),
    })


def log_learning_analytics(event_type: str, user=None, course=None, metadata: dict[str, Any] | None = None):
    learning_analytics_collection().insert_one({
        'event_type': event_type,
        'user_id': getattr(user, 'id', None),
        'username': getattr(user, 'username', None),
        'course_id': getattr(course, 'id', None),
        'course_name': getattr(course, 'name', None),
        'metadata': metadata or {},
        'created_at': timezone.now(),
    })


def aggregate_course_activity(course_id: int):
    pipeline = [
        {'$match': {'course_id': course_id}},
        {
            '$group': {
                '_id': '$action',
                'count': {'$sum': 1},
                'users': {'$addToSet': '$user_id'},
            }
        },
    ]
    result = list(activity_logs_collection().aggregate(pipeline))
    action_breakdown = {item['_id']: item['count'] for item in result}
    unique_users = len({user_id for item in result for user_id in item.get('users', []) if user_id})
    total_events = sum(item['count'] for item in result)
    return {
        'course_id': course_id,
        'total_events': total_events,
        'action_breakdown': action_breakdown,
        'unique_users': unique_users,
    }


def course_list_cache_key():
    return 'courses:list:v1'


def course_detail_cache_key(course_id: int):
    return f'courses:detail:{course_id}:v1'


def invalidate_course_cache(course_id: int | None = None):
    cache.delete(course_list_cache_key())
    if course_id is not None:
        cache.delete(course_detail_cache_key(course_id))


def rate_limit(scope: str):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            identity = request.META.get('REMOTE_ADDR', 'anonymous')
            key = f'rate-limit:{scope}:{identity}'
            current_count = cache.get(key)
            if current_count is None:
                cache.set(key, 1, timeout=settings.RATE_LIMIT_WINDOW)
            else:
                current_count = cache.incr(key)
                if current_count > settings.RATE_LIMIT_REQUESTS:
                    raise HttpError(429, 'Rate limit exceeded. Maksimal 60 request per menit.')
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def serialize_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }


def serialize_course(course):
    return {
        'id': course.id,
        'name': course.name,
        'description': course.description,
        'price': course.price,
        'image': course.image.url if course.image else None,
        'teacher': serialize_user(course.teacher),
        'enrollment_count': course.enrollment_count,
        'completion_count': course.completion_count,
        'created_at': course.created_at,
        'updated_at': course.updated_at,
    }


def serialize_course_detail(course):
    payload = serialize_course(course)
    payload['contents'] = [
        {'id': content.id, 'name': content.name}
        for content in course.coursecontent_set.all()
    ]
    return payload


def ensure_output_dir(directory_name: str) -> Path:
    output_dir = Path(settings.MEDIA_ROOT) / directory_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def export_course_report_file(course, members):
    output_dir = ensure_output_dir('reports')
    file_path = output_dir / f'course-report-{course.id}.csv'
    with file_path.open('w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['course_name', 'student_username', 'role', 'completed_at'])
        for member in members:
            writer.writerow([
                course.name,
                member.user_id.username,
                member.roles,
                member.completed_at.isoformat() if member.completed_at else '',
            ])
    return str(file_path)
