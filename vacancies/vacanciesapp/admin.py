from django.contrib import admin
from vacanciesapp.models import Employer, Vacancy

# Register your models here.
from .models import Category, Inquiries, Region, Employer, Employment, Skills, Vacancy

admin.site.register(Category)
admin.site.register(Inquiries)
admin.site.register(Region)
#admin.site.register(Employer)
admin.site.register(Employment)
admin.site.register(Skills)
#admin.site.register(Vacancy)



@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name', 'hh_id', 'url')
    search_fields = ('name', 'hh_id')
    list_filter = ('name',)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'salary_from', 'salary_to', 'published_at')
    search_fields = ('title', 'employer__name')
    list_filter = ('employer', 'published_at')
    date_hierarchy = 'published_at'