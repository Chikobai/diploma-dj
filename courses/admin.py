from django.contrib import admin
from .models import Skill, Course, CourseSkills, OrderList, CourseCategory
from modules.models import Module


class CourseSkilsInline(admin.TabularInline):
    model = CourseSkills
    extra = 3


class CourseModuleInline(admin.TabularInline):
    model = Module
    extra = 5


class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseSkilsInline]


admin.site.register(Skill)
admin.site.register(CourseCategory)
admin.site.register(CourseSkills)
admin.site.register(Course, CourseAdmin)
admin.site.register(OrderList)
