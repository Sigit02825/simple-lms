from django.contrib import admin
from .models import Course, CourseMember, CourseContent, Comment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'teacher',
        'price',
        'enrollment_count',
        'completion_count',
        'created_at',
    )
    list_filter = ('teacher', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'user_id', 'roles', 'completed_at', 'certificate_path')
    list_filter = ('roles', 'completed_at')
    search_fields = ('course_id__name', 'user_id__username')

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_id', 'parent_id')
    list_filter = ('course_id',)
    search_fields = ('name', 'description')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_id', 'member_id', 'comment')
    list_filter = ('content_id',)
