from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class CourseQuerySet(models.QuerySet):
    def for_listing(self):
        return self.select_related('instructor', 'category').prefetch_related('lessons')

class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)
    
    def for_listing(self):
        return self.get_queryset().for_listing()

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructed_courses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CourseManager()

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class EnrollmentQuerySet(models.QuerySet):
    def for_student_dashboard(self):
        # Optimized for student dashboard with related course, instructor and prefetching progress
        return self.select_related('course', 'course__instructor', 'course__category').prefetch_related('progress', 'course__lessons')

class EnrollmentManager(models.Manager):
    def get_queryset(self):
        return EnrollmentQuerySet(self.model, using=self._db)
    
    def for_student_dashboard(self):
        return self.get_queryset().for_student_dashboard()

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    objects = EnrollmentManager()

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

class Progress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('enrollment', 'lesson')
        verbose_name_plural = 'progresses'

    def __str__(self):
        return f"{self.enrollment.user.username} - {self.lesson.title} (Completed)"
