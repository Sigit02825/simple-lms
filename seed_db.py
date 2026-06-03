import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from courses.models import Course, CourseMember, CourseContent, Comment

def seed_data():
    # Clear existing data
    Comment.objects.all().delete()
    CourseContent.objects.all().delete()
    CourseMember.objects.all().delete()
    Course.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    # Create Users
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
    
    instructor = User.objects.create_user('instructor1', 'instructor1@example.com', 'pass123', role='instructor')
    student = User.objects.create_user('student1', 'student1@example.com', 'pass123', role='student')

    # Create Courses
    course1 = Course.objects.create(
        name='Pemrograman Web dengan Django',
        description='Belajar membuat aplikasi web dengan framework Django',
        price=50000,
        teacher=instructor
    )
    
    course2 = Course.objects.create(
        name='Docker untuk Pemula',
        description='Belajar containerization menggunakan Docker',
        price=75000,
        teacher=instructor
    )

    # Course Members
    CourseMember.objects.create(course_id=course1, user_id=student, roles='std')
    CourseMember.objects.create(course_id=course2, user_id=student, roles='std')

    # Course Contents
    content1 = CourseContent.objects.create(
        name='Pengenalan Django',
        description='Apa itu Django?',
        course_id=course1
    )
    
    content2 = CourseContent.objects.create(
        name='Instalasi Django',
        description='Cara menginstall Django di lokal',
        course_id=course1,
        parent_id=content1
    )

    # Comments
    Comment.objects.create(
        content_id=content1,
        member_id=CourseMember.objects.get(course_id=course1, user_id=student),
        comment='Sangat membantu!'
    )

    print("Data seeded successfully according to Chapter 4!")

if __name__ == '__main__':
    seed_data()
