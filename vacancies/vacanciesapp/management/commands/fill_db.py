from django.core.management.base import BaseCommand
from vacanciesapp.parser import HHAPIParser  # Изменено с app на vacanciesapp


class Command(BaseCommand):
    help = 'Заполняет базу данных вакансиями с hh.ru'

    def add_arguments(self, parser):
        parser.add_argument(
            '--search',
            type=str,
            default="Python",
            help='Текст для поиска вакансий (по умолчанию: Python)'
        )
        parser.add_argument(
            '--area',
            type=int,
            default=1,
            help='ID региона (1 - Москва, 2 - СПб)'
        )
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Количество вакансий для загрузки (макс. 100)'
        )

    def handle(self, *args, **options):
        search_text = options['search']
        area_id = options['area']
        vacancies_count = min(options['count'], 100)

        self.stdout.write(f"Начинаем загрузку вакансий с параметрами:")
        self.stdout.write(f"Поиск: '{search_text}'")
        self.stdout.write(f"Регион ID: {area_id}")
        self.stdout.write(f"Количество: {vacancies_count}")

        vacancies = HHAPIParser.parse_vacancies(
            search_text=search_text,
            area=area_id,
            per_page=vacancies_count
        )

        for vacancy in vacancies:
            HHAPIParser.save_vacancy_data(vacancy)
            self.stdout.write(f"Добавлена вакансия: {vacancy['name']}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно загружено {len(vacancies)} вакансий!"
            )
        )