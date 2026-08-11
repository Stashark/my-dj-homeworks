import pytest

from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def course_factory():
    def create_course(**kwargs):
        return baker.make(Course, **kwargs)
    return create_course

@pytest.fixture
def student_factory():
    def create_student(**kwargs):
        return baker.make(Student, **kwargs)
    return create_student