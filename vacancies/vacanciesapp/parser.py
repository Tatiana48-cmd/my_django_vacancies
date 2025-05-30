import requests
from datetime import datetime
from django.utils.timezone import make_aware
from vacanciesapp.models import Employer, Vacancy


class HHAPIParser:
    BASE_URL = "https://api.hh.ru/vacancies"

    @classmethod
    def parse_vacancies(cls, search_text="Python", area=1, per_page=20):
        params = {
            "text": search_text,
            "area": area,
            "per_page": per_page,
        }

        try:
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return []

    @staticmethod
    def save_vacancy_data(vacancy_data):
        employer_data = vacancy_data.get('employer', {})

        employer, _ = Employer.objects.get_or_create(
            hh_id=employer_data.get('id'),
            defaults={
                'name': employer_data.get('name', ''),
                'url': employer_data.get('alternate_url'),
                'description': employer_data.get('description', ''),
            }
        )

        salary_data = vacancy_data.get('salary')

        # Исправленная обработка даты
        published_at_str = vacancy_data['published_at']
        try:
            # Парсим строку в datetime с временной зоной
            published_at = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%S%z")
            # Если дата уже содержит временную зону, не используем make_aware
        except ValueError:
            published_at = make_aware(
                datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%S")
            )

        Vacancy.objects.update_or_create(
            hh_id=vacancy_data['id'],
            defaults={
                'title': vacancy_data['name'],
                'url': vacancy_data['alternate_url'],
                'salary_from': salary_data.get('from') if salary_data else None,
                'salary_to': salary_data.get('to') if salary_data else None,
                'salary_currency': salary_data.get('currency') if salary_data else None,
                'employer': employer,
                'description': vacancy_data.get('description', ''),
                'published_at': published_at,
            }
        )