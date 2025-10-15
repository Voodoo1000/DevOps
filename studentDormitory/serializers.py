from rest_framework import serializers
from studentDormitory.models import Student, Room, DutySchedule, Staff, RepairRequests
from datetime import datetime

class RoomSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		if 'request' in self.context:
			validated_data['user'] = self.context['request'].user
			
		return super().create(validated_data)
	
	class Meta:
		model = Room
		fields = ["id", "number", "user"]

class StudentSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		if 'request' in self.context:
			validated_data['user'] = self.context['request'].user
			
		return super().create(validated_data)
	
	room = RoomSerializer(read_only=True)
	room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), write_only=True, source="room")

	class Meta:
			model = Student
			fields = ["id", "name", "group", "room", "room_id", "picture", "user"]


class DutyScheduleSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		if 'request' in self.context:
			validated_data['user'] = self.context['request'].user
			
		return super().create(validated_data)
	
	student = StudentSerializer(read_only=True)
	student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True, source="student")

	class Meta:
		model = DutySchedule
		fields = ["id", "date", "student", "student_id", "user"]

class StaffSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		if 'request' in self.context:
			validated_data['user'] = self.context['request'].user
			
		return super().create(validated_data)
	
	class Meta:
		model = Staff
		fields = ["id", "name", "post", "picture", "user"]

class RepairRequestsSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		if 'request' in self.context:
			validated_data['user'] = self.context['request'].user
			
		return super().create(validated_data)
	
	room = RoomSerializer(read_only=True)
	room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), write_only=True, source="room")
	staff = StaffSerializer(read_only=True)
	staff_id = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all(), write_only=True, source="staff")
	status_display = serializers.CharField(source='get_status_display', read_only=True)

	class Meta:
		model = RepairRequests
		fields = ["id", "date", "description", "status", 'status_display', "room", "room_id", "staff", "staff_id", "user"]