import pytest

from django.urls import reverse

@pytest.mark.django_db
def test_get_course(api_client, course_factory):
    course = course_factory()
    response = api_client.get(
        reverse("courses-detail", kwargs={"pk": course.id})
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": course.id,
        "name": course.name,
        "students": [],
    }


@pytest.mark.django_db
def test_get_courses(api_client, course_factory):
    courses = course_factory(_quantity=2)

    response = api_client.get(reverse("courses-list"))
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": course.id,
            "name": course.name,
            "students": [],
        }
        for course in courses
    ]

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    first_course, second_course = course_factory(_quantity=2)

    response = api_client.get(
        reverse("courses-list"),
        data={"id": first_course.id},
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": first_course.id,
            "name": first_course.name,
            "students": [],
        }
    ]
    assert response.json()[0]["id"] != second_course.id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    first_course = course_factory(name="Python")
    second_course = course_factory(name="Django")

    response = api_client.get(
        reverse("courses-list"),
        data={"name": first_course.name},
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": first_course.id,
            "name": first_course.name,
            "students": [],
        }
    ]
    assert response.json()[0]["name"] != second_course.name


@pytest.mark.django_db
def test_create_course(api_client, student_factory):
    student = student_factory()
    course_data = {
        "name": "Новый курс",
        "students": [student.id],
    }

    response = api_client.post(
        reverse("courses-list"),
        data=course_data,
        format="json",
    )

    assert response.status_code == 201
    assert response.json()["name"] == course_data["name"]
    assert response.json()["students"] == course_data["students"]


@pytest.mark.django_db
def test_update_course(api_client, course_factory, student_factory):
    course = course_factory(name="Старое название")
    student = student_factory()
    course_data = {
        "name": "Новое название",
        "students": [student.id],
    }

    response = api_client.put(
        reverse("courses-detail", kwargs={"pk": course.id}),
        data=course_data,
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["id"] == course.id
    assert response.json()["name"] == course_data["name"]
    assert response.json()["students"] == course_data["students"]


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    response = api_client.delete(
        reverse("courses-detail", kwargs={"pk": course.id})
    )
    assert response.status_code == 204
    assert api_client.get(
        reverse("courses-detail", kwargs={"pk": course.id})
    ).status_code == 404