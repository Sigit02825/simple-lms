import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from courses.models import Category, Course, Lesson, Enrollment, Progress

def seed_data():
    # Clear existing data
    Progress.objects.all().delete()
    Enrollment.objects.all().delete()
    Lesson.objects.all().delete()
    Course.objects.all().delete()
    Category.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()
    User.objects.filter(username='admin').delete()

    # Create Users
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
    instructor = User.objects.create_user('instructor1', 'instructor1@example.com', 'pass123', role='instructor')
    student = User.objects.create_user('student1', 'student1@example.com', 'pass123', role='student')

    # Create Categories
    programming = Category.objects.create(name='Programming')
    python_cat = Category.objects.create(name='Python', parent=programming)
    web_dev = Category.objects.create(name='Web Development', parent=programming)

    # Create Courses
    course1 = Course.objects.create(
        title='Django for Beginners',
        description='Learn Django from scratch',
        instructor=instructor,
        category=python_cat
    )
    
    course2 = Course.objects.create(
        title='Advanced React',
        description='Deep dive into React',
        instructor=instructor,
        category=web_dev
    )

    # Create Lessons
    for i in range(1, 6):
        Lesson.objects.create(course=course1, title=f'Django Lesson {i}', content=f'Content {i}', order=i)
        Lesson.objects.create(course=course2, title=f'React Lesson {i}', content=f'Content {i}', order=i)

    # Enrollments
    enrollment = Enrollment.objects.create(user=student, course=course1)
    
    # Progress
    lessons = course1.lessons.all()
    for lesson in lessons[:3]: # Complete 3 lessons
        Progress.objects.create(enrollment=enrollment, lesson=lesson)

    print("Data seeded successfully!")

if __name__ == '__main__':
    seed_data()
