from django.contrib import admin
from studentDormitory.models import Student, Room, DutySchedule, Staff, RepairRequests

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "group", "room", "user"]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "number", "user"]

@admin.register(DutySchedule)
class DutyScheduleAdmin(admin.ModelAdmin):
    list_display = ["id", "date", "student", "user"]

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "post", "user"]

@admin.register(RepairRequests)
class RepairRequestsAdmin(admin.ModelAdmin): 
    list_display = ["date", "description", "status", "room", "staff", "user"]
