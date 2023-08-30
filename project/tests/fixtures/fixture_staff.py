import pytest


@pytest.fixture
def service():
    from staff.models import Service
    return Service.objects.create(name='Service_1', abbreviation='S1')


@pytest.fixture
def dept_1(service):
    from staff.models import Dept
    return Dept.objects.create(
        name='Dept_1', abbreviation='D1', service=service,
    )


@pytest.fixture
def dept_2(service):
    from staff.models import Dept
    return Dept.objects.create(
        name='Dept_2', abbreviation='D2', service=service,
    )


@pytest.fixture
def employee_1(test_password, dept_1):
    from staff.models import Employee
    return Employee.objects.create(
        username='User_1', password=test_password, dept=dept_1,
    )


@pytest.fixture
def employee_2(test_password, dept_2):
    from staff.models import Employee
    return Employee.objects.create(
        username='User_2', password=test_password, dept=dept_2,
    )
