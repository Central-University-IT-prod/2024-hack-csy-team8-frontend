# management/commands/remove_duplicate_memberships.py
from django.core.management.base import BaseCommand
from django.db.models import Count
from products.models import Membership

class Command(BaseCommand):
    help = 'Удаляет дублирующиеся участники в группах'

    def handle(self, *args, **options):
        # Находим дубликаты
        duplicates = (
            Membership.objects
            .values('user', 'group')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        for duplicate in duplicates:
            user_id = duplicate['user']
            group_id = duplicate['group']

            # Получаем все записи для данного дубликата
            memberships = Membership.objects.filter(user_id=user_id, group_id=group_id)

            # Удаляем все, кроме одной записи
            memberships_to_delete = memberships[1:]  # Все, кроме первой
            for membership in memberships_to_delete:
                membership.delete()
                self.stdout.write(self.style.SUCCESS(f'Удалён дубликат: пользователь {user_id} в группе {group_id}'))

        self.stdout.write(self.style.SUCCESS('Очистка дубликатов завершена.'))
