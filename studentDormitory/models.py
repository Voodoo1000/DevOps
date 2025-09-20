from django.db import models

class Student(models.Model):
	name = models.TextField("ФИО")
	group = models.TextField("Группа", default="ИСТБ-22-2")
	room = models.ForeignKey("Room", on_delete=models.CASCADE, null=True)
	picture = models.ImageField("Изображение", null=True, upload_to="students")
	user = models.ForeignKey('auth.User', verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

	class Meta:
		verbose_name = "Студент"
		verbose_name_plural = "Студенты"

	def __str__(self) -> str:
		return self.name

class Room(models.Model):
	number = models.TextField("Номер комнаты")
	user = models.ForeignKey('auth.User', verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

	class Meta:
			verbose_name = "Комната"
			verbose_name_plural = "Комнаты"

	def __str__(self) -> str:
		return self.number

class DutySchedule(models.Model):
	date = models.DateField("Дата")
	student = models.ForeignKey("Student", on_delete=models.CASCADE, null=True)
	user = models.ForeignKey('auth.User', verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

	class Meta:
			verbose_name = "График дежурств"
			verbose_name_plural = "График дежурств"

class Staff(models.Model):
	name = models.TextField("ФИО")
	post = models.TextField("Должность")
	picture = models.ImageField("Изображение", null=True, upload_to="staff")
	user = models.ForeignKey('auth.User', verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

	class Meta:
			verbose_name = "Персонал"
			verbose_name_plural = "Персонал"

	def __str__(self) -> str:
		return self.name

class RepairRequests(models.Model):
	STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В процессе"),
        ("completed", "Завершена"),
        ("cancelled", "Отменена"),
    ]
	
	date = models.DateField("Дата создания")
	description = models.TextField("Описание проблемы")
	status = models.CharField("Статус заявки", max_length=20, choices=STATUS_CHOICES, default="new")
	room = models.ForeignKey("Room", on_delete=models.CASCADE, null=True)
	staff = models.ForeignKey("Staff", on_delete=models.CASCADE, null=True)
	user = models.ForeignKey('auth.User', verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

	class Meta:
			verbose_name = "Заявка на ремонт"
			verbose_name_plural = "Заявки на ремонт"
