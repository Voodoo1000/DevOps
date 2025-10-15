from django.core.management.base import BaseCommand
from faker import Faker
from studentDormitory.models import Student, Room, DutySchedule, Staff, RepairRequests
from django.contrib.auth.models import User
from random import randint, choice
from datetime import timedelta
import random

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])

        # Создание пользователей
        users = []
        for _ in range(10):
            user = User.objects.create_user(username=fake.user_name(), password="password123")
            users.append(user)

        # Создание комнат
        for _ in range(300):
            Room.objects.create(number=fake.building_number(), user=random.choice(users))

        # Создание студентов
        rooms = Room.objects.all()
        for _ in range(300):
            Student.objects.create(
                name=fake.name(),
                group=f"ИСТБ-{randint(20, 30)}-{randint(1, 5)}",
                room=random.choice(rooms),
                user=random.choice(users)
            )

        # Создание персонала
        for _ in range(50):
            Staff.objects.create(
                name=fake.name(),
                post=fake.job(),
                picture=None,
                user=random.choice(users)
            )

        # Создание графика дежурств
        students = Student.objects.all()
        for _ in range(200):
            DutySchedule.objects.create(
                date=fake.date_between(start_date='-1y', end_date='today'),
                student=random.choice(students),
                user=random.choice(users)
            )

        # Создание заявок на ремонт
        statuses = ['new', 'in_progress', 'completed', 'cancelled']
        staff = Staff.objects.all()
        for _ in range(300):
            RepairRequests.objects.create(
                date=fake.date_between(start_date='-1y', end_date='today'),
                description=fake.text(),
                status=random.choice(statuses),
                room=random.choice(rooms),
                staff=random.choice(staff),
                user=random.choice(users)
            )

        self.stdout.write(self.style.SUCCESS("Данные успешно сгенерированы!"))
