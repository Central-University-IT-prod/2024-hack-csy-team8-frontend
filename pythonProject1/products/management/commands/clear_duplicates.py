from django.core.management.base import BaseCommand
from products.models import Membership

class Command(BaseCommand):
    help = 'Удалить дубликаты участников из группы'

    def handle(self, *args, **kwargs):
        # Получаем все записи Membership
        memberships = Membership.objects.all()

        seen = set()  # Для отслеживания уникальных комбинаций (user_id, group_id)
        duplicates = []  # Список для хранения дубликатов

        for membership in memberships:
            # Создаем уникальный идентификатор для каждой комбинации (user_id, group_id)
            identifier = (membership.user.id, membership.group.id)

            if identifier in seen:
                duplicates.append(membership)  # Если уже видели, добавляем в дубликаты
            else:
                seen.add(identifier)  # В противном случае добавляем в множество

        # Удаляем дубликаты
        for duplicate in duplicates:
            duplicate.delete()
            self.stdout.write(self.style.WARNING(f'Удален дубликат: {duplicate}'))

        self.stdout.write(self.style.SUCCESS('Очистка дубликатов завершена.'))
