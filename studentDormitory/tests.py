from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
from django.contrib.auth.models import User
from datetime import datetime
from studentDormitory.models import Student, Room, DutySchedule, Staff, RepairRequests

#test
class StudentsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_get_list(self):
        rm = baker.make("studentDormitory.Room", user=self.user)
        student = baker.make("Student", room=rm, user=self.user)

        r = self.client.get('/api/students/')
        data = r.json()

        assert len(data) == 1
        assert student.name == data[0]['name']
        assert student.id == data[0]['id']
        assert student.room.id == data[0]['room']['id']
        assert student.room.number == data[0]['room']['number']
        assert student.group == data[0]['group']

    def test_create_student(self):
        rm = baker.make("studentDormitory.Room", user=self.user)
        r = self.client.post('/api/students/', {
            "name": "Студент",
            "group": "ИСТб-22-2",
            "room_id": rm.id
        })

        new_student_id = r.json()['id']
        new_student = Student.objects.get(id=new_student_id)

        assert new_student.name == 'Студент'
        assert new_student.group == 'ИСТб-22-2'
        assert new_student.room == rm
        assert new_student.user == self.user

    def test_delete_student(self):
        students = baker.make("Student", 10, user=self.user)
        r = self.client.get('/api/students/')
        data = r.json()
        assert len(data) == 10

        student_id_to_delete = students[3].id
        self.client.delete(f'/api/students/{student_id_to_delete}/')

        r = self.client.get('/api/students/')
        data = r.json()
        assert len(data) == 9
        assert student_id_to_delete not in [i['id'] for i in data]

    def test_update_student(self):
        students = baker.make("Student", 10, user=self.user)
        student = students[2]

        r = self.client.get(f'/api/students/{student.id}/')
        data = r.json()
        assert data['name'] == student.name

        update_data = {
            "name": "Вася Иванов",
            "group": student.group
        }
        if student.room:
            update_data["room_id"] = student.room.id

        r = self.client.patch(f'/api/students/{student.id}/', update_data)
        assert r.status_code == 200

        r = self.client.get(f'/api/students/{student.id}/')
        data = r.json()
        assert data['name'] == "Вася Иванов"

        student.refresh_from_db()
        assert student.name == "Вася Иванов"


class RoomViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_get_list(self):
        room = baker.make("Room", user=self.user)
        r = self.client.get('/api/rooms/')
        data = r.json()

        assert len(data) == 1
        assert room.id == data[0]['id']
        assert room.number == data[0]['number']

    def test_create_room(self):
        r = self.client.post('/api/rooms/', {
            "number": "101"
        })

        new_room_id = r.json()['id']
        new_room = Room.objects.get(id=new_room_id)

        assert new_room.number == "101"
        assert new_room.user == self.user 

    def test_delete_room(self):
        rooms = baker.make("Room", 10, user=self.user)
        r = self.client.get('/api/rooms/')
        data = r.json()
        assert len(data) == 10

        room_id_to_delete = rooms[3].id
        self.client.delete(f'/api/rooms/{room_id_to_delete}/')

        r = self.client.get('/api/rooms/')
        data = r.json()
        assert len(data) == 9
        assert room_id_to_delete not in [i['id'] for i in data]

    def test_update_room(self):
        rooms = baker.make("Room", 10, user=self.user)
        room = rooms[2]

        r = self.client.get(f'/api/rooms/{room.id}/')
        data = r.json()
        assert data['number'] == room.number

        update_data = {"number": "209б"}
        r = self.client.patch(f'/api/rooms/{room.id}/', update_data)
        assert r.status_code == 200

        r = self.client.get(f'/api/rooms/{room.id}/')
        data = r.json()
        assert data['number'] == "209б"

        room.refresh_from_db()
        assert room.number == "209б"


class DutyScheduleViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_get_list(self):
        student = baker.make("Student", user=self.user)
        duty = baker.make("DutySchedule", student=student, user=self.user)

        r = self.client.get('/api/dutySchedule/')
        data = r.json()

        response_date = datetime.strptime(data[0]['date'], "%Y-%m-%d").date()
        assert duty.date == response_date
        assert duty.id == data[0]['id']
        assert duty.student.id == data[0]['student']['id']
        assert len(data) == 1

    def test_create_duty_schedule(self):
        student = baker.make("Student", user=self.user)
        r = self.client.post('/api/dutySchedule/', {
            "date": "2024-09-18",
            "student_id": student.id
        })

        new_duty_id = r.json()['id']
        new_duty = DutySchedule.objects.get(id=new_duty_id)

        expected_date = datetime.strptime("2024-09-18", "%Y-%m-%d").date()
        assert new_duty.date == expected_date
        assert new_duty.student == student
        assert new_duty.user == self.user

    def test_delete_duty_schedule(self):
        duty_schedules = baker.make("DutySchedule", 10, user=self.user)
        r = self.client.get('/api/dutySchedule/')
        data = r.json()
        assert len(data) == 10

        duty_id_to_delete = duty_schedules[3].id
        self.client.delete(f'/api/dutySchedule/{duty_id_to_delete}/')

        r = self.client.get('/api/dutySchedule/')
        data = r.json()
        assert len(data) == 9
        assert duty_id_to_delete not in [i['id'] for i in data]

    def test_update_duty_schedule(self):
        duty_schedules = baker.make("DutySchedule", 10, user=self.user)
        duty = duty_schedules[2]

        r = self.client.get(f'/api/dutySchedule/{duty.id}/')
        data = r.json()
        assert data['date'] == duty.date.strftime("%Y-%m-%d")

        update_data = {"date": "2024-09-18"}
        r = self.client.patch(f'/api/dutySchedule/{duty.id}/', update_data)
        assert r.status_code == 200

        r = self.client.get(f'/api/dutySchedule/{duty.id}/')
        data = r.json()
        assert data['date'] == "2024-09-18"

        duty.refresh_from_db()
        assert duty.date.strftime("%Y-%m-%d") == "2024-09-18"


class StaffViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_get_list(self):
        staff = baker.make("Staff", user=self.user)
        r = self.client.get('/api/staff/')
        data = r.json()

        assert len(data) == 1
        assert staff.id == data[0]['id']
        assert staff.name == data[0]['name']
        assert staff.post == data[0]['post']

    def test_create_staff(self):
        r = self.client.post('/api/staff/', {
            "name": "Вася Пупкин",
            "post": "Каменщик"
        })

        new_staff_id = r.json()['id']
        new_staff = Staff.objects.get(id=new_staff_id)

        assert new_staff.name == "Вася Пупкин"
        assert new_staff.post == "Каменщик"
        assert new_staff.user == self.user

    def test_delete_staff(self):
        staff = baker.make("Staff", 10, user=self.user)
        r = self.client.get('/api/staff/')
        data = r.json()
        assert len(data) == 10

        staff_id_to_delete = staff[3].id
        self.client.delete(f'/api/staff/{staff_id_to_delete}/')

        r = self.client.get('/api/staff/')
        data = r.json()
        assert len(data) == 9
        assert staff_id_to_delete not in [i['id'] for i in data]

    def test_update_staff(self):
        staff = baker.make("Staff", 10, user=self.user)
        stf = staff[2]

        r = self.client.get(f'/api/staff/{stf.id}/')
        data = r.json()
        assert data['post'] == stf.post

        update_data = {"post": "Каменщик"}
        r = self.client.patch(f'/api/staff/{stf.id}/', update_data)
        assert r.status_code == 200

        r = self.client.get(f'/api/staff/{stf.id}/')
        data = r.json()
        assert data['post'] == "Каменщик"

        stf.refresh_from_db()
        assert stf.post == "Каменщик"


class RepairRequestsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_get_list(self):
        room = baker.make("Room", user=self.user)
        staff = baker.make("Staff", user=self.user)
        req = baker.make("RepairRequests", room=room, staff=staff, user=self.user)

        r = self.client.get('/api/repairRequests/')
        data = r.json()

        response_date = datetime.strptime(data[0]['date'], "%Y-%m-%d").date()
        assert req.date == response_date
        assert req.id == data[0]['id']
        assert req.description == data[0]['description']
        assert req.status == data[0]['status']
        assert req.room.id == data[0]['room']['id']
        assert req.staff.id == data[0]['staff']['id']
        assert len(data) == 1

    def test_create_repair_requests(self):
        room = baker.make("Room", user=self.user)
        staff = baker.make("Staff", user=self.user)

        r = self.client.post('/api/repairRequests/', {
            "date": "2024-09-18",
            "description": "afgasf",
            "status": "completed",
            "room_id": room.id,
            "staff_id": staff.id
        })

        new_req_id = r.json()['id']
        new_req = RepairRequests.objects.get(id=new_req_id)

        expected_date = datetime.strptime("2024-09-18", "%Y-%m-%d").date()
        assert new_req.date == expected_date
        assert new_req.description == "afgasf"
        assert new_req.status == "completed"
        assert new_req.room == room
        assert new_req.staff == staff
        assert new_req.user == self.user

    def test_delete_repair_request(self):
        requests = baker.make("RepairRequests", 10, user=self.user)
        r = self.client.get('/api/repairRequests/')
        data = r.json()
        assert len(data) == 10

        req_id_to_delete = requests[3].id
        self.client.delete(f'/api/repairRequests/{req_id_to_delete}/')

        r = self.client.get('/api/repairRequests/')
        data = r.json()
        assert len(data) == 9
        assert req_id_to_delete not in [i['id'] for i in data]

    def test_update_repair_request(self):
        requests = baker.make("RepairRequests", 10, user=self.user)
        req = requests[2]

        r = self.client.get(f'/api/repairRequests/{req.id}/')
        data = r.json()
        assert data['status'] == req.status

        update_data = {"status": "cancelled"}
        r = self.client.patch(f'/api/repairRequests/{req.id}/', update_data)
        assert r.status_code == 200

        r = self.client.get(f'/api/repairRequests/{req.id}/')
        data = r.json()
        assert data['status'] == "cancelled"

        req.refresh_from_db()
        assert req.status == "cancelled"