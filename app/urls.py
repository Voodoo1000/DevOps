"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from studentDormitory.api import StudentViewset, RoomViewset, DutyScheduleViewset, StaffViewset, RepairRequestsViewset, UserViewset
from studentDormitory import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register("students", StudentViewset, basename="students")
router.register("rooms", RoomViewset, basename="rooms")
router.register("dutySchedule", DutyScheduleViewset, basename="dutySchedule")
router.register("staff", StaffViewset, basename="staff")
router.register("repairRequests", RepairRequestsViewset, basename="repairRequests")
router.register("user", UserViewset, basename="user")

urlpatterns = [
	path('', views.ShowStudentsDormitoryView.as_view()),
    path('admin/', admin.site.urls),
	path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
