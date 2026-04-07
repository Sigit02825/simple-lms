import os
import django
from django.db import connection, reset_queries

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Course, Enrollment

def demo_n_plus_one():
    print("\n--- DEMO: N+1 Problem (Tanpa Optimasi) ---")
    reset_queries()
    
    # Query standar tanpa select_related atau prefetch_related
    courses = Course.objects.all()
    print(f"Menjalankan iterasi pada {courses.count()} courses...")
    
    for course in courses:
        # Mengakses foreign key instructor memicu query tambahan untuk setiap iterasi
        instructor_name = course.instructor.username 
        # Mengakses foreign key category memicu query tambahan
        category_name = course.category.name if course.category else "N/A"
        # Mengakses reverse relation lessons memicu query tambahan
        lessons = list(course.lessons.all())
        print(f"Course: {course.title} | Instructor: {instructor_name} | Category: {category_name} | Lessons: {len(lessons)}")
    
    print(f"Total Query Count (N+1): {len(connection.queries)}")

def demo_optimized():
    print("\n--- DEMO: Optimized Queries (select_related & prefetch_related) ---")
    reset_queries()
    
    # Menggunakan for_listing() yang menggunakan select_related dan prefetch_related
    courses = Course.objects.for_listing()
    print(f"Menjalankan iterasi pada {courses.count()} courses...")

    for course in courses:
        # Instructor dan Category sudah diambil via select_related (JOIN)
        instructor_name = course.instructor.username 
        category_name = course.category.name if course.category else "N/A"
        # Lessons sudah diambil via prefetch_related (Separate query, then matched in Python)
        lessons = course.lessons.all()
        print(f"Course: {course.title} | Instructor: {instructor_name} | Category: {category_name} | Lessons: {len(lessons)}")

    print(f"Total Query Count (Optimized): {len(connection.queries)}")

def demo_student_dashboard():
    print("\n--- DEMO: Student Dashboard Optimization ---")
    reset_queries()
    
    enrollments = Enrollment.objects.for_student_dashboard()
    print(f"Menjalankan iterasi pada {enrollments.count()} enrollments...")

    for enrollment in enrollments:
        course_title = enrollment.course.title
        instructor = enrollment.course.instructor.username
        # Progress sudah diprefetch
        completed_lessons = len(enrollment.progress.all())
        print(f"Student: {enrollment.user.username} | Course: {course_title} | Instructor: {instructor} | Completed Lessons: {completed_lessons}")

    print(f"Total Query Count (Dashboard Optimized): {len(connection.queries)}")

if __name__ == '__main__':
    demo_n_plus_one()
    demo_optimized()
    demo_student_dashboard()
