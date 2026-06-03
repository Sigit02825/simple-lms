import os
import django
from django.db import connection, reset_queries

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Course, CourseMember

def demo_n_plus_one():
    print("\n--- DEMO: N+1 Problem (Tanpa Optimasi) ---")
    reset_queries()
    
    courses = Course.objects.all()
    print(f"Menjalankan iterasi pada {courses.count()} courses...")
    
    for course in courses:
        teacher_name = course.teacher.username # Query tambahan!
        print(f"Course: {course.name} | Teacher: {teacher_name}")
    
    print(f"Total Query Count (N+1): {len(connection.queries)}")

def demo_optimized():
    print("\n--- DEMO: Optimized Queries (select_related) ---")
    reset_queries()
    
    courses = Course.objects.select_related('teacher').all()
    print(f"Menjalankan iterasi pada {courses.count()} courses...")

    for course in courses:
        teacher_name = course.teacher.username # Terambil via JOIN
        print(f"Course: {course.name} | Teacher: {teacher_name}")

    print(f"Total Query Count (Optimized): {len(connection.queries)}")

if __name__ == '__main__':
    demo_n_plus_one()
    demo_optimized()
