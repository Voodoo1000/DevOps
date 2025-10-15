from typing import Any
from django.views.generic import TemplateView
from studentDormitory.models import Student

class ShowStudentsDormitoryView(TemplateView):
	template_name = "studentsDormitory/show_dormitory.html"

	def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
		context = super().get_context_data(**kwargs)
		context['students'] = Student.objects.all()

		return context
	
