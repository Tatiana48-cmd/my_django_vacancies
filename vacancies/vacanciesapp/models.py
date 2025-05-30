from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Inquiries(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название запроса")
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор запроса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название региона")

    def __str__(self):
        return self.name

class Employer(models.Model):
    hh_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    hh_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=10, blank=True, null=True)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField()


    def __str__(self):
        return f"{self.title} at {self.employer.name}"


class Employment(models.Model):
    EMPLOYMENT_TYPES = [
        ('FT', 'Полный рабочий день'),
        ('PT', 'Частичная занятость'),
        ('RM', 'Удалённая работа'),
        ('FL', 'Гибкий график'),
        ('PR', 'Проектная работа'),
    ]

    name = models.CharField(max_length=2, choices=EMPLOYMENT_TYPES, unique=True, verbose_name="Тип занятости")

    def __str__(self):
        return self.get_name_display()


class Skills(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название навыка")

    def __str__(self):
        return self.name




