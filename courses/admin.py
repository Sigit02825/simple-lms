from django.contrib import admin
from .models import Category, Course, Lesson, Enrollment, Progress

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'created_at')
    list_filter = ('category', 'instructor')
    search_fields = ('title', 'description')
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('user__username', 'course__title')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'get_course', 'lesson', 'completed_at')
    list_filter = ('enrollment__course', 'completed_at')
    search_fields = ('enrollment__user__username', 'lesson__title')
    autocomplete_fields = ['enrollment', 'lesson']

    def get_course(self, obj):
        return obj.enrollment.course.title
    get_course.short_description = 'Course'
